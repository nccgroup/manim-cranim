from manim import *
from .types import *


def zoomable(cls):
    assert not hasattr(cls, "zoom")  # make sure we're not overwriting anything

    def _update_zoom_and_get_text_strokes(mobj, zoom):
        if not hasattr(mobj, "_zoom"):
            mobj._zoom = 1.0
        mobj._zoom *= zoom
        strokes = {}
        if isinstance(mobj, TEXT_TYPE):
            strokes[mobj] = mobj.get_stroke_width()
        for submobj in mobj.submobjects:
            strokes.update(_update_zoom_and_get_text_strokes(submobj, zoom))
        return strokes

    def zoom(self, amount, **kwargs):
        """
        Like .scale() but also adjusts stroke widths on everything except text.
        """
        stroke_width = self.get_stroke_width()
        text_strokes = _update_zoom_and_get_text_strokes(self, amount)
        self.scale(amount, **kwargs)
        self.set_stroke(width=stroke_width*amount)
        # reset stroke widths for text mobjects
        for text, stroke_width in text_strokes.items():
            text.set_stroke(width=stroke_width)
        return self

    cls.zoom = zoom
    cls._zoom_submobject = lambda self, mobj: [_update_zoom_and_get_text_strokes(mobj, self._zoom), None][1]

    _old_init = cls.__init__
    def __init__(self, *args, zoom=None, **kwargs):
        self._zoom = 1.0
        _old_init(self, *args, **kwargs)
        if zoom is not None:
            self.zoom(zoom)
    cls.__init__ = __init__

    return cls


@zoomable
class ZoomableVGroup(VGroup):
    pass
