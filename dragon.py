#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os.path
import fcntl


class Dragon(object):

    class Error(Exception):
        pass

    def compile(self, src):
        self.src = src
        self.jmptbl = {}
        stack = []
        memptr = 0

        for i in range(0, len(self.src)):
            if self.src[i] == 'A':
                stack.append(i)
            elif self.src[i] == 'G':
                if len(stack) < 1:
                    raise self.Error(u'Aが足りません')
                j = stack.pop()
                self.jmptbl[j] = i
                self.jmptbl[i] = j
            elif self.src[i] == '>':
                memptr += 1
            elif self.src[i] == '<':
                memptr -= 1

        if 0 < len(stack):
            raise self.Error(u'Gが足りません')

    def execute(self):
        mem = [0]
        srcptr = memptr = 0

        while srcptr < len(self.src):
            if self.src[srcptr] == 'D':
                mem[memptr] += 1
            elif self.src[srcptr] == 'R':
                mem[memptr] -= 1

            elif self.src[srcptr] == 'A':
                if mem[memptr] == 0:
                    srcptr = self.jmptbl[srcptr]
            elif self.src[srcptr] == 'G':
                if 0 < mem[memptr]:
                    srcptr = self.jmptbl[srcptr]

            elif self.src[srcptr] == 'O':
                sys.stdout.write((chr(mem[memptr])))
                sys.stdout.flush()
            elif self.src[srcptr] == 'N':
                sys.stdout.write('>>> ')
                sys.stdout.flush()
                _input = sys.stdin.read()
                if len(_input) < 1:
                    raise self.Error(u'入力がありません')

                mem[memptr] = ord(_input[0])
                sys.stdout.write('\n')
                sys.stdout.flush()

            elif self.src[srcptr] == '>':
                memptr += 1
                if not memptr < len(mem):
                    mem.append(0)
            elif self.src[srcptr] == '<':
                memptr -= 1

            srcptr += 1


def main():
    dragon = Dragon()
    if 1 < len(sys.argv):
        if os.path.isfile(sys.argv[1]):
            try:
                with open(sys.argv[1], 'r') as f:
                    fcntl.fcntl(f.fileno(), fcntl.LOCK_SH)
                    src = f.read()
                    fcntl.fcntl(f.fileno(), fcntl.LOCK_UN)
                dragon.compile(src)
            except Dragon.Error, inst:
                print inst
            else:
                dragon.execute()
                print
            finally:
                exit(1)

        else:
            print u"Not Found Such File"
            exit(1)

    while True:
        try:
            dragon.compile(raw_input())
        except Dragon.Error, inst:
            print inst
        else:
            dragon.execute()


if __name__ == '__main__':
    main()
