# Example Gallery


[[_TOC_]]

##  Showcase


![ECBvsCBCExample](examples/renders/ECBvsCBCExample.mp4)

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

-----

![CTSExample](examples/renders/CTSExample_ManimCE_v0.17.3.png)

```python
class CTSExample(Scene):
    def construct(self):
        block_0 = CBCBlock(direction=DOWN, margin=3)
        block_1 = CBCBlock(prev=block_0, direction=DOWN, margin=3.4)
        block_2 = CBCBlock(msg=[None]*3, prev=block_1, direction=DOWN, margin=3.4, padfunc=bytes)

        block_1.remove(block_1.enc_to_ct)
        block_2.remove(block_2.enc_to_ct)
        block_2.remove(block_2.ct_to_xor)
        block_2.ct.remove(*block_2.ct[3:])

        stroke = DEFAULT_STROKE_WIDTH*0.66
        enc_to_xor = BendyArrow(block_1.enc, DOWN, block_2.xor, UP, stroke_width=stroke)
        enc_to_ct = BendyArrow(block_1.enc, DOWN, block_2.ct, UP, stroke_width=stroke, offset_ratio=0.524)
        enc_to_ct_2 = BendyArrow(block_2.enc, RIGHT, block_1.ct, LEFT, stroke_width=stroke)
        enc_to_ct_2_bg = Rectangle(width=0.12, height=0.3, stroke_opacity=0, fill_color=C_SCENE_BG, fill_opacity=1).move_to(enc_to_ct_2)

        cts = ZoomableVGroup(
            block_0, block_1, block_2,
            enc_to_xor, enc_to_ct, enc_to_ct_2_bg, enc_to_ct_2,
        ).center().zoom(0.7)

        self.add(cts)
```

-----

![SlideExample1](examples/renders/SlideExample1.mp4)

```python
class SlideExample1(Scene):
    def construct(self):
        token = list('email=foo@bar.com&uid=10&role=user')
        last_len = len(token[32:])
        pad_len = 16-last_len
        block_1 = Block(token[:16], c_fills=C_PT)
        block_2 = Block(token[16:32], c_fills=C_PT)
        block_3 = PaddingBlock(token[32:])

        ZoomableVGroup(block_1, block_2, block_3, zoom=0.8).arrange(DOWN).center()
        self.add(block_1, block_2, block_3)
        self.wait(0.5)
        self.play(
            LaggedStart(
                FadeOut(block_3[2], scale=0.5, rate_func=rate_functions.ease_in_cubic),
                FadeOut(block_3[3], scale=0.5, rate_func=rate_functions.ease_in_cubic),
                Slide(*block_1, *block_2, *block_3, start=7, stop=-14, shift=2),
                FadeIn(new_o_1 := block_1[7].copy(), scale=0.5),
                FadeIn(new_o_2 := block_1[8].copy(), scale=0.5),
                lag_ratio=0.25,
            ),
            AnimationGroup(*[Rewrite(byte, 12, C_PAD) for byte in block_3[4:]]),
            run_time=5,
        )
        self.wait()

        new_block_1 = Block.from_boxes(*block_1[:7], new_o_1, new_o_2, *block_1[7:14])
        new_block_2 = Block.from_boxes(*block_1[-2:], *block_2[:-2])
        new_block_3 = Block.from_boxes(*block_2[-2:], *block_3[:2], *block_3[4:])
        admin_block = Block(list("admin") + [11]*11, c_fills=C_PT, zoom=0.8)
        self.play(
            Group(
                new_block_1,
                admin_block,
                new_block_2,
                new_block_3,
            ).animate.arrange(DOWN).align_to(new_block_1, UP),
        )
        self.wait()
        self.play(
            admin_block.animate.move_to(new_block_2),
            new_block_2.animate.move_to(admin_block),
        )
        self.wait(0.5)
        self.play(
            Rewrite(admin_block, c_fills=[C_PT]*5+[C_PAD]*11),
            FadeOut(new_block_3),
        )
        self.wait()
```

-----

![CodeRewriteExample1](examples/renders/CodeRewriteExample1.mp4)

