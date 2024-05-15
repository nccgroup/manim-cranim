
![FuncBoxExample1](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/FuncBoxExample1_ManimCE_v0.18.1.png)

```python
class FuncBoxExample1(Scene):
    def construct(self):
        self.add(FuncBox("H"))
```

-----

![FuncBoxExample2](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/FuncBoxExample2_ManimCE_v0.18.1.png)

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

![FuncBoxExample3](https://github.com/nccgroup/manim-cranim/raw/main/examples/renders/FuncBoxExample3.mp4)

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
