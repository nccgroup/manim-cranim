
{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/SlideExample1.mp4" type="video/mp4"> </video>
{:/nomarkdown}

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

{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/BlockExample1.mp4" type="video/mp4"> </video>
{:/nomarkdown}

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

{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/BlockExample2_ManimCE_v0.18.1.png" type="video/mp4"> </video>
{:/nomarkdown}

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

{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/BlockExample3_ManimCE_v0.18.1.png" type="video/mp4"> </video>
{:/nomarkdown}

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