```python
class CodeRewriteExample1(Scene):
    def construct(self):
        kwargs = {"language": "python", "tab_width": 4, "font": "Monospace", "style": "inkpot", "background": "window", "line_spacing": 0.6, "insert_line_no": False}
        code_1 = Code("code/padding_oracle_1.py", **kwargs).scale(0.5)
        code_2 = Code("code/padding_oracle_2.py", **kwargs).scale(0.5).align_to(code_1, UL)
        self.add(code_1)
        self.wait(0.5)
        self.play(CodeRewrite(code_1, code_2))
        self.wait(0.5)
```


## BendyArrow


![BendyArrowExample1](examples/renders/BendyArrowExample1_ManimCE_v0.17.3.png)

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


## Block


![SlideExample1](examples/renders/SlideExample1.mp4)

```python
class SlideExample1(Scene):
    def construct(self):
        token = list('email=foo@bar.com&uid=10&role=user')
        last_len = len(token[32:])
        pad_len = 16-last_len
        block_1 = Block(token[:16], c_fills=C_PT)
        block_2 = Block(token[16:32], c_fills=C_PT)
        block_3 = PaddingBlock(token[32:])

        ZoomableVGroup(block_1, block_2, block_3, zoom=0.8).arrange(DOWN).center()
        self.add(block_1, block_2, block_3)
        self.wait(0.5)
        self.play(
            LaggedStart(
                FadeOut(block_3[2], scale=0.5, rate_func=rate_functions.ease_in_cubic),
                FadeOut(block_3[3], scale=0.5, rate_func=rate_functions.ease_in_cubic),
                Slide(*block_1, *block_2, *block_3, start=7, stop=-14, shift=2),
                FadeIn(new_o_1 := block_1[7].copy(), scale=0.5),
                FadeIn(new_o_2 := block_1[8].copy(), scale=0.5),
                lag_ratio=0.25,
            ),
            AnimationGroup(*[Rewrite(byte, 12, C_PAD) for byte in block_3[4:]]),
            run_time=5,
        )
        self.wait()

        new_block_1 = Block.from_boxes(*block_1[:7], new_o_1, new_o_2, *block_1[7:14])
        new_block_2 = Block.from_boxes(*block_1[-2:], *block_2[:-2])
        new_block_3 = Block.from_boxes(*block_2[-2:], *block_3[:2], *block_3[4:])
        admin_block = Block(list("admin") + [11]*11, c_fills=C_PT, zoom=0.8)
        self.play(
            Group(
                new_block_1,
                admin_block,
                new_block_2,
                new_block_3,
            ).animate.arrange(DOWN).align_to(new_block_1, UP),
        )
        self.wait()
        self.play(
            admin_block.animate.move_to(new_block_2),
            new_block_2.animate.move_to(admin_block),
        )
        self.wait(0.5)
        self.play(
            Rewrite(admin_block, c_fills=[C_PT]*5+[C_PAD]*11),
            FadeOut(new_block_3),
        )
        self.wait()
```

-----

![BlockExample1](examples/renders/BlockExample1.mp4)

```python
class BlockExample1(Scene):
    def construct(self):
        block = Block(bytes(16), c_fills=C_PT)
        self.add(block)
        self.wait()
        self.play(Rewrite(block, [0xFF]*16, [C_PT, C_CT]*8))
        self.wait()
```

-----

![BlockExample2](examples/renders/BlockExample2_ManimCE_v0.17.3.png)

```python
class BlockExample2(Scene):
    def construct(self):
        from itertools import product
        group = VGroup()
        for color, size in product((C_BOX_BG, GRAY), (8, 16, 24)):
            group.add(Block(range(size), c_fills=color, block_size=None))  # type: ignore  # TODO fix type sig
        group.arrange_in_grid(cols=1, buff=0.55)
        self.add(group)
```

-----

![BlockExample3](examples/renders/BlockExample3_ManimCE_v0.17.3.png)

