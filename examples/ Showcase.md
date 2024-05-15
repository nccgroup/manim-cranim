
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
