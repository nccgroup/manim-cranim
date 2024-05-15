
![CycleExample1](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/CycleExample1.mp4)

```python
class CycleExample1(Scene):
    def construct(self):
        box = ByteBox(0)
        self.add(box)
        self.wait(0.5)
        self.play(Cycle(box, range(256)))
        self.wait(0.5)
```