```python
class BlockExample3(Scene):
    # demonstrates cranim's custom handling of characters with tails (e.g. q, y).
    # manim does not provide a built-in way of recognizing/handling descenders,
    # and so centering them will take them off the baseline. That looks awful,
    # so cranim's ByteBox automatically re-aligns them.
    def construct(self):
        from string import ascii_lowercase, ascii_uppercase, punctuation
        block_style = {"c_fills": C_PT, "block_size": None, "zoom": 0.7}
        blocks_style = {**block_style, "block_size": 32}
        lower = Block(list(ascii_lowercase), **block_style)
        upper = Block(list(ascii_uppercase), **block_style)
        text = Block(list('Mr Jock, TV quiz PhD, bags few lynx'), **block_style)
        punc = Block(list(punctuation), **block_style)
        hexes = Blocks(range(256), **blocks_style)
        blocks = Group(lower, upper, text, punc, *hexes)
        blocks.arrange(DOWN).center()
        self.add(blocks)
```


## BoxLen


![BoxLenExample1](examples/renders/BoxLenExample1.mp4)

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

![BoxLenExample2](examples/renders/BoxLenExample2.mp4)

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


## BufferToText


![BufferToTextExample1](examples/renders/BufferToTextExample1.mp4)

```python
class BufferToTextExample1(Scene):
    def construct(self):
        pt_msg = "This is a plaintext string!"
        text = Text(pt_msg).scale(0.7).shift(UP/3)
        buff = Blocks(pt_msg, c_fills=C_PT, zoom=0.7, n_cols=2, buff=1/3).shift(DOWN/3)
        self.add(buff)
        self.wait(0.5)
        self.play(BufferToText(buff, text, lag_ratio=0.05, unpad=True))
        self.wait(0.5)
```


## ByteBox


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


## CBCBlock


![CBCExample1](examples/renders/CBCExample1_ManimCE_v0.17.3.png)

```python
class CBCExample1(Scene):
    def construct(self):
        cbc = CBCBlock(zoom=0.8)
        self.add(cbc)
```

-----

![CBCExample2](examples/renders/CBCExample2_ManimCE_v0.17.3.png)

```python
class CBCExample2(Scene):
    def construct(self):
        block_1 = CBCBlock(msg=bytes(16))
        block_2 = CBCBlock(msg=bytes(), prev=block_1)
        cbc_group = ZoomableVGroup(block_1, block_2, zoom=0.55)
        self.add(cbc_group.center())
```

-----

![CBCExample3](examples/renders/CBCExample3_ManimCE_v0.17.3.png)

```python
class CBCExample3(Scene):
    def construct(self):
        block_1 = CBCBlock(msg=bytes(16), direction=DOWN)
        block_2 = CBCBlock(msg=bytes(16), prev=block_1, direction=DOWN)
        block_3 = CBCBlock(msg=bytes(12), prev=block_2, direction=DOWN)
        self.add(ZoomableVGroup(block_1, block_2, block_3, zoom=2/3).center())
```

-----

![CBCExample4](examples/renders/CBCExample4.mp4)

```python
class CBCExample4(MovingCameraScene):  # Loops seamlessly
    @staticmethod
    def introduce(cbc):
        # custom creation animation - Create(cbc) and Write(cbc) also work,
        # but i think this looks nicer
        return LaggedStart(
            AnimationGroup(    
                Write(cbc.ct_to_xor),    
                Write(cbc.pt_to_xor),
                Write(cbc.xor_to_enc),
                Write(cbc.enc_to_ct),
                FadeIn(cbc.xor),
                FadeIn(cbc.enc),
            ),
            FadeIn(cbc.ct, shift=0.5*DOWN, run_time=0.5),
            lag_ratio=0.2
        )

    def construct(self):
        iv_block  = CBCBlock()
        chained_1 = CBCBlock(prev=iv_block)
        chained_2 = CBCBlock(prev=chained_1)
        chained_3 = CBCBlock(prev=chained_2)
        chained_4 = CBCBlock(prev=chained_3)
        chained_5 = CBCBlock(prev=chained_4)
        chained_6 = CBCBlock(prev=chained_5)

        self.add(iv_block, chained_1, chained_2, chained_3, chained_4.pt, chained_5.pt, chained_6.pt)
        self.camera.frame.scale(2.2).move_to(chained_2.xor_to_enc)
        self.play(
            self.introduce(chained_4),
            self.camera.frame.animate(rate_func=linear).move_to(chained_3.xor_to_enc),
            run_time=2
        )
```

-----

![CBCExample5](examples/renders/CBCExample5_ManimCE_v0.17.3.png)

