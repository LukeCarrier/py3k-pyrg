#!/usr/bin/env python
"""pyrg - colorized Python's UnitTest Result Tool"""
from ConfigParser import ConfigParser
from subprocess import Popen, PIPE
from select import poll, POLLIN
import sys
import re
import os

__version__ = '0.2.1'
__author__ = 'Hideo Hattroi <hhatto.jp@gmail.com>'
__license__ = 'NewBSDLicense'

PRINT_COLOR_SET = {
        'ok': '[32m%s[0m',
        'fail': '[31m%s[0m',
        'error': '[33m%s[0m',
        'function': '[36m%s[0m',
}
COLOR_MAP = {
        'black': '[30m%s[0m',
        'red': '[31m%s[0m',
        'green': '[32m%s[0m',
        'yellow': '[33m%s[0m',  # TODO:fail??
        'blue': '[34m%s[0m',
        'magenta': '[35m%s[0m',
        'cyan': '[36m%s[0m',
        'white': '[37m%s[0m',
        }


def parse_result_line(line):
    """parse to test result when fail tests"""
    err = False
    fail = False
    if 'errors' in line:
        err = True
    if 'failures' in line:
        fail = True
    if err and fail:
        f = line.split('=')[1].split(',')[0]
        e = line.split('=')[2].split(')')[0]
        result = "(%s=%s. " % (PRINT_COLOR_SET['fail'] % "failures",
                               PRINT_COLOR_SET['fail'] % f)
        result += "%s=%s)" % (PRINT_COLOR_SET['error'] % "errors",
                              PRINT_COLOR_SET['error'] % e)
    elif fail and not err:
        l = line.split('=')[1].split(')')[0]
        result = "(%s=%s)" % (PRINT_COLOR_SET['fail'] % "failures",
                              PRINT_COLOR_SET['fail'] % l)
    elif err and not fail:
        l = line.split('=')[1].split(')')[0]
        result = "(%s=%s)" % (PRINT_COLOR_SET['error'] % "errors",
                              PRINT_COLOR_SET['error'] % l)
    return PRINT_COLOR_SET['fail'] % "FAILED" + " %s" % result


def parse_lineone(line):
    """parse to test result line1"""
    results = []
    line = line.strip()
    for char in line:
        if '.' == char:
            results.append(PRINT_COLOR_SET['ok'] % ".")
        elif 'E' == char:
            results.append(PRINT_COLOR_SET['error'] % "E")
        elif 'F' == char:
            results.append(PRINT_COLOR_SET['fail'] % "F")
        else:
            results.append(char)
    return "".join(results)


def coloring_method(line):
    """colorized method line"""
    return PRINT_COLOR_SET['function'] % line


def parse_unittest_result(lines):
    """parse test result"""
    results = []
    err = re.compile("ERROR:")
    fail = re.compile("FAIL:")
    ok = re.compile("OK")
    failed = re.compile("FAILED")
    results.append(parse_lineone(lines[0]) + '\n')
    for line in lines[1:]:
        if ok.match(line):
            result = PRINT_COLOR_SET['ok'] % "OK"
        elif failed.match(line):
            result = parse_result_line(line)
        elif fail.match(line):
            result = "%s:%s" % (PRINT_COLOR_SET['fail'] % "FAIL",
                                coloring_method(line[5:]))
        elif err.match(line):
            result = "%s:%s" % (PRINT_COLOR_SET['error'] % "ERROR",
                                coloring_method(line[6:]))
        else:
            result = line
        results.append(result)
    return "".join(results)


def get_configfile_path():
    """get $HOME/.pyrgrc path"""
    return "/home/%s/.pyrgrc" % (os.getlogin())


def set_configration():
    """setting to printing color map"""
    filename = get_configfile_path()
    if not os.path.exists(filename):
        print "default configration"
        return
    configure = ConfigParser()
    configure.read(filename)
    for item in configure.items('color'):
        PRINT_COLOR_SET[item[0]] = COLOR_MAP[item[1]]
    return


def main():
    """execute command line tool"""
    set_configration()
    if sys.argv[1:]:
        p = Popen(['python', sys.argv[1]], stdout=PIPE, stderr=PIPE)
        r = p.communicate()[1]
        print parse_unittest_result(r.splitlines(1))
    else:
        poller = poll()
        poller.register(sys.stdin, POLLIN)
        pollret = poller.poll(1)
        if len(pollret) == 1 and pollret[0][1] & POLLIN:
            print parse_unittest_result(sys.stdin.readlines())
        else:
            print __doc__
            print "version:", __version__
            print "usage: pyrg pythontest.py"
            print "       python pythontest.py |& pyrg"
            print ""

if __name__ == '__main__':
    sys.exit(main())
