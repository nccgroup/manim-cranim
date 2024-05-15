from manim import *
from typing import Sequence


B_TYPE = str | int | bytes | None
BS_TYPE = None | str | bytes | Sequence[B_TYPE]
TEXT_TYPE = MathTex | Text | MarkupText
