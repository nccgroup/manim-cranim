from manim import *
from .zoom import *
from .colors import *
from .buffers import *
from .rewrite import *


@zoomable
class BoxLen(VGroup):
    def __init__(self, rhs=r"\:?", c_box=C_PT, c_stroke=C_STROKE, tex_kwargs=None, **kwargs):
        super().__init__(**kwargs)
        tex_kwargs = tex_kwargs or {}
        tex_kwargs.setdefault("color", c_stroke)
        self.eqn = eqn = self._make_tex(rhs, tex_kwargs)
        lhs, self.eq, self.rhs = self.eqn
        self.box = box = ByteBox(None, c_box, zoom=0.8).move_to(eqn[0][3:])
        self.lhs = VGroup(lhs, box)
        self.add(eqn, box)

    @staticmethod
    def _make_tex(rhs, kwargs):
        return MathTex(r"len(\quad)", "=", rhs, **kwargs)

    def write_lhs(self, include_eq=False):
        return AnimationGroup(Write(self.eqn[0:2 if include_eq else 1]), Write(self.box))  # type: ignore

    def write_rhs(self, include_eq=False):
        return Write(self.eqn[1 if include_eq else 2:])  # type: ignore

    def update_rhs(self, new_rhs, transform=None, **kwargs):
        """
        Replaces eqn's rhs with new_rhs.
        If transform=None, does this instantaneously and returns self.
        Otherwise, returns an animation using the given transformation function.
        (e.g. Transform, TransformMatchingShapes, Rewrite)
        """
        new_box_len = BoxLen(new_rhs, **kwargs)
        new_box_len.shift(self.lhs.get_center() - new_box_len.lhs.get_center())  # type: ignore
        if transform is None:
            self.rhs.become(new_box_len.rhs)
            return self
        else:
            anim = transform(self.rhs, new_box_len.rhs)
            self.rhs = new_box_len.rhs
            return anim

    def rewrite_rhs(self, new_rhs, **kwargs):  # convenience method wrapping update_rhs
        return self.update_rhs(new_rhs, transform=Rewrite, **kwargs)
