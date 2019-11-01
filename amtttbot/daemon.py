"""Generic linux daemon base class for python 3.x."""

import atexit
import os
import sys


def fork():
    """Do fork"""
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('fork failed: {0}\n'.format(err))
        sys.exit(1)


class Daemon(object):
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        """UNIX double fork mechanism."""
        fork()

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        fork()

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        sin = open(os.devnull, 'r')
        sout = open(os.devnull, 'a+')
        serr = open(os.devnull, 'a+')

        os.dup2(sin.fileno(), sys.stdin.fileno())
        os.dup2(sout.fileno(), sys.stdout.fileno())
        os.dup2(serr.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        self.writepid()

    def writepid(self):
        """Save the pid"""
        with open(self.pidfile, 'w') as pidfile:
            pidfile.write(str(os.getpid()))

    def delpid(self):
        """Remove pid file"""
        os.remove(self.pidfile)

    def start(self):
        """Run daemon"""
        self.daemonize()
        self.run()

    def run(self):
        """You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized."""
