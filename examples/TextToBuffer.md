
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
