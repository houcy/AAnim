# manim-cs

## Description

This is a library for data structure animation by using a Python library called Manim.

## Installation

This library uses ManimCE (instead of ManimGL, learn differences between versions [here](https://docs.manim.community/en/stable/installation/versions.html)) To set up the environment, follow [this tutorial](https://docs.manim.community/en/stable/installation.html)

Also, you need to enable LaTeX, go to http://www.tug.org/mactex/ and download the full version of MacTeX.

## Validation

After installing, `cd practice` and try `manimgl make_image.py SquareToCircle`, if you see a window pop up which renders a blue circle, you are good to go.

## Working demo

You will need to `cd practice` first.
Heap operations: `python animate.py commands.txt`
You can customize your commands in commands.txt. However it only takes one of the four commands:

1. Create a heap by giving a list of numbers less than 15 elements, seperated by space. For example: `19 18 17 16 15 14 13 12 11`
2. Build a heap: build [min/max]. For example: `build min`
3. Extract the Min/Max: extract.
4. Insert a value and heapify: insert [integer]. For example: `insert 1`
