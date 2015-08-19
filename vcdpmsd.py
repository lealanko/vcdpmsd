import argparse
import signal
import sys
import time
import xcb
from xcb.dpms import DPMSMode
import xcb.xproto

from sh import tvservice

def main_iteration(dpms, cfg):
    def display_required():
        reply = dpms.Info().reply()
        # We can only really support the DPMS "off" mode.
        return reply.state == 0 or reply.power_level != xcb.dpms.DPMSMode.Off

    while display_required():
        time.sleep(cfg.interval)

    tvservice(off=True)

    try:
        while not display_required():
            time.sleep(cfg.interval)
    finally: # Restore even when killed
        tvservice(preferred=True) # TODO: support non-preferred HDMI modes
        reply = dpms.Info().reply()
        dpms.Disable() # For some reason this is the best way to restore X
        if reply.state != 0:
            dpms.Enable()

def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Display Power Management controller for VideoCore."
    )
    p.add_argument('-d', '--display', help="X display to poll"),
    p.add_argument('-i', '--interval', help="Poll interval in seconds",
                   default=1.0, type=float)
    return p.parse_args(argv)
            
def main():
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
    cfg = parse_args(sys.argv[1:])
    conn = xcb.connect(cfg.display)
    dpms = conn(xcb.dpms.key)

    while True:
        main_iteration(dpms, cfg)
