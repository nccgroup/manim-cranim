from manim import *
from manim import VGroup


from colour import Color

#from typing import Sequence
#from functools import cached_property

#import re

from .named import *
from .zoom import *
from .colors import *
from .rewrite import *
from .cycle import *
from .buffers import *
from .named import *
from .types import *
from .boxlen import *
from .funcs import *
from .util import *
from .ciphermodes import *
from .highlight import *


#__all__ = [
#    # manim utilities that might also be useful to calling code
#    "NamedGroup", "NamedVGroup", "zoomable", "ZoomableVGroup",
#
#    # animations
#    "BlockWrite", "BlocksWrite", "WriteBlock", "WriteBlocks",
#    "Rewrite", "Slide", "FlowThru", "Pop",
#
#    # crypto-related helper functions
#    "_enc", "_dec", "_pad", "blk", "bytes_xor", "chunk_bytes",
#
#    # colors (most of these are aliases to the palette below)
#    "C_BOX_BG", "C_SCENE_BG", "C_EDGE", "C_FILL", "C_PT", "C_CT", "C_IV", "C_PAD", 
#
#    # Bang Wong's colorblind color palette
#    "BW_GOLD", "BW_SKYBLUE", "BW_GREEN", "BW_YELLOW", "BW_BLUE", "BW_ORANGE",
#    "BW_MAUVE", 
#
#    # Mobjects
#    "ByteBox", "Block", "PaddingBlock", "BendyArrow", "FuncBox", "EncBox",
#    "DecBox", "XOR", "ECBBlock", "CBCBlock", "BoxLen",
#
#    # types
#    "B_TYPE", "BS_TYPE", "TEXT_TYPE",
#]


config.background_color = C_SCENE_BG
Mobject.set_default(color=C_STROKE)  # omg it took me so long to realize i could do this


#@zoomable
#class Blocks(VGroup):
#    def __init__(self, msg, colors, block_size=16, pad=True, pad_kwargs={}, buff=0.5, **kwargs):
#        self.msg = msg
#        chunks = chunk_bytes(msg, block_size)
#        try:
#            len(colors)
#            if isinstance(colors, str): raise TypeError
#        except TypeError:
#            colors = [colors]*len(msg)
#        c_chunks = chunk_bytes(colors, block_size)  # type: ignore
#
#        if pad and len(chunks[-1]) == block_size:
#            chunks.append([])  # type: ignore
#
#        block_list = [
#            Block(chunk, colors)  # TKTK TODO Block() needs to accept block_size so we can pass that here
#            for chunk, colors in zip(chunks[:-1], c_chunks)
#        ]
#        if pad:
#            block_list.append(PaddingBlock(chunks[-1], **pad_kwargs))
#        Group(*block_list).arrange(DOWN, buff).center()  # type: ignore
#
#        super().__init__(*block_list, **kwargs)
#
#    def _on_finish(self, new_blocks):
#        self.remove(*self)
#        self.add(new_blocks)
#
#    def drop_range(self, start, stop, lag_ratio=0.17):
#        assert start <= stop
#        if stop == 0: return AnimationGroup()
#
#        # bookkeeping
#        msg = self.msg[:start] + self.msg[stop:]
#        shift = stop - start
#        boxes = [box for block in self for box in block]
#        last_block = self[-1]
#        fade_anims = [FadeOut(box, scale=0.5) for box in boxes[start:stop][::-1]]
#        shift_anims = []
#        pad_anims = []
#
#        # after the animation the current blocks will be removed and replaced
#        # with these
#
#        # TODO write classmethods for Block and PaddingBlock taking ByteBoxes
#        # as args, so we can keep the existing ByteBox instances around and
#        # just replace their containing Blocks, and a classmethod like
#        # Blocks.from_blocks() to wrap *those*. This will also allow us to
#        # preserve each ByteBox's colors.
#        new_blocks = Blocks(msg, GREEN)
#
#        # handle pading bytes (if necessary)
#        if isinstance(last_block, PaddingBlock):
#            pad_len = last_block.pad_len
#            pad_anims += [FadeOut(box, shift=RIGHT) for box in boxes[-pad_len:]]
#            boxes = boxes[:-pad_len]
#
#        # do the actual fancy shift marquee thing
#        for i, box in enumerate(boxes[stop:], start=stop):
#            path = Line(box.get_center(), boxes[i-1].get_center())
#            for j in range(2, shift+1):
#                path = path.add_line_to(boxes[i-j].get_center())
#            shift_anims.append(MoveAlongPath(box, path))
#
#        return LaggedStart(
#            *fade_anims,
#            AnimationGroup(
#                *shift_anims,
#                *pad_anims,
#                run_time=1.5
#            ),
#            lag_ratio=lag_ratio,
#            _on_finish=lambda _: self._on_finish(new_blocks),
#        )


