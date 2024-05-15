
![BendyArrowExample1](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/BendyArrowExample1_ManimCE_v0.18.1.png)

```python
class BendyArrowExample1(Scene):
    def construct(self):
        boxes = VGroup(*[ByteBox(i, C_PT) for i in range(7)]).arrange_in_grid(buff=1.5)
        self.add(boxes)

        self.add(BendyArrow(boxes[0], DOWN, boxes[4], UP))
        arrow = BendyArrow(boxes[1], RIGHT, boxes[5], LEFT)
        self.add(arrow)

        # these arrows' paths are arbitrary, but i think they look neat
        # directional arguments indicate where to come out of (point into) the source (destination)
        self.add(
            BendyArrow(boxes[0], DOWN, boxes[4], UP),
            BendyArrow(boxes[4], DOWN, boxes[6], RIGHT),
            BendyArrow(boxes[5], DOWN, boxes[6], RIGHT),
            BendyArrow(boxes[6], UP, boxes[3], DOWN),
            BendyArrow(boxes[1], RIGHT, boxes[5], LEFT),
            BendyArrow(boxes[5], UP, boxes[2], DOWN),
        )
```
