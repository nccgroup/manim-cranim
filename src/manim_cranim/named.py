from manim import *
from .zoom import *


@zoomable
class NamedGroup(Group):
    """Helper class for creating groups with custom attributes.

    Parameters
    ----------
    d : dict[str, Any]
        Attributes to set. Key/value pairs from d are passed to setattr.
    """
    def __init__(self, d, *args, **kwargs):
        items = sorted(d.items())
        super().__init__(*[t[1] for t in items], *args, **kwargs)
        for k, v in items:
            setattr(self, k, v)


@zoomable
class NamedVGroup(VGroup):
    """Helper class for creating groups with custom attributes.

    Parameters
    ----------
    d : dict[str, Any]
        Attributes to set. Key/value pairs from d are passed to setattr.
    """
    def __init__(self, d, *args, **kwargs):
        #items = sorted(d.items())
        items = d.items()  # turns out this doesn't need to be sorted any more since dicts are ordered now lol
        super().__init__(*[t[1] for t in items], *args, **kwargs)
        for k, v in items:
            setattr(self, k, v)