```python
class CBCExample5(Scene):
    def construct(self):
        # accepts and automatically encodes strings (assumes ASCII)
        blocks = CBCBlocks("YELLOW SUBMARINE"*2, zoom=2/3)
        self.add(blocks)
```

-----

![CBCExample6](examples/renders/CBCExample6.mp4)

```python
class CBCExample6(Scene):
    def construct(self):
        blocks = CBCBlocks("YELLOW SUBMARINE"*3, zoom=2/3)
        self.add(blocks)
        self.wait(0.5)
        self.play(Rewrite(blocks[0], "MISTER BOATSWAIN"))
        self.wait(0.5)
```


## CodeRewrite


![CodeRewriteExample1](examples/renders/CodeRewriteExample1.mp4)

```python
class CodeRewriteExample1(Scene):
    def construct(self):
        kwargs = {"language": "python", "tab_width": 4, "font": "Monospace", "style": "inkpot", "background": "window", "line_spacing": 0.6, "insert_line_no": False}
        code_1 = Code("code/padding_oracle_1.py", **kwargs).scale(0.5)
        code_2 = Code("code/padding_oracle_2.py", **kwargs).scale(0.5).align_to(code_1, UL)
        self.add(code_1)
        self.wait(0.5)
        self.play(CodeRewrite(code_1, code_2))
        self.wait(0.5)
```


## Cycle


![CycleExample1](examples/renders/CycleExample1.mp4)

```python
class CycleExample1(Scene):
    def construct(self):
        box = ByteBox(0)
        self.add(box)
        self.wait(0.5)
        self.play(Cycle(box, range(256)))
        self.wait(0.5)
```


## ECBBlock


![ECBExample1](examples/renders/ECBExample1_ManimCE_v0.17.3.png)

```python
class ECBExample1(Scene):
    def construct(self):
        self.add(ECBBlock())
```

-----

![ECBExample3](examples/renders/ECBExample3.mp4)

```python
class ECBExample3(Scene):
    def construct(self):
        blocks = ECBBlocks(bytes(16*8), direction=RIGHT, pbuff=0.4)
        self.add(blocks.zoom(0.7))
        self.wait()
        new_msg = bytes(15) + b'\x01'
        new_pt_fills, new_ct_fills = [C_PT]*15 + [darken(C_PT, amount=0.25)], darken(C_CT, amount=0.25)
        self.play(*[
            Rewrite(row, new_msg, c_pt=new_pt_fills, c_ct=new_ct_fills)
            for row in blocks[4:]
        ])
        self.wait()
```

-----

![ECBExample4](examples/renders/ECBExample4_ManimCE_v0.17.3.png)

```python
class ECBExample4(Scene):
    def construct(self):
        # you can use ASCII strings as inputs and they will be automatically encoded
        blocks = ECBBlocks("YELLOW SUBMARINE"*2, direction=RIGHT)
        self.add(blocks.zoom(0.7))
```


## ECBBlocks


![ECBExample2](examples/renders/ECBExample2_ManimCE_v0.17.3.png)

```python
class ECBExample2(Scene):
    def construct(self):
        self.add(ECBBlocks(bytes(32), zoom=0.7))
```


## FuncBox


![FuncBoxExample1](examples/renders/FuncBoxExample1_ManimCE_v0.17.3.png)

```python
class FuncBoxExample1(Scene):
    def construct(self):
        self.add(FuncBox("H"))
```

-----

![FuncBoxExample2](examples/renders/FuncBoxExample2_ManimCE_v0.17.3.png)

```python
class FuncBoxExample2(Scene):
    def construct(self):
        from hashlib import sha256
        msg = b'aaaa'
        img = sha256(msg).digest()

        input_block = Block(msg, c_fills=C_PT, block_size=None)
        output_block_1 = Block(img[:16], c_fills=C_CT)  # first half of digest
        output_block_2 = Block(img[16:], c_fills=C_CT)  # second half of digest

        input_block.shift(UP*1.5)
        output_block_1.shift(DOWN*1.5)
        output_block_2.next_to(output_block_1, DOWN, buff=0.00)

        func_box = FuncBox.with_arrows(
            (input_block, DOWN, UP),
            (output_block_1, DOWN, UP),
            r"H",
        )

        self.add(input_block, output_block_1, output_block_2, func_box)
```

-----

