# Manim learning notes

Manim relies on Python’s simplicity to generate animations programmatically, making it convenient to specify exactly how each one should animate. There are three building blocks to create animation: the mathematical object (i.e., mobject), the animation, and the scene. Manim uses the object-oriented design where each of these three concepts is implemented in manim as a separate class: the Mobject, Animation, and Scene classes.

## 1. Mobject

Mobject is one of the fundamental building blocks of Manim. A mobject, such as Circle, Line, or Arrow, represents an object that can be displayed on the screen. They inherit the Mobject() class. The following code snippet creates a circle instance and adds it to the canvas in order to display it on the screen.

```
from manim import *

class CreatingMobjects(Scene):
  def construct(self):
    circle = Circle()
    self.add(circle)
```

Other examples: Circle(), Arrow(), Rectangle(), SurroundingRectangle(text)

### How to display

    ```
    Class xx(Scene):
        def construct():
            circle = Circle()
            self.add(circle)
    ```

### How to change location

- shift(): change the location from ORIGIN. Can be shifted to LEFT, RIGHT, UP, DOWN, etc. Like circle.shift(LEFT). For example, x.shift(x.get_center()\*LEFT).

- move_to(): circle.move_to(LEFT \* 2) place the circle two units left from the origin.
- next_to(): square.next_to(circle, LEFT) place the square to the left of the circle.
- align_to(): triangle.align_to(circle, LEFT) align the left border of the triangle to the left border of the circle.
  All above functions are built-in methods of specific mobject.

### How to style

Apperance

- set_stroke(): circle.set_stroke(color=GREEN, width=20)
- set_fill(): square.set_fill(YELLOW, opacity=1.0)
- set_color(): for non VMobject
- set_opacity(1)

Order

- add(): add(triangle, square, circle), triangle on bottom, circle on front

### Getter

Manim provides functions to get the position of an mobject.

- arrow = Line(start=rect.get_bottom(), end=circ.get_top())

You can also use `always_redraw(lambda : mobject)` to update the position of the mobject if it depends on another moving mobject.

- arraw2 = always_redraw(lambda: arrow)

## 2. Animation

Animation is another building block of Manim. We can add an animation by calling the play() method. We need to pass an animation object to the play() method so that the animation can be played. There are many different animation objects that we can use such as FadeIn(), Rotate(), DrawBoarderThenFill(), etc. There is another way to create an animation object which is calling animate() methods of a mobject, such as circle.animate.set_fill(WHITE), circle.animate.to_edge(UR, buff=0.5), etc. The following code snippet creates a circle instance and adds it to the canvas in order to display it on the screen.

Creating an instance of an animation action

- FadeIn(circle)
- Rotate(square, 1)
- FadeOut(square)
- Write(text)
- DrawBoarderThenFill(square)
- Create(circle)

Calling animate() methods of a mobject

- circle.animate.set_fill(WHITE)
- circle.animate.to_edge(UR, buff=0.5)

Change duration

- self.play(circle.animate.set_fill(WHITE), run_time=3)

## 3. Scene

Last but not least, Scene. Scene is the canvas that can host the above two building blocks. An object needs to inherit Scene in order to show an mobject or play animations. We can use add() or remove() to add an mobject to the scene or remove the mobject from the scene. To generate a video, we need to use the construct() method.
