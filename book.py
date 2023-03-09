#!/bin/python3
import sounder
import sys
import random
import threading
import queue
import time
import argparse

#levels = "KM U R E S N A P T L W I . J Z = F O Y , V G 5 / Q 9 2 H 3 8 B ? 4 7 C 1 D 6 0 X".split()
levels = 'ETANIM DSOURC KPBGWL QHFY ZVXJ 12345 67890'.split()


parser = argparse.ArgumentParser(
    prog = 'Morse code',
    description = 'A program to practice morse code',
)

parser.add_argument('-d', '--dot', default=0.040)
parser.add_argument("-s", "--charset", default="")
parser.add_argument('-c', '--count', default=5)
parser.add_argument('-f', '--farnsworth', default=1)
parser.add_argument('text')

args = parser.parse_args()
print("\x1b\x5b\x48\x1b\x5b\x32\x4a")
sounder.sound(f'h  ', float(args.dot), float(args.farnsworth))

remove = "[]{}(),.-~\n\t"

for word in args.text.split(" "):
    for char in remove:
        word = word.replace(char, "")
    print("\x1b\x5b\x48\x1b\x5b\x32\x4a")
    print(word)
    sounder.sound(f'{word}   ', float(args.dot), float(args.farnsworth))
