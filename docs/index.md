# CBCExample4

<video controls allowfullscreen> <source src="renders/CBCExample4.mp4" type="video/mp4"> </video>

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


