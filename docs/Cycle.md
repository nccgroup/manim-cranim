
{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/CycleExample1.mp4" type="video/mp4"> </video>
{:/nomarkdown}

```python
class CycleExample1(Scene):
    def construct(self):
        box = ByteBox(0)
        self.add(box)
        self.wait(0.5)
        self.play(Cycle(box, range(256)))
        self.wait(0.5)
```
