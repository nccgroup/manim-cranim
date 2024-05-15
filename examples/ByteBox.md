
![ByteBoxExample1](examples/renders/ByteBoxExample1_ManimCE_v0.17.3.png)

```python
class ByteBoxExample1(Scene):
    def construct(self):
        # contents can be str, int, bytes, or None
        box_1 = ByteBox(0xf, c_fill=C_CT)  # numeric values are zero-padded as need be
        box_2 = ByteBox('0')   # length-1 strings are center-aligned
        box_3 = ByteBox('hi', c_fill=C_STROKE, c_text=C_BOX_BG)  # any string is allowed (but the box is sized to 2 chars)
        box_4 = ByteBox(None, c_fill=GRAY)  # to disable byte text, pass b=None
        self.add(VGroup(box_1, box_2, box_3, box_4).arrange_in_grid())
```

-----

![ByteBoxExample2](examples/renders/ByteBoxExample2.mp4)

```python
class ByteBoxExample2(Scene):
    def construct(self):
        box = ByteBox('aa')

        # demonstrate rewriting
        self.play(FadeIn(box))
        self.wait(0.5)
        self.play(Rewrite(box, 'bb'))

        # integer values are converted to hex and 0-padded
        for i in (1, 0x23):
            self.play(Rewrite(box, i))
            self.wait(0.2)

        # rewrite is compatible with zoom
        self.play(box.animate.zoom(6))  # zoom() is like scale(), but it also adjusts stroke_width
        self.wait(0.5)                  # so that border lines maintain their relative weight
        self.play(Rewrite(box, '4'))
        self.wait(0.5)

        # zoom state persists through .copy()
        box_2 = box.copy()
        box_3 = box.copy().rewrite('7')
        self.play(Group(box, box_2).animate.arrange(RIGHT, buff=1.2).center())
        #self.wait(0.5)

        # pass None to erase a box. it can still be re-populated at will
        self.play(Rewrite(box, None), Rewrite(box_2, None))
        self.play(LaggedStart(
            Rewrite(box, '5', c_fill=C_PT),
            Rewrite(box_2, '6', c_text=RED),
            lag_ratio=0.33
        ))
        self.play(
            ReplacementTransform(VGroup(box.box, box_2.box), box_3.box),
            ReplacementTransform(VGroup(box.text, box_2.text), box_3.text)
        )
        self.play(Rewrite(box_3, '8', c_fill=C_STROKE, c_text=C_BOX_BG))
        self.play(Rewrite(box_3, '9'))
        self.play(FadeOut(box_3, scale=1.2))
```
