import sys
from heap import BinaryHeap


f = open(sys.argv[1], "r")
scene = None
for i, c in enumerate(f.readlines()):
    command = c.strip().split(' ')
    if command[0].isdigit():
        scene = BinaryHeap([int(num) for num in command])
        scene.construct(command)
    elif (command[0] == 'build' and len(command) == 2) or command[0] == 'extract' or (command[0] == 'insert' and len(command) == 2):
        scene.construct(command)
    else:
        print('Error: input is invalid')

# Use FFMPEG to combine partial videos      
scene.renderer.scene_finished(scene)  

