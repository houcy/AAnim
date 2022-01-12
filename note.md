# 3 classes

## Mobject

Example: Circle(), Arrow(), Rectangle(), SurroundingRectangle(text)

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

## Animation

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

## Getter

Manim provides functions to get the position of an mobject.

- arrow = Line(start=rect.get_bottom(), end=circ.get_top())

You can also use `always_redraw(lambda : mobject)` to update the position of the mobject if it depends on another moving mobject.

- arraw2 = always_redraw(lambda: arrow)
