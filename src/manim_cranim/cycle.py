from manim import *


class Cycle(Animation):
    # this performs better than .rewrite() + .wait(), and also results
    # in a lower level of compression noise in the final video

    def __init__(self, box, vals, rate=1/20, run_time=None, *args, **kwargs):
        self.box = box
        if run_time is None:
            run_time = rate * len(vals)
        else:
            rate = run_time / len(vals)
        self._t = 0
        self._i = 0
        self._dt = rate / run_time

        copy = box.copy()
        self.texts = [copy.rewrite(val).text.copy() for val in vals]
        self.final_val = vals[-1]

        super().__init__(box, *args, run_time=run_time, _on_finish=self.on_finish, **kwargs)

    def interpolate_mobject(self, dt):
        if dt > self._t and self._i < len(self.texts):
            self.box.text.become(self.texts[self._i])
            while dt > self._t:
                self._t += self._dt
                self._i += 1
        super().interpolate_mobject(dt)

    def on_finish(self, _):
        self.box.rewrite(self.final_val)
