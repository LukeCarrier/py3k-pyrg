#!/usr/bin/env python
from subprocess import *
import sys
import re

__version__ = '0.1.1'
__author__ = 'Hideo Hattroi <syobosyobo@gmail.com>'
__license__ = 'NewBSDLicense'

OK_COLOR = "[32m%s[0m"
FAIL_COLOR = "[31m%s[0m"
ERROR_COLOR = "[33m%s[0m"

def parse_result_line(line):
    err = False
    fail = False
    if 'errors' in line:
        err = True
    if 'failures' in line:
        fail = True
    if err and fail:
        f = line.split('=')[1].split(',')[0]
        e = line.split('=')[2].split(')')[0]
        result = "(" + FAIL_COLOR % "failures" + "=" + FAIL_COLOR % f + ", "
        result += ERROR_COLOR % "errors" + "=" + ERROR_COLOR % e + ")"
    elif err and not fail:
        l = line.split('=')[1].split(')')[0]
        result = "(" + FAIL_COLOR % "failures" + "=" + FAIL_COLOR % l
    elif not err and fail:
        l = line.split('=')[1].split(')')[0]
        result = "(" + ERROR_COLOR % "errors" + "=" + ERROR_COLOR % l
    return FAIL_COLOR % "FAILED" + " %s" % result

def parse_lineone(line):
    result = []
    for l in line:
        if '.' == l:
            result.append(OK_COLOR % ".")
        elif 'E' == l:
            result.append(ERROR_COLOR % "E")
        else:
            result.append(FAIL_COLOR % "F")
    return "".join(result)

def parse_unittest_result(lines):
    result = []
    err = re.compile("ERROR:")
    fail = re.compile("FAIL:")
    ok = re.compile("OK")
    failed = re.compile("FAILED")
    result.append(parse_lineone(lines[0])+'\n')
    for line in lines[1:]:
        if ok.match(line):
            r = OK_COLOR % "OK" + "\n"
        elif failed.match(line):
            r = parse_result_line(line)
        elif fail.match(line):
            r = FAIL_COLOR % "FAIL" + line[4:]
        elif err.match(line):
            r = ERROR_COLOR % "ERROR" + line[5:]
        else:
            r = line
        result.append(r)
    return "".join(result)

def main():
    if sys.argv[1:]:
        p = Popen(['python', sys.argv[1]], stdout=PIPE, stderr=PIPE)
        r = p.communicate()[1]
        print parse_unittest_result(r.splitlines(1))
    else:
        print parse_unittest_result(sys.stdin.readlines())


if __name__ == '__main__':
    main()

