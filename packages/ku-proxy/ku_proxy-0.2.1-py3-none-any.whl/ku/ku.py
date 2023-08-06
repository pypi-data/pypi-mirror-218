"""
    Ku
    ==
    single-threaded async mitm tcp proxy
"""

from threading import Thread, currentThread
from select import select
from socket import socket, SOL_SOCKET, AF_INET, AF_INET6
import logging

from typing import Union, Tuple, List

from enum import Enum
from time import time, sleep
from re import match

from platform import system

# https://learn.microsoft.com/en-us/windows/win32/winsock/so-conditional-accept
SO_CONDITIONAL_ACCEPT = 0x3002

class Reject(object):
    pass

class Pass(object):
    pass

class state(Enum):
    DISCONNECTED = 0
    CLIENT_W_U = 1 # client waiting for upstream
    CONNECTED = 2

class tcpsession(object):

    _state: state = state.DISCONNECTED

    client: socket
    server: socket

    client_total: int
    server_total: int

    estab_time: int

    def __init__(self, client: socket, server: socket, proxy, *args) -> None:
        pass

    def clientbound(self, data: bytes) -> Union[bytes, Reject, Pass]:
        pass

    def serverbound(self, data) -> Union[bytes, Reject, Pass]:
        pass

    def connection_lost(self, side: Union[socket, None], err: Union[Exception, None]) -> None:
        pass
    
    def shutdown(self) -> None:
        pass

    def _change_state(self, new_state: state) -> None:
        self.proxy._logger.debug(f"#{id(self)} {self._state} -> {new_state}")
        self._state = new_state

    def terminate(self) -> None:
        self.proxy.terminate(self)

    def __repr__(self):        
        if self._state != state.CONNECTED:
            return super().__repr__()
        return f"<#{id(self)}[{round((time() - self.estab_time), 2)}] {self.client.getpeername()}->{self.client.getsockname()}::{self.server.getsockname()}->{self.server.getpeername()}>"

