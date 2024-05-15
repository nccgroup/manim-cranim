from manim import *
import re
from .named import *
from .zoom import *
from .colors import *
from .types import *
from .util import *


class BlockSizeError(Exception):
    pass


@zoomable
class ByteBox(VGroup):
    def __init__(
        self,
        byte: B_TYPE = None,
        c_fill=C_BOX_BG,
        c_text=C_STROKE,
        c_stroke=C_STROKE,
        escape=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.b = byte
        self.c_fill = c_fill
        self.c_text = c_text
        self.c_stroke = c_stroke
        self.escape = escape
        self._normalize_attrs()
        self._add_box()
        self._add_text()
        self.old_text = None

    def __str__(self):
        return f"ByteBox('{self.b}')"

    def __repr__(self):
        return str(self)

    def rewrite(  # rewrites b in place - NO ANIMATION
        self,
        byte,
        c_fill=None,
        c_text=None,
        c_stroke=C_STROKE,
        escape=True,
    ):
        self.b = byte
        if c_fill is not None: self.c_fill = c_fill
        if c_text is not None: self.c_text = c_text
        if c_stroke is not None: self.c_stroke = c_stroke
        self.escape = escape
        self._normalize_attrs()  # normalize inputs before using them
        self.old_text = old_text = self.text
        self.remove(old_text)
        self._add_text()
        self.box.become(self._get_box(self.c_stroke, self.c_fill).move_to(self.box))
        return self

    def _add_box(self):
        self.box = box = self._get_box(self.c_stroke, self.c_fill)
        self.add(box)
        return box

    def _add_text(self):
        self.text = text = self._get_byte_tex()
        self._center_tex_in_box()
        self.add(text)

    def _get_box(self, c_stroke, c_fill, **kwargs):
        box_style = {
            "width": 0.5,
            "height": 0.5,
            "stroke_color": c_stroke,
            **({"fill_opacity": 0} if c_fill is None else
               {"fill_opacity": 1, "fill_color": c_fill}),
            **kwargs,
        }
        box = Rectangle(**box_style)
        ByteBox.zoom(box, self._zoom)  # type: ignore  # TODO FIXME how do we fix this one? zoom comes from the decorator
        return box

    def _get_byte_tex(self, byte=None, c_text=None, escape=None, scale=0.75, **kwargs):
        byte = byte or self.byte
        c_text = c_text or self.c_text
        escape = self.escape if escape is None else escape
        assert type(byte) is str
        # only apply texttt if escape is True, because it is bad at handling
        # unescaped special chars. also avoid empty \texttt{}
        if escape and byte != "":
            tex_string = r"\texttt{ " + byte + " }"
        else:
            tex_string = self.byte
        kwargs.setdefault("color", c_text)
        tex = MathTex(tex_string, **kwargs).scale(scale)
        ByteBox.zoom(tex, self._zoom)  # type: ignore  # TODO FIXME how do we fix this one? zoom comes from the decorator
        return tex

    def _normalize_attrs(self):
        self.c_text = self._normalize_text_color(self.c_text, self.c_stroke, self.c_fill)
        self.byte = self._normalize_byte(self.b, self.escape)

    @property
    def bytes(self):
        ch = self.byte
        assert isinstance(ch, str)
        if ch.startswith('\\'):
            ch = ch[1:]
        i = int(ch, 16) if len(ch) == 2 else ord(' ' if ch == '' else ch)
        return bytes([i])

    @staticmethod
    def _normalize_text_color(c_text, c_stroke, c_fill):
        if c_text is not None:
            return c_text
        if c_fill == C_BOX_BG:
            return c_stroke
        return C_BOX_BG

    @staticmethod
    def _normalize_byte(b, escape):
        match b:
            case None:
                b = ""
            case str(b):
                b = b.strip()
            case int(b):
                pass
            case bytes(b) if len(b) == 1:
                b = b[0]
            case _:
                raise ValueError("bad byte value", b)
        if isinstance(b, int):
            b = hex(b)[2:].rjust(2, '0')
        assert isinstance(b, str)
        if escape:
            b = ByteBox._tex_escape(b)
        return b

    def _center_tex_in_box(self):
        # hacky, but it works :) supports just-about-arbitrary LaTeX, not just the listed characters below
        b = self.byte
        assert isinstance(b, str)
        if b == "": return
        tex = self.text
        box = self.box
        escape = self.escape
        dummy_tex_1 = self._get_byte_tex("0", C_STROKE, escape=escape)
        dummy_tex_2 = self._get_byte_tex("0" + b, C_STROKE, substrings_to_isolate="0", escape=escape)
        self._old_center_tex_in_box(dummy_tex_1, box)
        dummy_tex_2.move_to(dummy_tex_1.get_center() - dummy_tex_2[0].get_center())  # type: ignore
        tex.move_to(box).match_y(dummy_tex_2[2 if escape else 1:])

    @staticmethod
    def _old_center_tex_in_box(tex, box):
        # centers a '0' character in a box; used as a helper for _center_tex_in_box()
        # finds the center point by taking a weighted average of the box's top and bottom edge-centers
        tex.move_to(box)
        anchor_1 = box.get_edge_center(UP)
        anchor_2 = box.get_edge_center(DOWN)
        ratio = 0.26025
        tex.align_to(Point(anchor_2*ratio + anchor_1*(1-ratio)), UP)

    @staticmethod
    def _tex_escape(text) -> str:
        """
            :param text: a plain text message
            :return: the message escaped to appear correctly in LaTeX
        """
        conv = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\char`~',  # TODO FIXME this ~ is too high and stack overflow says "there are 1000 alternatives but none of them actually work"
            '^': r'\string^',
            '<': r'\textless{}',
            '>': r'\textgreater{}',
            '\\': r'\textbackslash{}',
        }
        regex = re.compile('|'.join(re.escape(key) for key in conv.keys()))
        return regex.sub(lambda match: conv[match.group()], text)


@zoomable
class Block(VGroup):
    def __init__(
            self,
            block=None,
            c_fills=None,
            c_texts=None,
            block_size=16,
            c_stroke=C_STROKE,
            **kwargs
    ):
        self.block = block
        self.bs = None
        self.c_fills = c_fills
        self.c_texts = c_texts
        self.block_size = block_size
        self.c_stroke = c_stroke
        #self.stroke_color = stroke_color
        self._normalize_attrs()
        self.byte_boxes = byte_boxes = self._get_byte_boxes()
        super().__init__(*byte_boxes, **kwargs)

    def __str__(self):
        return f'Block("{" ".join(self.bs)}")'

    def __repr__(self):
        return str(self)

    def _normalize_attrs(self):
        bs = self.bs
        block_size = self.block_size if bs is None else len(bs)
        self.bs = bs = self._validate_and_normalize_block(block_size, self.block)
        self.block_size = block_size = len(bs)  # if block_size was None, fix it to the initial size; in other cases this has no effect
        self.c_fills = self._normalize_fill_colors(self.c_fills, block_size)
        self.c_texts = self._normalize_text_colors(self.c_texts, self.stroke_color, self.c_fills, block_size)

    @staticmethod
    def _validate_and_normalize_block(block_size, block):
        # normalize block 
        block = Block._normalize_buffer(block, block_size=block_size)
        # check block size (if possible)
        if block_size is not None:
            if block is None:
                block = [None] * block_size
            if isinstance(block, str):
                if len(block) != 2*block_size:
                    raise BlockSizeError(f"Expected len {2*block_size}, got {len(block)}")
            elif len(block) != block_size:  # type: ignore  # TODO how do we convince the linter that bs can be len()'d?
                raise BlockSizeError(f"Expected len {block_size}, got {len(block)}")  # type: ignore
        # store result as bs
        if block_size is None:
            block_size = len(block)
        else:
            assert block_size == len(block)  # if this assert fails, the block size check above is broken
        return block

    @staticmethod
    def _normalize_buffer(block, block_size=None, allow_multiple_blocks=False):
        if block is None:
            assert block_size is not None
            block = (None,) * block_size
        match block:
            case str(block):
                if block_size is not None and block.count(" ") == block_size-1:
                    # treat block as space-separated list (like the enum interface)
                    block = tuple(block.split(" "))
                else:
                    # treat block as ascii string
                    #block = tuple(block[i:i+2] for i in range(0, len(block), 2))  # split after every other char
                    block = tuple(ch for ch in block)
            case bytes(block) | list(block) | (range() as block):
                block = tuple(block)
            case tuple(block):
                pass
            case _:
                raise ValueError("bad block value", block)
        assert isinstance(block, tuple)
        if block_size is not None:
            assert len(block) == block_size or (allow_multiple_blocks and len(block) % block_size == 0)
        return tuple(ByteBox._normalize_byte(b, escape=False) for b in block)  # leave escaping to the ByteBox - if we pass escape=True here we'll end up double-escaping

    @staticmethod
    def _normalize_fill_colors(c_fills, block_size):
        fill_colors = C_BOX_BG if c_fills is None else c_fills
        if isinstance(fill_colors, (str, ManimColor)):
            fill_colors = [fill_colors] * block_size
        else:
            assert len(fill_colors) == block_size  # type: ignore  # TODO fix bg_colors type annotation
        return fill_colors

    @staticmethod
    def _normalize_text_colors(c_texts, c_stroke, c_fills, block_size):
        text_colors = C_STROKE if c_texts is None else c_texts
        if isinstance(text_colors, (str, ManimColor)):
            text_colors = [text_colors] * block_size
        else:
            assert len(text_colors) == block_size  # type: ignore  # TODO same as above
        return [ByteBox._normalize_text_color(text_color, c_stroke, fill_color)
                for text_color, fill_color in zip(text_colors, c_fills)]  # type: ignore  # TODO same as above

    def _get_byte_boxes(self):
        assert self.bs is not None and self.c_fills is not None and self.c_texts is not None
        byte_boxes = [ByteBox(*args, c_stroke=self.c_stroke)
                      for args in zip(self.bs, self.c_fills, self.c_texts)]
        Group(*byte_boxes).arrange(RIGHT, buff=0).center()  # type: ignore  # TODO fix manim's type annotations here
        return byte_boxes

    @classmethod
    def from_boxes(cls, *boxes, **kwargs):
        bs = [box.b for box in boxes]
        fill_colors = [box.box.fill_color if box.fill_opacity > 0 else None for box in boxes]
        text_colors = [None if box.text is None else box.text.color for box in boxes]
        kwargs.setdefault("block_size", len(bs))
        block = Block(bs, fill_colors, text_colors, **kwargs)
        block.remove(*block.submobjects)
        for box in boxes:
            block.add(box)
        return block

    @property
    def bytes(self):
        assert self.bs is not None
        #return bytes(int(ch, 16) if len(ch) == 2 else ord(' ' if ch == '' else ch) for ch in self.bs)  # type: ignore  # TODO fix types here
        return b''.join(box.bytes for box in self.byte_boxes)

    @property
    def _boxes(self):
        return [byte_box.box for byte_box in self]

    @property
    def boxes(self):
        return ZoomableVGroup(*self._boxes)

    @property
    def _texts(self):
        return [byte_box.byte for byte_box in self]  # TODO is .byte correct here? Should be the MathTex attr

    @property
    def texts(self):
        return ZoomableVGroup(*self._texts)

    def rewrite(self, block=None, c_fills=None, c_texts=None, escape=True, **kwargs):
        self.block   = [""] * self.block_size if block   is None else block
        self.c_fills = self.c_fills           if c_fills is None else c_fills
        self.c_texts = self.c_texts           if c_texts is None else c_texts
        self._normalize_attrs()
        block, c_fills, c_texts = self.block, self.c_fills, self.c_texts
        assert block is not None and c_fills is not None and c_texts is not None
        for byte_box, *args in zip(self, block, c_fills, c_texts):  # type: ignore  # TODO fix types
            byte_box.rewrite(*args, escape=escape, **kwargs)
        return self


#@zoomable   # TODO FIXME this doesn't work??
class PaddingBlock(Block):
    """A Block with automatically populated padding bytes. Provide a padding
    function or use the default (PKCS7). Update your block's contents and the
    padding bytes will change as well.

    Parameters
    ----------
    msg_bytes : BS_TYPE
        Block contents (sans padding) - must be less than 16 bytes
    padfunc : Callable
        Optional: provide a custom padding function. Called with required
        padding length. If None, PKCS7 padding is used. Defaults to None.

    Attributes
    ----------
        pad_bytes : BS_TYPE
            Current padding bytes
        msg_len : int
            len(msg_bytes)
        msg_bytes : list[str]
        pad_len : int
            len(pad_bytes)
        block : list[str]
            msg_bytes + pad_bytes
    """
    def __init__(self, msg_bytes=None, c_msg=C_PT, c_pad=C_PAD, padfunc=None, block_size=16, **kwargs):
        super().__init__(bytes(block_size), **kwargs)
        msg_bytes = [] if msg_bytes is None else msg_bytes
        self.c_msg = c_msg
        self.c_pad = c_pad
        self.block_size = block_size
        self.padfunc = self._get_padding if padfunc is None else padfunc
        self._pad_update(msg_bytes, padfunc=padfunc)
        self.rewrite(msg_bytes)
        #super().__init__(self.block, self._get_colors(), block_size=block_size, **kwargs)

    @staticmethod
    def _get_padding(pad_len):
        """Default padding function. Adds padding bytes equal to padding len.
        Note that padding len is not bounds-checked.

        Parameters
        ----------
            pad_len : int
                Number of bytes of padding to provide.

        Returns
        -------
            bytes
        """
        return bytes([pad_len])*pad_len

    def _pad_update(self, msg_bytes, padfunc=None):
        padfunc = self.padfunc if padfunc is None else padfunc
        self.msg_bytes = msg_bytes = self._normalize_buffer(msg_bytes)
        self.msg_len = msg_len = len(msg_bytes)
        if msg_len >= self.block_size:
            raise BlockSizeError("PaddingBlock contents must be shorter than block size")
        self.pad_len = pad_len = self.block_size - msg_len
        self.pad_bytes = pad_bytes = self._normalize_buffer(padfunc(pad_len))
        self.block = msg_bytes + pad_bytes
        self.bs = None
        self._normalize_attrs()

    def rewrite(self, msg_bytes=None, padfunc=None, **kwargs):
        msg_bytes = self.msg_bytes if msg_bytes is None else msg_bytes
        padfunc = self.padfunc if padfunc is None else padfunc
        self._pad_update(msg_bytes, padfunc)
        return super().rewrite(self.bs, c_fills=self._get_colors())

    def get_braces(self, blk_text="Block", msg_text="Message", pad_text="Padding", use_tex=False, blk_dir=DOWN, msg_dir=UP, pad_dir=UP, color=C_STROKE):
        blk_brace = Brace(self, color=color, direction=blk_dir)  # type: ignore
        msg_brace = Brace(self[:self.msg_len], color=color, direction=msg_dir)  # type: ignore
        pad_brace = Brace(self[self.msg_len:], color=color, direction=pad_dir)  # type: ignore

        if use_tex:
            blk_text = blk_brace.get_tex(blk_text).set_color(color)
            msg_text = msg_brace.get_tex(msg_text).set_color(color)
            pad_text = pad_brace.get_tex(pad_text).set_color(color)
        else:
            blk_text = blk_brace.get_text(blk_text).set_color(color)
            msg_text = msg_brace.get_text(msg_text).set_color(color)
            pad_text = pad_brace.get_text(pad_text).set_color(color)

        return NamedVGroup({
            "blk_brace": blk_brace,
            "msg_brace": msg_brace,
            "pad_brace": pad_brace,
            "blk_text": blk_text,
            "msg_text": msg_text,
            "pad_text": pad_text
        })

    def _get_colors(self):
        return [self.c_msg]*self.msg_len + [self.c_pad]*self.pad_len


@zoomable
class Blocks(VGroup):
    def __init__(self, contents, c_fills=C_BOX_BG, c_texts=C_STROKE, c_stroke=C_STROKE, c_pad=C_PAD, buff=0, block_size=16, pad=True, n_cols=1, padfunc=None):
        self.pad = pad
        self.block_size = block_size
        self.c_stroke = c_stroke
        contents, c_fills, c_texts = self._prepare_args(contents, c_fills, c_texts)

        # build a list of Block instances (and possibly a PaddingBlock too)
        self.blocks = blocks = [
            (
                PaddingBlock(bs, fills[0], c_pad, padfunc, block_size)
                if pad and len(bs) < block_size else
                Block(bs, fills, texts, block_size, c_stroke)
            ) for bs, fills, texts in zip(contents, c_fills, c_texts)
        ]

        # load the Blocks into self, then set them up
        super().__init__(*blocks)
        if n_cols == 1:
            self.arrange(DOWN, buff)  # TODO FIME do we always want DOWN or should we support other directions?
        else:
            self.arrange_in_grid(cols=n_cols, buff=buff)

    def rewrite(self, contents, c_fills=None, c_texts=None, **kwargs):
        # TODO FIXME make it so this supports adding/removing blocks
        contents, c_fills, c_texts = self._prepare_args(contents, c_fills, c_texts)
        for block, content, fills, texts in zip(self.blocks, contents, c_fills, c_texts):
            block.rewrite(content, c_fills=fills, c_texts=texts, **kwargs)

    def _prepare_args(self, contents, c_fills, c_texts):
        block_size = self.block_size

        contents = Block._normalize_buffer(contents, block_size=None)
        c_fills = Block._normalize_fill_colors(c_fills, block_size=len(contents))
        c_texts = Block._normalize_text_colors(c_texts, self.c_stroke, c_fills, block_size=len(contents))

        contents = chunk_bytes(contents, block_size)
        c_fills = chunk_bytes(c_fills, block_size)  # lol i need to rename chunk_bytes(), this looks so cursed
        c_texts = chunk_bytes(c_texts, block_size)  # and misleading

        if self.pad and len(contents) % block_size == 0:
            contents.append([])
            c_fills.append([])
            c_texts.append([])
        if self.pad and len(contents) % block_size == 0:  # edge case: do we need to add a full block of padding?
            contents.append([])
            c_fills.append([])
            c_texts.append([])
        return contents, c_fills, c_texts

    @property
    def bytes(self):
        return b''.join(block.bytes for block in self)

    @classmethod
    def from_blocks(cls, *blocks, **kwargs):
        return cls(
            _flatten(block.bs for block in blocks),
            _flatten(block.c_fills for block in blocks),  # type: ignore  # TODO FIXME fix type annotations
            _flatten(block.c_texts for block in blocks),  # type: ignore  # TODO FIXME fix type annotations
            **kwargs
        )

    ...  # TODO rewrite()
    ...  # TODO build out other features (eg helpers for in-place rewrite, diff+slide rewrite, etc)


class TextToBuffer(AnimationGroup):
    def __init__(self, text, buff, transform=Transform, pad=True, pad_kwargs=None, **kwargs):  # TODO figure out how to add "pad=True" kwarg (tricky bc we're not making the padding - buff would have it, if it exists)
        if pad:
            if pad_kwargs is None: pad_kwargs = {"lag_ratio": 0.1}
            #assert isinstance(buff, PaddingBlock) or (isinstance(buff, Blocks) and isinstance(buff[-1], PaddingBlock))
            if isinstance(buff, PaddingBlock):
                pad_len: int = buff.pad_len
            else:
                pad_len = buff[-1].pad_len
        text_str = text.text
        if isinstance(buff, Blocks):
            chs = [ch for block in buff for ch in block]
        else:
            chs = list(buff)
        transforms = [transform(ch, byte) for ch, byte in zip(text, [byte for byte in chs if byte.b != ""])]
        fades = [FadeIn(byte, target_position=text[i-text_str[:i].count(" ")], scale=0) for i, byte in enumerate(chs) if byte.b == ""]
        anims = [fades.pop(0) if chs[i].b == "" else transforms.pop(0) for i in range(len(transforms) + len(fades))]
        self._to_remove = [ch for ch in text] + [byte for byte in chs if byte.b == ""]
        self._to_add = [buff]
        pad_anims = []
        if pad:
            pad_anims = [FadeIn(*chs[-pad_len:], **pad_kwargs)]
            self._to_remove += list(chs[-pad_len:])

        super().__init__(
            Succession(
                AnimationGroup(*anims, **kwargs),
                *pad_anims
            ),
            _on_finish=self._on_finish,
        )

    def _on_finish(self, scene):
        scene.remove(*self._to_remove)
        scene.add(*self._to_add)


class BufferToText(AnimationGroup):
    def __init__(self, buff, text, transform=Transform, unpad=False, unpad_kwargs=None, per_char_run_time=0.8, **kwargs):
        text_str = text.text
        unpad_anims = []
        if unpad:
            if unpad_kwargs is None: unpad_kwargs = {"lag_ratio": 0.1}
            assert isinstance(buff, PaddingBlock) or (isinstance(buff, Blocks) and isinstance(buff[-1], PaddingBlock))
            if isinstance(buff, PaddingBlock):
                pad_len: int = buff.pad_len
            else:
                pad_len: int = buff[-1].pad_len
        if isinstance(buff, Blocks):
            buff = [ch for block in buff for ch in block]
        if unpad:
            msg = buff[:-pad_len]
            pad = buff[-pad_len:]
            unpad_anims = [FadeOut(*pad[::-1], **unpad_kwargs)]
        transforms = [transform(byte, ch, run_time=per_char_run_time) for ch, byte in zip(text, [byte for byte in buff if byte.b != ""])]
        fades = [FadeOut(byte, target_position=text[i-text_str[:i].count(" ")], scale=0, run_time=per_char_run_time) for i, byte in enumerate(buff) if byte.b == ""]
        anims = [fades.pop(0) if buff[i].b == "" else transforms.pop(0) for i in range(len(transforms) + len(fades))]
        self._to_remove = [byte for byte in buff if byte.b != ""][:len(text)]
        self._to_add = [text]
        super().__init__(
            Succession(
                *unpad_anims,
                AnimationGroup(*anims, **kwargs),
            ),
            _on_finish=self._on_finish,
        )

    def _on_finish(self, scene):
        scene.remove(*self._to_remove)
        scene.add(*self._to_add)
