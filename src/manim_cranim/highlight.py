from manim import *


rush_from = rate_functions.rush_from
rush_into = rate_functions.rush_into


class Highlight(AnimationGroup):
    def __init__(self, *args, radial=False, **kwargs):
        if radial:
            super().__init__(HighlightRadial(*args, **kwargs))
        else:
            super().__init__(HighlightLinear(*args, **kwargs))


class HighlightRadial(ShowPassingFlash):
    def __init__(self, target, opacity=0.5, color=YELLOW, time_width=1, rate_func=rate_functions.double_smooth, run_time=1.5, buff=0.03, **kwargs):
        super().__init__(
            SurroundingRectangle(target, fill_color=color, fill_opacity=opacity, stroke_width=0, buff=buff),
            time_width=time_width,
            rate_func=rate_func,
            run_time=run_time,
            **kwargs,
        )


class HighlightLinear(Succession):
    def __init__(self, target, opacity=0.5, speed=0.4, color=YELLOW, time_width=1, delay=0.2, **kwargs):
        rect = SurroundingRectangle(target, fill_color=color, fill_opacity=opacity, stroke_width=0, buff=0.03)
        smaller = rect.copy().stretch_to_fit_width(0).align_to(rect, LEFT)
        super().__init__(
            Transform(smaller, rect, rate_func=rush_from, run_time=speed),
            Wait(delay),
            Transform(smaller, smaller.copy().align_to(rect, RIGHT), rate_func=rush_into, run_time=speed),
            time_width=time_width, **kwargs
        )


class HighlightExample(Scene):
    def construct(self):
        square = Text("Hello world!")
        self.add(square)
        self.play(HighlightRadial(square))
        self.wait(0.5)
        self.play(HighlightLinear(square))
        self.wait(0.5)
