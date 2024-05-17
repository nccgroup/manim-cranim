
{::nomarkdown}
<video controls allowfullscreen width=100%> <source src="renders/BufferToTextExample1.mp4" type="video/mp4"> </video>
{:/nomarkdown}

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
