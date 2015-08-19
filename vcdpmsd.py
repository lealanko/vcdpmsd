import argparse
import re
import signal
import sys
import time
import xcb
import xcb.dpms
import xcb.xproto

from sh import tvservice, vcgencmd

_status_re = re.compile(r'\[(\S+) (\S+) \((\d+)\) (?:3D (\S+))?')

def get_hdmi_state():
    line = str(tvservice(status=True))
    m = _status_re.search(line)
    if not m:
        return None

    drive, group, mode, td = m.groups()
    if td is not None:
        if group != 'CEC':
            return None
        group = "CEC_3D_" + td.replace('&', '').upper()
    return group, mode, drive

def disable_hdmi(state):
    if state is None: # Fallback, couldn't parse state string
        vcgencmd('display_power', '0')
    else: 
        tvservice(off=True)

def enable_hdmi(state):
    if state is None:
        vcgencmd('display_power', '1')
    else:
        tvservice(explicit=' '.join(state))

def main_iteration(dpms, cfg):
    def display_required():
        reply = dpms.Info().reply()
        # We can only really support the DPMS "off" mode.
        return reply.state == 0 or reply.power_level != xcb.dpms.DPMSMode.Off

    while display_required():
        time.sleep(cfg.interval)

    state = get_hdmi_state()
    disable_hdmi(state)

    try:
        while not display_required():
            time.sleep(cfg.interval)
    finally: # Restore even when killed
        enable_hdmi(state)
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
