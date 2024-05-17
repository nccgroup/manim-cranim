# Example Gallery


##  Showcase

{::nomarkdown}
<video controls allowfullscreen width=100%>
  <source src="renders/ECBvsCBCExample.mp4" type="video/mp4">
</video>
{:/nomarkdown}

```python
class ECBvsCBCExample(Scene):
    def construct(self):
        ecb = ECBBlocks(bytes(16*5), direction=RIGHT, zoom=0.36)
        cbc = CBCBlocks(bytes(16*5))
        cbc.zoom(ecb.width / cbc.width)

        for e, c in zip(ecb, cbc):
            e.align_to(c, DOWN)

        self.add(
            ecb.move_to(LEFT*(32/9)),
            cbc.move_to(RIGHT*(32/9)).align_to(ecb, DOWN),
            DashedLine(3*UP, 3*DOWN, color=C_STROKE),
        )

        ecb_block = ecb[2]
        cbc_block = cbc[2]

        self.play(LaggedStart(
            FocusOn(ecb_block.pt[0].get_edge_center(LEFT)),
            Rewrite(ecb_block, b'\xff'+bytes(15)),
            lag_ratio=0.7
        ))
        self.wait()
        self.play(LaggedStart(
            FocusOn(cbc_block.pt[0].get_edge_center(LEFT)),
            Rewrite(cbc_block, b'\xff'+bytes(15)),
            lag_ratio=0.7
        ))
```


