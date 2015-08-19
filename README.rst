vcdpmsd
=======

This is a simple daemon that makes X11's standard display power
management work on Raspberry Pi. It polls the X server for the current
DPMS state and toggles the VideoCore HDMI output accordingly. This is
done with the ``tvservice`` program included with the Raspberry Pi
firmware.


Requirements
------------

The following PiPy packages are required:

* `sh` - Raspbian package ``python-sh``
* `xpyb` - Raspbian package ``python-xpyb``

Also, the ``tvservice`` program is required. This is typically installed
in ``/opt/vc/bin`` along with other VideoCore control utilities.


Installation
------------

Standard setuptools installation:

* for the current user: ``./setup.py install --user``
* globally: ``sudo ./setup.py install``  

  
Usage
-----

Make sure that ``tvservice`` is in path and run: ``vcdpmsd &``.
Typically you might want to include this in your X session startup
script. To stop the program, kill the process with ``SIGTERM``.

The following options are provided:

* ``-d``, ``--display``: The X display to poll. Defaults to
  ``$DISPLAY``.
* ``-i``, ``--interval``: The DPMS polling interval in seconds.
  Defaults to 1.

To check that everything works, run ``xset dpms force off``. The display
should now turn off. Press a key and the display should be restored. If
the monitor turns on but the screen stays blank, you may have to change
to another virtual terminal and back (typically Ctrl+Alt+F1,
Ctrl+Alt+F7). Please report if this happens.


Issues
------

* The HDMI output is always restored in the "preferred" mode, even if it
  was in some other mode when the display was turned off.


Todo
----

* Support other HDMI modes besides ``--preferred``. This is a bit of
  work since ``tvservice`` uses different syntaxes for querying and
  setting the mode.

* Use ``libvchostif`` directly instead of ``tvservice``. Currently not
  feasible because ``libvchostif`` is usually only distributed as a
  static library.

* Use ``xcffib`` instead of ``xpyb``. Not reasonable until ``xcffib`` is
  included in Raspbian.


Contributing
------------

Bugs, suggestions, pull requests etc. can be reported on the project's
site at https://github.com/lealanko/vcdpmsd


License
-------

This program is distributed under the MIT license, included in the file
``LICENSE``.


Author
------

Lauri Alanko <la@iki.fi>