class ku(object):

    fd: List[socket]  # tracked file descriptors
    wai: List[socket] # wa
    ss: List[tcpsession]

    sockets: Tuple[socket]  # listening socket
    thread: Thread  # polling thread
    upstream: tuple  # upstream proto, host, port

    alive: bool = True  # alive marker
    pause: bool = False # you can temporarily stop polling
    PSM = 0.00001 # power Save Mode, reduces cpu cycles count

    @staticmethod
    def _resolve_proto(host: str):

        IPv6 = r"^(\[[\d\D]{1,}\])$"
        IP6 = r"^([a-f0-9:]{1,})$"
        IPv4 = r"^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})$"
        TLD = r"^([A-z0-9._-]{1,})$"

        PATTERNS = [IPv6, IPv4, TLD, IP6]

        for pattern in PATTERNS:
            i = match(pattern, host)
            if i:
                if pattern is IPv6:
                    return AF_INET6
                
                elif pattern is IP6:
                    return AF_INET6

                elif pattern is IPv4:
                    return AF_INET

                elif pattern is TLD:
                    return -1

    def __init__(self, listen: tuple, upstream: tuple, session: tcpsession = tcpsession, session_args: tuple = (), maxcon: int = -1, upstream_6: bool = False, loglevel = logging.ERROR):

        self.fd: list = []
        self.wai: list = []
        self.ss: list = []

        self._logger = logging.getLogger("ku.devel")
        self._logger.setLevel(loglevel)

        proto = self._resolve_proto(upstream[0])
        self.upstream = (AF_INET6 if upstream_6 else AF_INET if proto == -1 else proto, upstream[0], upstream[1])
        self._logger.debug(f"Upstreaming to - {'v6' if self.upstream[0] is AF_INET6 else 'v4'} {upstream[0]}:{upstream[1]}")

        self.session = session
        self.maxcon = maxcon
        self.session_args = session_args

        self.sockets = ()
        for i in range(0, len(listen), 2):
            proto, host, port = self._resolve_proto(listen[i]), *listen[i:i+2]

            sock = socket(proto, 1)
            self._logger.debug(f"Listening at - {'v6' if proto is AF_INET6 else 'v4'} {host}:{port}")
            sock.bind((host, port))
            if system() == "Windows":
                sock.setsockopt(SOL_SOCKET, SO_CONDITIONAL_ACCEPT, 1)
            sock.listen()
            self.fd.append(sock)
            self.sockets = (*self.sockets, sock)

        self.thread = Thread(target=self.poll, name=f"Ku poller #{id(self)}", daemon=True)
        self.thread.start()

    def shutdown(self):
        # can't be called from handler!)
        if currentThread() is self.thread:
            raise RuntimeError(f"People stuck at {currentThread()}")

        self.alive = False
        while self.thread.is_alive():
            pass

        for s in self.ss:
            if s._state == state.CONNECTED:
                s.shutdown()

            s.client.shutdown(1)
            s.server.shutdown(1)
            s._change_state(state.DISCONNECTED)

        del self.fd
        del self.ss        
        for sock in self.sockets:
            sock.close()
        del self.sockets
        del self.thread

    def terminate(self, session: tcpsession):
        session._change_state(state.DISCONNECTED)
        # Call handlers
        session.connection_lost(None, RuntimeError("Internal terminate request"))
        # Remove descriptors from polling
        self.fd.remove(session.client)
        self.fd.remove(session.server)
        # Shutdown sockets
        session.client.shutdown(2)
        session.server.shutdown(2)
        # Delete session
        self.ss.remove(session)
        self._logger.debug(f"#{id(session)} terminated [ITR]")

    def _handle_socket_disconnect(self, fd, err):            
        s = self.lookup_session(fd)        
        if not s:
            # ITR
            return

        # Remove descriptors from wathcing list
        self.fd.remove(s.client)
        self.fd.remove(s.server)

        # Close associated descripors
        s.server.close()
        s.client.close()

        # Destroy session instance
        self.ss.remove(s)

        s._change_state(state.DISCONNECTED)
        s.connection_lost(fd, err)

        self._logger.debug(f"#{id(s)} terminated")

    def lookup_session(self, fd: socket):
        for s in self.ss:
            if s.client == fd or s.server == fd:
                return s

    def send(self, fd: socket, data: bytes) -> None:
        try:
            fd.sendall(data)
        except Exception as e:
            self._logger.debug(f"Failed to send data to the fd, initiating session termination...")
            self._handle_socket_disconnect(fd, e)

    def _accept(self, fd: socket):
        # check limitations
        if len(self.ss) == self.maxcon:
            try:
                c, addr = fd.accept()
                c.close()
            except:
                pass
            return
        
        # create new instance of tcpsession class
        s = object.__new__(self.session)
        s.proxy = self
        self._logger.debug(f"#{id(s)} Begin new connection request processing")

        # new client
        try:
            c, addr = fd.accept()
        except Exception as e:
            self._logger.warning(f"Failed to accept new client: {e}")
            self._logger.debug(f"#{id(s)} terminated")
            return
            
        self._logger.debug(f"#{id(s)} client: {addr}")
        s.client = c

        s._change_state(state.CLIENT_W_U)

        # new upstream
        u = socket(self.upstream[0], 1)
        u.settimeout(0)
        s.server = u

        try:                        
            u.connect(self.upstream[1:])
        except BlockingIOError:
            pass

        self._logger.debug(f"#{id(s)} upstreaming initiated, waiting...")        

        self.ss.append(s)                    
        self.wai.append(u)

    def poll(self):
        self._logger.debug("Begin polling")

        while self.alive:
            # select()
            fds, puo, puf = select(self.fd, self.wai, self.wai, 0)
            if not (fds or puo or puf) or self.pause:
                if self.PSM:
                    sleep(self.PSM)
                continue

            for fd in puo:                
                s = self.lookup_session(fd)
                self._logger.debug(f"#{id(s)} upstreamed, initiating trasmisson")

                # Remove upstream from waiting list
                self.wai.remove(fd)

                # Add client & upstream to watging list
                self.fd.append(fd)
                self.fd.append(s.client)

                # Change session state
                s._change_state(state.CONNECTED)

                s.estab_time = time()

                # Init session
                s.__init__(s.client, fd, self, *self.session_args)

            for fd in puf:
                s = self.lookup_session(fd)
                self._logger.debug(f"#{id(s)} Failed to upstream")

                # Remove upstream from waiting list
                self.wai.remove(fd)

                # Close associated client & upstream descriptors
                s.client.close()
                fd.close()

                # Change session state
                s._change_state(state.DISCONNECTED)

                self.ss.remove(s)

                self._logger.debug(f"#{id(s)} terminated")

            for sock in self.sockets:
                if sock in fds:
                    self._accept(sock)
                    fds.remove(sock)

            for fd in fds:
                if fd not in self.fd:
                    continue

                s = self.lookup_session(fd)
                bname = 'client' if fd is s.client else 'upstream'

                try:
                    data = fd.recv(65535)
                except Exception as e:
                    self._logger.debug(f"#{id(s)}, {bname} lost connection: {e}")
                    self._handle_socket_disconnect(fd, e)
                    continue

                if len(data) < 1:
                    self._logger.debug(f"#{id(s)}, {bname} disconnected")
                    self._handle_socket_disconnect(fd, None)
                    continue

                if fd is s.client:
                    #self._logger.debug(f"#{id(s)} client -> server {round(len(data) / 1000, 2)}Kb")
                    hr = None

                    try:
                        hr = s.serverbound(data)
                    except Exception as e:
                        self._logger.error(f"Exception in {s.serverbound}: {e}")

                    if isinstance(hr, bytes):
                        data = hr

                    elif hr is Reject:
                            continue

                    elif hr is not Pass and hr is not None:
                        self._logger.error(F"#{id(s)} ServerBound handler returned unidentified type! {hr.__class__}")

                    try:
                        s.server.sendall(data)
                    except Exception as e:
                        self._logger.debug(f"#{id(s)} Upstream dropped connection in the middle of data transmission process")
                        self._handle_socket_disconnect(s.server, e)

                else:
                    #self._logger.debug(f"#{id(s)} server -> client {round(len(data) / 1000, 2)}Kb")
                    hr = None

                    try:
                        hr = s.clientbound(data)
                    except Exception as e:
                        self._logger.error(f"Exception in {s.clientbound}: {e}")                        

                    if isinstance(hr, bytes):
                        data = hr

                    elif hr is Reject:
                            continue

                    elif hr is not Pass and hr is not None:
                        self._logger.error(F"#{id(s)} ClientBound handler returned unidentified type! {hr.__class__}")

                    try:
                        s.client.sendall(data)
                    except Exception as e:
                        self._logger.debug(f"#{id(s)} Client dropped connection in the middle of data transmission process")
                        self._handle_socket_disconnect(s.client, e)

        self._logger.debug(f"Stop polling")
