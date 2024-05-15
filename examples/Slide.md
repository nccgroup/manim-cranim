
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