![FuncBoxExample3](examples/renders/FuncBoxExample3.mp4)

```python
class FuncBoxExample3(Scene):
    def construct(self):
        from hashlib import sha256
        msg = b'aaaa'
        hsh = sha256(msg).digest()

        input_block = Block(msg, c_fills=C_PT, block_size=None)
        output_block_1 = Block(hsh[:16], c_fills=C_CT)  # first half of digest
        output_block_2 = Block(hsh[16:], c_fills=C_CT)  # second half of digest

        input_block.shift(UP*1.5)
        output_block_1.shift(DOWN*1.5)
        output_block_2.next_to(output_block_1, DOWN, buff=0.00)

        func_box = FuncBox.with_arrows(
            (input_block, DOWN, UP),
            (output_block_1, DOWN, UP),
            "H",
        )

        self.play(FadeIn(input_block), run_time=1)
        self.play(Write(func_box))
        self.play(FadeIn(output_block_1, output_block_2, shift=DOWN*0.5), run_time=0.8)
        self.wait()
```


## PaddingBlock


![PaddingBlockExample1](examples/renders/PaddingBlockExample1.mp4)

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

![PaddingBlockExample2](examples/renders/PaddingBlockExample2.mp4)

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

![PaddingBlockExample3](examples/renders/PaddingBlockExample3.mp4)

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

![BoxLenExample2](examples/renders/BoxLenExample2.mp4)

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


## Slide


![SlideExample1](examples/renders/SlideExample1.mp4)

```python
class SlideExample1(Scene):
    def construct(self):
        token = list('email=foo@bar.com&uid=10&role=user')
        last_len = len(token[32:])
        pad_len = 16-last_len
        block_1 = Block(token[:16], c_fills=C_PT)
        block_2 = Block(token[16:32], c_fills=C_PT)
        block_3 = PaddingBlock(token[32:])

        ZoomableVGroup(block_1, block_2, block_3, zoom=0.8).arrange(DOWN).center()
        self.add(block_1, block_2, block_3)
        self.wait(0.5)
        self.play(
            LaggedStart(
                FadeOut(block_3[2], scale=0.5, rate_func=rate_functions.ease_in_cubic),
                FadeOut(block_3[3], scale=0.5, rate_func=rate_functions.ease_in_cubic),
                Slide(*block_1, *block_2, *block_3, start=7, stop=-14, shift=2),
                FadeIn(new_o_1 := block_1[7].copy(), scale=0.5),
                FadeIn(new_o_2 := block_1[8].copy(), scale=0.5),
                lag_ratio=0.25,
            ),
            AnimationGroup(*[Rewrite(byte, 12, C_PAD) for byte in block_3[4:]]),
            run_time=5,
        )
        self.wait()

        new_block_1 = Block.from_boxes(*block_1[:7], new_o_1, new_o_2, *block_1[7:14])
        new_block_2 = Block.from_boxes(*block_1[-2:], *block_2[:-2])
        new_block_3 = Block.from_boxes(*block_2[-2:], *block_3[:2], *block_3[4:])
        admin_block = Block(list("admin") + [11]*11, c_fills=C_PT, zoom=0.8)
        self.play(
            Group(
                new_block_1,
                admin_block,
                new_block_2,
                new_block_3,
            ).animate.arrange(DOWN).align_to(new_block_1, UP),
        )
        self.wait()
        self.play(
            admin_block.animate.move_to(new_block_2),
            new_block_2.animate.move_to(admin_block),
        )
        self.wait(0.5)
        self.play(
            Rewrite(admin_block, c_fills=[C_PT]*5+[C_PAD]*11),
            FadeOut(new_block_3),
        )
        self.wait()
```


## TextToBuffer


![TextToBufferExample1](examples/renders/TextToBufferExample1.mp4)

```python
class TextToBufferExample1(Scene):
    def construct(self):
        pt_msg = "This is a plaintext string!"
        text = Text(pt_msg).scale(0.7).shift(UP/3)
        buff = Blocks(pt_msg, c_fills=C_PT, zoom=0.7, n_cols=2, buff=1/3).shift(DOWN/3)
        self.add(text)
        self.wait(0.5)
        self.play(TextToBuffer(text, buff, lag_ratio=0.05))
        self.wait(0.5)
```


