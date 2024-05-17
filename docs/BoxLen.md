
{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/BoxLenExample1.mp4" type="video/mp4"> </video>
{:/nomarkdown}

```python
class BoxLenExample1(Scene):
    def construct(self):
        box = BoxLen("2^8")
        self.add(box)  # argument can be str, int, or anything else accepted by MathTex
        print(self.mobjects)
        self.play(box.update_rhs("256", transform=TextRewrite))
        print(self.mobjects)
```

-----

{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/BoxLenExample2.mp4" type="video/mp4"> </video>
{:/nomarkdown}

```python
class BoxLenExample2(Scene):
    def construct(self):
        pad_blk = PaddingBlock()
        msg_len = BoxLen(0)
        pad_len = BoxLen(16, c_box=C_PAD)

        self.add(
            pad_blk,
            msg_len.next_to(pad_blk, DOWN*2).align_to(pad_blk, LEFT),
            pad_len.next_to(pad_blk, DOWN*2).align_to(pad_blk, RIGHT)
        )

        dec = lambda a, b: AnimationGroup(FadeOut(a, shift=0.2*UP), FadeIn(b, shift=0.2*UP))
        inc = lambda a, b: AnimationGroup(FadeOut(a, shift=0.2*DOWN), FadeIn(b, shift=0.2*DOWN))

        for i in range(1, 16):
            self.play(
                Rewrite(pad_blk, bytes(i)),
                msg_len.update_rhs(i, transform=inc),
                pad_len.update_rhs(16-i, transform=dec),
                run_time=0.8
            )
            self.wait(0.2)
```
