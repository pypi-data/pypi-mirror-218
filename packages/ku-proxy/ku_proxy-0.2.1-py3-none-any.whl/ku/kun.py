"""
    Kun
    ===
    Powerful fronted for ku-proxy
"""

import argparse
import logging
from random import randint
from re import findall
from socket import gaierror, getaddrinfo
from time import sleep, time
from typing import Tuple

from ku import ku, tcpsession
from ku import version as ku_version

from .util import CustomFormatter
import statistics, curses
import traceback

reset = "\u001b[0m"

version = '0.1'

banner = \
f"""
 __    __                    
|  \  /  \                   
| $$ /  $$__    __  _______  
| $$/  $$|  \  |  \|       \ 
| $$  $$ | $$  | $$| $$$$$$$\\
| $$$$$\ | $$  | $$| $$  | $$
| $$ \$$\| $$__/ $$| $$  | $$
| $$  \$$ \$$    $$| $$  | $$
 \$$   \$$ \$$$$$$  \$$   \$$ v{version}
"""

def _host_parse(host: str) -> Tuple[str, int]:
    
    IPv6_PORT = r"^(\[[\d\D]{1,}\]):([0-9]{1,5})$"
    IPv4_PORT = r"^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}):([0-9]{1,5})$"
    TLD_PORT = r"^([A-z0-9._-]{1,}):([0-9]{1,5})$"

    PATTERNS = [IPv6_PORT, IPv4_PORT, TLD_PORT]
    for pattern in PATTERNS:
        i = findall(pattern, host)
        if i:
            if pattern is IPv6_PORT:
                proto = 23
            elif pattern is IPv4_PORT:
                proto = 2
            else:
                proto = -1

            return proto, i[0][0], int(i[0][1])
    raise RuntimeError('Failed to parse host string', host)

def _resolve_host(host: str) -> Tuple[Tuple[int, str]]:
    protocol = ku._resolve_proto(host)
    if not protocol:
        raise RuntimeError("Failed to define protocol(ipv4 or ipv6) for host:", host)
    elif protocol == -1:
        try:
            host_addresses = getaddrinfo(host, 7)
        except gaierror:
            raise RuntimeError("Failed to resolve hostname:", host)
        return [(addr[0], addr[4][0]) for addr in host_addresses]
    return [[protocol, host]]

def genrancol(brightness: int = 1) -> Tuple[int, int, int]:
    cs = randint(0, 255), randint(0, 255), randint(0, 255)
    while cs[0] + cs[1] + cs[2] < 250:
        cs = randint(0, 255), randint(0, 255), randint(0, 255)
    r, g, b = (min(255, int(c * brightness)) for c in cs)
    return r, g, b

