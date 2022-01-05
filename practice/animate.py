import sys
from heap import BinaryHeap
from manim import *

config.preview = True
config["preview"] = True
f = open(sys.argv[1], "r")
instance = None
for i, c in enumerate(f.readlines()):
    command = c.strip().split(' ')
    if command[0].isdigit():
        instance = BinaryHeap([int(num) for num in command])
        instance.construct(command)
    elif (command[0] == 'build' and len(command) == 2) or command[0] == 'extract' or (command[0] == 'insert' and len(command) == 2):
        instance.construct(command)
    else:
        print('Error: input is invalid')
        
        