class BlockWrite(AnimationGroup):
    """
    Fades in block backgrounds. Writes block text.
    In some cases this looks better than the default Write(),
    especially when you have white text on a light scene background.
    """

    def __init__(self, block, fade_lag_ratio=0.05, fade_run_time=1.5,
                 write_lag_ratio=0.1, write_run_time=1,
                 *args, **kwargs):
        self._block = block
        fades = AnimationGroup(
            *[FadeIn(box) for box in block.boxes],
            lag_ratio=fade_lag_ratio,
            run_time=fade_run_time,
            rate_function=linear,
        )
        writes = AnimationGroup(
            *[Write(text) for text in block.texts],
            lag_ratio=write_lag_ratio,
            run_time=write_run_time,
        )
        lag_ratio = kwargs.pop("lag_ratio", 0.25)
        super().__init__(fades, writes, *args, lag_ratio=lag_ratio, **kwargs)

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(*self._block.boxes)
        scene.remove(*self._block.texts)
        scene.add(self._block)
        super().clean_up_from_scene(scene)


class BlocksWrite(AnimationGroup):
    def __init__(self, *blocks, lag_ratio=0.25, **kwargs):
        anims = [BlockWrite(block) for block in blocks]
        super().__init__(LaggedStart(*anims, lag_ratio=lag_ratio), **kwargs)


# these names are better, but i'm keeping the old names around too for backwards compatibility
WriteBlock = BlockWrite
WriteBlocks = BlocksWrite


class RewriteTest(Scene):
    def construct(self):
        text_1 = Text("text one")
        text_2 = Text("text two")
        print("---- before add", self.mobjects)
        self.add(text_1)
        print("---- after add", self.mobjects)
        self.play(Rewrite(text_1, text_2, replace=False))
        print("---- after rewrite", self.mobjects)
        self.wait(0.5)



class ByteRewrite(AnimationGroup):
    def __init__(self, byte, b, color=None, text_color=None,
                 stroke_color=C_STROKE, lag_ratio=0.6, **kwargs):
        self._byte = byte
        self._to_remove = []

        if color is None:
            color = byte.color
        else:
            color = Color(color)
        if text_color is None:
            text_color = C_STROKE if color == Color(C_BOX_BG) else C_BOX_BG
        anims = []
        anims.append(AnimationGroup(byte.box.animate.set_fill(color).set_stroke(color=stroke_color), lag_ratio=0.99))  # type: ignore  # FIXME broken if color=None

        b = byte._b_normalize(b)
        if b is None:
            if byte.b is not None:
                assert byte.text is not None
                anims.append(Unwrite(byte.text))
                byte.text = byte.b = None
        elif b == byte.b:
            anims.append(Transform(byte.text, byte.text))  # dummy anim to keep text on top of box
        elif byte.b is None:
            byte.b = b
            text = byte.set_byte(b, text_color)
            anims.append(Write(
                text,
                _on_finish=lambda _: byte.add(text),
                run_time=1+lag_ratio,
            ))
            self._to_remove.append(text)
        else:
            old_text = byte.text
            assert old_text is not None
            new_text = byte.set_byte(b, text_color)
            byte.remove(old_text)
            byte.b = b
            anims.append(Rewrite(
                old_text,
                new_text,
                lag_ratio=lag_ratio,
                _on_finish=lambda _: byte.add(new_text)
            ))
            self._to_remove.append(new_text)
        super().__init__(*anims, **kwargs)

    def clean_up_from_scene(self, scene: Scene) -> None:
        for text in self._to_remove:
            scene.mobjects.remove(text)
            self._byte.add(text)
        #scene.mobjects.remove(*self._to_remove)
        self._byte.add(*self._to_remove)
        super().clean_up_from_scene(scene)


class BlockRewrite(AnimationGroup):
    def __init__(self, block, bs=None, colors=None, text_colors=None, **kwargs):
        self._block = block

        block.bs = bs = block._bs_normalize(bs)
        block.colors = colors = block._colors_normalize(colors)
        block.text_colors = text_colors = block._colors_normalize(text_colors, default_color=C_BOX_BG)
        animations = [
            box.rewrite(*args, scale=block._zoom)
            for box, *args in zip(block, bs, colors, text_colors)
        ]
        animations = [a for a in animations if a is not None]
        assert len(animations) > 0
        super().__init__(*animations, **kwargs)

    def clean_up_from_scene(self, scene):
        scene.remove(*self._block)
        scene.add(self._block)


class Slide(AnimationGroup):
    def __init__(self, *shapes, shift, start, stop=None, **kwargs):
        assert shift != 0
        dir = -1 if shift < 0 else 1
        to_move = shapes[start:stop]
        anims = []
        for i, mob in enumerate(to_move, start=start):
            adj = shapes[i+dir]
            path = Line(mob.get_center(), adj.get_center())
            for j in range(2, abs(shift)+1):
                adj = shapes[i+j*dir]
                path = path.add_line_to(adj.get_center())
            anims.append(MoveAlongPath(mob, path))
        super().__init__(*anims, **kwargs)


class Pop(Indicate):
    def __init__(self, *args, scale_factor=1.3, run_time=2.0, rate_func=there_and_back_with_pause, **kwargs):
        super().__init__(*args, color=None, scale_factor=scale_factor,
                         rate_func=rate_func, run_time=run_time, **kwargs)
