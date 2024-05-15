
![PaddingBlockExample1](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/PaddingBlockExample1.mp4)

```python
class PaddingBlockExample1(Scene):
    def construct(self):
        #global pb
        pb = PaddingBlock(bytes(15))
        self.add(pb)
        self.wait(0.5)
        for i in (14, 13, 12):
            self.play(Rewrite(pb, bytes(i)))
            self.wait(0.25)
        for i in range(11, 0, -1):
            pb.rewrite(bytes(i))
            self.wait(0.25)
        pb.rewrite(bytes(0))
        self.wait()
        self.play(FadeOut(pb))
```

-----

![PaddingBlockExample2](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/PaddingBlockExample2.mp4)

```python
class PaddingBlockExample2(Scene):
    def construct(self):
        pb = PaddingBlock(bytes(6))
        self.add(pb)
        self.wait(1)
        self.play(Rewrite(pb, bytes(6), padfunc=lambda l: b'\x00'*l))
        self.wait(0.17)
        self.play(Wiggle(pb[5:7], n_wiggles=17, run_time=4))
        self.play(Rewrite(pb, bytes(6), padfunc=lambda l: b'\x80' + b'\x00'*(l-1)))
        self.wait(1)
```

-----

![PaddingBlockExample3](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/PaddingBlockExample3.mp4)

```python
class PaddingBlockExample3(Scene):
    def construct(self):
        self.add(Point(), Point(), Point(), Point())
        block = PaddingBlock(
            [None]*3,  # ensure message bytes are blank
            c_pad=C_BOX_BG,
            padfunc=lambda l: [None]*l   # set padding bytes to None
        )

        # get local references (this is ugly - how could we clean it up?)
        braces = block.get_braces(pad_text="?")
        msg_brace, pad_brace, blk_brace = braces.msg_brace, braces.pad_brace, braces.blk_brace
        msg_text, pad_text, blk_text = braces.msg_text, braces.pad_text, braces.blk_text

        # introduce message bytes
        self.play(
            FadeIn(block.boxes[:3]),
            FadeIn(msg_brace, msg_text, shift=DOWN)
        )
        self.wait(0.5)

        # introduce block
        self.play(
            FadeIn(block.boxes[3:]),
            FadeIn(blk_brace, blk_text, shift=UP),
        )
        self.play(
            FadeIn(pad_brace, pad_text, shift=DOWN)  # but wait - what's this?
        )
        self.wait(0.5)

        # reveal: padding!
        block.c_pad=PURPLE
        self.play(
            Rewrite(block, [None]*3),
            #pad_text.animate.become(pad_brace.get_text("Padding").set_color(C_EDGE))
            Transform(braces, block.get_braces())
        )

        # try changing the message size and moving the braces accordingly
        for size in (5, 15, 8):
            self.wait(0.5)
            self.play(
                Rewrite(block, [None]*size),
                Transform(braces, block.get_braces())
            )

        self.wait(0.5)
        self.play(FadeOut(block, braces))
        self.wait(0.5)
```

-----

![BoxLenExample2](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/BoxLenExample2.mp4)

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
