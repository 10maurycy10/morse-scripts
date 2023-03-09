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

parser.add_argument('level', nargs='*')
parser.add_argument('-d', '--dot', default=0.060)
parser.add_argument("-s", "--charset", default="")
parser.add_argument('-c', '--count', default=5)
parser.add_argument('-f', '--farnsworth', default=3)

args = parser.parse_args()

if len(args.charset) > 0:
    levels = args.charset.split()

sounder_queue = queue.Queue()

def sounder_thread():
    """
    Background thread that calls the (blocking) sounder.sound foucntion
    """
    sounder.sound("", 0, 0)
    while True:
        s = sounder_queue.get()
        sounder.sound(s, float(args.dot), float(args.farnsworth))

def edit_distance(a,b):
    """
    Todo, find location of errors
    """
    # Cache results by length in a 2d array.
    array = [[0 for e in range(len(b)+1)] for i in range(len(a)+1)]
    # Assuming all computations for less than the current prams.
    def compute(len_a, len_b):
        # Trival case, seqence of insertions/deletions
        if len_a == 0:
            return len_b
        if len_b == 0:
            return len_a
        # No change
        if a[len_a - 1] == b[len_b - 1]:
            return array[len_a - 1][len_b - 1]
        else:
            return min(array[len_a - 1][len_b], array[len_a][len_b - 1], array[len_a-1][len_b-1]) + 1
    # Starting for the low lengths, fill out the array.
    for len_a in range(len(a) + 1):
        for len_b in range(len(b) + 1):
            array[len_a][len_b] = compute(len_a, len_b)
    return array[len(a)][len(b)]

if len(args.level) != 0:
    level = int(args.level[0])
    if level > len(levels) or level <= 0:
        print("Invalid level")
        exit(1)
    # Initalize sounder thread
    sound = threading.Thread(target=sounder_thread, daemon=True)
    sound.start()
    time.sleep(1)
    
    # Setup charset
    level = list("".join(levels[level-1]))

    # Show morse code table for reference
    for c in level:
        print(f"{c}: {sounder.LATIN_TO_MORSE[c]}")
    
    # Randomly generate seqence of charaters and send to sounder thread
    chars = random.choices(level, k=int(args.count))
    print(f"Playing {args.count} characters")
    sounder_queue.put("".join(chars))
    
    # Prompt user for input
    entered = input("Please enter charaters: ").strip().upper()
    
    total = len(chars)
    errors = edit_distance(entered, "".join(chars))
    correct = total - errors

    print(f"Entered: {entered}")
    print(f"Sounded: {''.join(chars)}")

    if total > 0:
        print(f"Errors {errors}/{total}")
        percentage_correct = correct / total * 100
        print(f"{int(percentage_correct)}% correct")
else:
    print("Levels:")
    for (number,level) in enumerate(levels):
        print(f"{number+1}:\t"," ".join(level))
    print("Nothing to do, try passing a level. (1?)")
    print("Koch style training can be done by starting with 1 and increasing when you reach ~90%.")
    print("Farnsworth can be done by setting level to max and decreasing --farnsworth over time.")