def ansicol(r: int, g: int ,b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"

TOTAL = 0

def mb(len: int) -> str:
    val = round(len / 1024**2, 2)
    if not val:
        val = round(len / 1_000_000, 7)

    return str(val)

class sess(tcpsession):
    def __init__(self, client, server, proxy):
        self.id = id(self)   
        self.color = ansicol(*genrancol(1.17))

        print(self.color, F"#{self.id} {client.getpeername()}->{client.getsockname()}::{server.getsockname()}->{server.getpeername()}", reset)

    def clientbound(self, data):
        global TOTAL     
        TOTAL += len(data)
        print(self.color, F"#{self.id} server->client  {len(data)}", reset)
    
    def serverbound(self, data):        
        global TOTAL
        TOTAL += len(data)
        print(self.color, F"#{self.id} client->server  {len(data)}", reset)
    
    def connection_made(self):
        print(self.color, F"#{self.id} connection_made", reset)
    
    def connection_lost(self, side, err):
        side = 'client' if side is self.client else 'server' if side is not None else 'proxy'
        print(self.color, F"#{self.id} connection_lost by {side} due to {err}", reset)
    
class transit(tcpsession):

    TX = 0
    RX = 0

    def clientbound(self, data):
        global TOTAL     
        self.RX += len(data)
        TOTAL += len(data)

    def serverbound(self, data):        
        global TOTAL
        self.TX += len(data)
        TOTAL += len(data)
                
    def __repr__(self) -> str:
        ttime = ".".join([i.zfill(2) for i in str(round((time() - self.estab_time), 2)).split('.')])
        output = f"#{id(self)}[{ttime}] / {self.client.getpeername()} / RX:{mb(self.RX)}Mb TX: {mb(self.TX)}Mb"
        return output
    
def entry_point():
    pcolor = ansicol(*genrancol(1.37))
    print(pcolor, banner[1:], reset, sep='')

    parser = argparse.ArgumentParser(description="Powerful fronted for ku-proxy")
    parser.add_argument("-v", action="store_true", help="If passed, enabling verbose logging")
    parser.add_argument("-l", action='append', help="Proxy listen addr (allowed multiple and dualstack hostnames) (enclose ipv6 like [::1])", metavar="localhost:65535", required=True)
    parser.add_argument("-u", help="Proxy upstream server addr", metavar="localhost:8000", required=True)
    parser.add_argument("-7", help="Tells proxy to upstream over IPv6", action="store_true", dest='u6')
    parser.add_argument("-ll", action="store_true", help="If passed, enables low level debug logging (ku-proxy debug)")
    parser.add_argument("-mc", type=int, help="Maximum of parralel clients (connection over the limit will be refused)", default=-1, metavar="15")
    parser.add_argument("--transit", action="store_true", help="If passed, enables transit (no session orientated) displaying")
    args = parser.parse_args()

    logger = logging.getLogger("[")
    logger.setLevel(logging.DEBUG if args.v else logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter('[%(asctime)s] [%(levelname)s] %(name)s:  %(message)s', pcolor))
    logger.addHandler(stdout_handler)

    logging.getLogger("ku.devel").addHandler(stdout_handler)
    logging.getLogger("ku.devel").setLevel(logging.DEBUG if args.ll else logging.WARNING)

    logger.info(f"Running kun v{version} (ku v{ku_version})")

    listen = []
    for addr in args.l:
        ler = _host_parse(addr)
        addreses = _resolve_host(ler[1])
        for addr in addreses:
            addr = f"[{addr[1]}]" if addr[0] == 23 else addr[1]
                
            listen.append(addr)
            listen.append(ler[2])
            logger.info(f"\u001b[97mListening \u001b[92m-> \u001b[97m{addr}:{ler[2]}")

    upstream = _host_parse(args.u)
    logger.info(f"\u001b[97mUpstream {ansicol(120, 120, 120)}({'v6' if upstream[0] is 23 else 'v6' if (args.u6 and upstream[0] == -1) else 'v4'}) \u001b[92m-> \u001b[97m{upstream[1]}:{upstream[2]}")

    logger.info("Starting...")
    proxy = ku(listen, upstream[1:], transit if args.transit else sess, maxcon = args.mc, upstream_6 = args.u6)
    logger.info("Started")

    if args.transit:
        def transit_screen(screen):

            curses.start_color()
            curses.curs_set(0)
            screen.timeout(int(1000 / 25))
            fps = [0]
            button = 0

            while 7:
                if button == 99:
                    proxy.pause = not proxy.pause

                render_begin = time()
                    
                screen.clear()
                height, width = screen.getmaxyx()

                # Banner
                curses.init_pair(1, 8, curses.COLOR_BLACK)
                screen.addstr(0, 0, banner[1:], curses.color_pair(1))

                # Listen
                curses.init_pair(3, 12, curses.COLOR_BLACK)                
                for k, i in enumerate(range(0, len(listen), 2)):
                    screen.addstr(k + 2, width - 36, f"Listening -> {listen[i]}:{listen[i+1]}"[:36], curses.color_pair(3))

                # Upstream
                curses.init_pair(4, 8, curses.COLOR_BLACK)
                screen.addstr(k + 4, width - 36, f"Upstream ({'v6' if upstream[0] is 23 else 'v6' if (args.u6 and upstream[0] == -1) else 'v4'}) -> {upstream[1]}:{upstream[2]}", curses.color_pair(4))

                # Sessions
                curses.init_pair(6, 13, curses.COLOR_BLACK)
                screen.addstr(10, 0, f"Active sessions [{len(proxy.ss)}]:", curses.color_pair(6))

                sess_offset = 11
                for i, session in enumerate(proxy.ss):
                    curses.init_pair(5, 1, curses.COLOR_BLACK)
                    screen.addstr(sess_offset + i, 5, str(session), curses.color_pair(5))

                # Actionbar
                fps_fix = f"FPS: {round(statistics.median(fps), 2)}".ljust(10)
                state = f"State: {'PAUSED' if proxy.pause else 'RUNNING' if proxy.alive else 'STOPP'}"
                actionbar = f"{fps_fix}, {state}, {button}, Total transfered: {mb(TOTAL)}Mb".ljust(width - 1)
                curses.init_pair(2, curses.COLOR_BLACK, 15)
                screen.addstr(height - 1, 0, actionbar, curses.color_pair(2))

                try:
                    screen.refresh()
                    button = screen.getch()
                except KeyboardInterrupt:
                    logger.info("Shutting down...")
                    proxy.shutdown()
                    logger.info("Exiting...")
                    break
                
                fps.append(round(1 / (time() - render_begin + 0.0001), 2))
                if len(fps) == 10:
                    del fps[0]

        try:
            curses.wrapper(transit_screen)
        except Exception as e:
            print(traceback.format_exc())
            proxy.shutdown()            

    else:
        while 7:
            try:
                if not proxy.thread.is_alive():
                    logger.warning(f"Proxy unexpectedly closed")
                    break
                sleep(0.07)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                proxy.shutdown()
                logger.info("Exiting...")
                break
