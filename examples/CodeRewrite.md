
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
