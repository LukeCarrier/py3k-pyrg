#!/usr/bin/env python
from subprocess import *
import sys
import re

__version__ = '0.1.0'
__author__ = 'Hideo Hattroi <syobosyobo@gmail.com>'
__license__ = 'NewBSDLicense'


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
        result = "([31mfailures[0m=[31m%s[0m, " % f
        result += "[33merrors[0m=[33m%s[0m)" % e
    elif err and not fail:
        l = line.split('=')[1].split(')')[0]
        result = "([31mfailures[0m=[31m%s[0m)" % l
    elif not err and fail:
        l = line.split('=')[1].split(')')[0]
        result = "([33merrors[0m=[33m%s[0m)" % l
    return "FAILED " + result

def parse_lineone(line):
    result = []
    for l in line:
        if '.' == l:
            result.append("[32m.[0m")
        elif 'E' == l:
            result.append("[33mE[0m")
        else:
            result.append("[31mF[0m")
    return "".join(result)

def parse_unittest_result(lines):
    result = []
    err = re.compile("ERROR:")
    fail = re.compile("FAIL:")
    ok = re.compile("OK")
    failed = re.compile("FAILED")
    lines = lines.split('\n')
    result.append(parse_lineone(lines[0]))
    for line in lines[1:]:
        if ok.match(line):
            r = "[32mOK[00m\n"
        elif failed.match(line):
            r = parse_result_line(line)
        elif fail.match(line):
            r = "[31mFAIL[00m%s" % line[4:]
        elif err.match(line):
            r = "[33mERROR[00m%s" % line[5:]
        else:
            r = line
        result.append(r)
    return "\n".join(result)

def main():
    if sys.argv[1:]:
        p = Popen(['python', sys.argv[1]], stdout=PIPE, stderr=PIPE)
        r = p.communicate()[1]
        print parse_unittest_result(r)
    else:
        print parse_unittest_result(sys.stdin.read())


if __name__ == '__main__':
    main()

