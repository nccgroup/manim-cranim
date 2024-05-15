from manim import *
from manim.mobject.text.text_mobject import remove_invisible_chars  # not included in __all__ for some reason
from .buffers import *
from .boxlen import *
from .ciphermodes import *
from .util import *
from .funcs import FlowThru

from difflib import Differ
from types import UnionType



UNCHANGED = object()  # unique value used as default value for "contents" arg in Rewrite()


class TextRewrite(AnimationGroup):
    def __init__(self, old_text, new_text, lag_ratio=0.6):
        if isinstance(new_text, str):
            new_text = Text(new_text).move_to(old_text)
        super().__init__(Unwrite(old_text), Write(new_text), lag_ratio=lag_ratio)

        # TODO FIXME needs an on_finish hook to restore old_text and have it
        # .become new_text but will this break ByteRewrite()?


class Rewrite(AnimationGroup):
    # TODO is it possible for this class to actually somehow become the
    # underlying animation rather than wrapping it?
    # having an AnimationGroup of one animation seems redundant and ugly
    def __init__(self, buffer, contents=UNCHANGED, *args, **kwargs):
        # NOTE: dict order matters here! subclasses must appear before their parents
        if contents is UNCHANGED:
            if hasattr(buffer, 'block'): contents = buffer.block
            elif hasattr(buffer, 'bytes'): contents = buffer.bytes  # TODO FIXME breaks for eg ascii content (replaces chr with ord(chr))
        rewriters = {
            ECBBlock: ECBBlockRewrite,
            CBCBlock: CBCBlockRewrite,
            Blocks: BlocksRewrite,
            PaddingBlock: PaddingBlockRewrite,
            Block: BlockRewrite,
            ByteBox: ByteRewrite,
            #MathTex: TextRewrite,
            Text | Tex | MathTex: TextRewrite,
        }
        for cls, anim in rewriters.items():
            if isinstance(buffer, cls):
                animation = anim(buffer, contents, *args, **kwargs)
                break
        else:
            # no rewriter found for buffer
            classes = [elem for cls in rewriters.keys() for elem in (cls.__args__ if isinstance(cls, UnionType) else (cls,))]
            supported = ", ".join(cls.__name__ for cls in classes)
            raise TypeError("buffer must be one of: " + supported)
        super().__init__(animation)


class ByteRewrite(AnimationGroup):
    def __init__(self, byte_box: ByteBox, contents: B_TYPE, c_fill=C_BOX_BG, c_text=C_STROKE, c_stroke=C_STROKE, escape=True, calling_block=None, **kwargs):
        self.calling_block = calling_block
        self.byte_box = byte_box
        rect = byte_box.box
        contents = ByteBox._normalize_byte(contents, escape=escape)
        old_text = byte_box.text
        rect.save_state()
        byte_box.rewrite(contents, c_fill, c_text, c_stroke)
        rect_copy = rect.copy()
        rect.restore()
        self.new_text = byte_box.text
        byte_box.remove(byte_box.text)  # remove this for now - we'll add it back at the end
        text_anim = (
            self.new_text.animate.scale(1.0)
            if old_text.tex_strings == self.new_text.tex_strings else
            TextRewrite(old_text, self.new_text)
        )
        super().__init__(
            rect.animate.become(rect_copy),  # type: ignore  # TODO fix manim's type sigs here
            text_anim,
            _on_finish=self.on_finish,
            **kwargs
        )

    def on_finish(self, scene):
        assert self.new_text is not None
        byte_box, new_text, calling_block = self.byte_box, self.new_text, self.calling_block
        scene.remove(byte_box.box, new_text)
        byte_box.remove(byte_box.text)
        byte_box.add(new_text)
        byte_box.text = new_text
        scene.add(byte_box)
        if calling_block is not None:
            calling_block.on_finish(scene)


class BlockRewrite(AnimationGroup):
    def __init__(self, block: Block, contents=None, c_fills=None, c_texts=None, lag_ratio=0, rev=False, **kwargs):
        self.block = block
        block_size = block.block_size
        block.block = contents
        block.c_fills  = block.c_fills if c_fills is None else c_fills
        block.c_texts  = block.c_texts if c_texts is None else c_texts
        block._normalize_attrs()
        contents = block.bs
        c_fills = block.c_fills
        c_texts = block.c_texts
        assert len(contents) == len(c_fills) == len(c_texts) == block_size  # type: ignore  # TODO
        all_args = list(zip(block, contents, c_fills, c_texts))
        anims = [
            ByteRewrite(*args, calling_block=(self if args is all_args[-1] else None))
            for args in all_args  # type: ignore  # TODO
        ]
        if rev:
            anims = anims[::-1]
        super().__init__(*anims, lag_ratio=lag_ratio, _on_finish=self.on_finish, **kwargs)

    def on_finish(self, scene):
        # TODO FIXME this works when the top-level object being reconstituted is a Block - but what if the Block is contained in eg a CBCBlock?
        # can we figure out a way of cleanly handling those cases?
        scene.remove(*self.block)
        scene.add(self.block)


class BlocksRewrite(AnimationGroup):
    def __init__(self, blocks: Blocks, contents=None, c_fills=None, c_texts=None, c_stroke=C_STROKE, lag_ratio_h=0.025, lag_ratio_v=0.1, rev=False, **kwargs):
        block_size = blocks.block_size
        blocks_len = sum(len(block) for block in blocks.blocks)

        contents = Block._normalize_buffer(contents, block_size=blocks_len)
        c_fills = Block._normalize_fill_colors(c_fills, block_size=blocks_len)
        c_texts = Block._normalize_text_colors(c_texts, c_stroke, c_fills, block_size=blocks_len)

        contents = chunk_bytes(contents, block_size)
        c_fills = chunk_bytes(c_fills, block_size)
        c_texts = chunk_bytes(c_texts, block_size)
        anims = [Rewrite(*args, rev=rev, lag_ratio=lag_ratio_h) for args in zip(blocks, contents, c_fills, c_texts)]
        if rev: anims = anims[::-1]
        super().__init__(*anims, lag_ratio=lag_ratio_v, **kwargs)


class PaddingBlockRewrite(BlockRewrite):
    def __init__(self, block: PaddingBlock, contents, **kwargs):
        block.padfunc = kwargs.pop("padfunc", block.padfunc)
        copied = block.copy().rewrite(contents)
        block.msg_len, block.pad_len = copied.msg_len, copied.pad_len  # TODO FIXME there's an ugly detail here. these aren't automatically updated because we aren't actually calling rewrite() on our block. propagating side effects is ugly; how can we fix that? should we refactor side effects out of rewrite()?
        super().__init__(block, copied.bs, copied.c_fills, **kwargs)


class ECBBlockRewrite(AnimationGroup):
    def __init__(self, ecb, contents, c_pt=None, c_ct=None, **kwargs):
        rewrite_pt = Rewrite(ecb.pt, contents, c_fills=c_pt, **kwargs)
        rewrite_ct = Rewrite(ecb.ct, _enc(contents), c_fills=c_ct, **kwargs)
        super().__init__(
            rewrite_pt,
            FlowThru(ecb.pt_to_enc, ecb.enc, ecb.enc_to_ct, run_time=1.5, lag_ratio=2/3),
            rewrite_ct,
            lag_ratio=0.7,
        )


class CBCBlockRewrite(AnimationGroup):
    def __init__(self, cbc, contents, c_pt=None, c_ct=None, pt_kwargs=None, ct_kwargs=None, lag_ratio=0.6, **kwargs):
        # TODO FIXME doesn't work for CBCBlock(dec=True)
        pt_kwargs = pt_kwargs or {}
        ct_kwargs = ct_kwargs or {}
        flow_from_pt = True
        anims = [
            Rewrite(cbc.pt, contents, c_fills=c_pt, **pt_kwargs),
        ]

        while cbc is not None:
            if flow_from_pt:
                anims.append(FlowThru(cbc.pt_to_xor, run_time=0.3))
                flow_from_pt = False
            else:
                anims.append(FlowThru(getattr(cbc, 'ct_to_xor', getattr(cbc, 'iv_to_xor', None)), run_time=1.5))
            anims.append(FlowThru(cbc.xor, cbc.xor_to_enc, cbc.enc, cbc.enc_to_ct, lag_ratio=0.5, run_time=1.2))
            anims.append(Rewrite(cbc.ct, cbc._get_ct(), c_fills=c_ct, **ct_kwargs))
            cbc = cbc.next

        #if propagate:
            #while (cbc := cbc.next) is not None:
                #anims.extend(Rewrite(cbc, flow_from_pt=False, flow_from_chain=True, propagate=False, lag_ratio=0).animations)

        super().__init__(*anims, lag_ratio=lag_ratio, **kwargs)


class CodeRewrite(AnimationGroup):
    def __init__(self, old_code, new_code, lag_ratio=0.75, bg_ratefunc=rate_functions.running_start, **kwargs):
        self.to_remove = [old_code]
        self.to_add = new_code
        fg_anims = self.get_fg_anims(old_code, new_code, lag_ratio)
        bg_anim = self.get_bg_anim(old_code, new_code, bg_ratefunc, fg_anims.run_time)
        super().__init__(bg_anim, fg_anims, **kwargs)
        self._on_finish

    def get_bg_anim(self, old_code, new_code, ratefunc, run_time):
        old_bg = old_code.background_mobject
        new_bg = new_code.background_mobject

        # we want to resize old_bg to new_bg's dimensions without distorting any buttons it may contain
        if isinstance(old_bg, SurroundingRectangle):  # simple background
            assert isinstance(new_bg, SurroundingRectangle)
            return old_bg.animate(run_time=run_time, rate_func=ratefunc).match_width(new_bg).match_height(new_bg).align_to(old_code, UL)
        else:
            old_rect, new_rect = old_bg[0], new_bg[0]  # NOTE: fragile - might be better to filter submobjects for RoundedRectangles
            assert isinstance(old_rect, RoundedRectangle) and isinstance(new_rect, RoundedRectangle)
            old_btns, new_btns = old_bg[1], new_bg[1]
            assert isinstance(old_btns, VGroup) and isinstance(new_btns, VGroup)
            self.to_remove += [old_rect, old_btns]
            return AnimationGroup(
                old_rect.animate.stretch_to_fit_width(new_rect.get_width()).stretch_to_fit_height(new_rect.get_height()).align_to(new_rect, UL),
                old_btns.animate.become(new_btns),
                run_time=run_time,
                rate_func=ratefunc,
            )

    def get_fg_anims(self, old_code, new_code, lag_ratio):
        # get and split code strings
        old_text, new_text = old_code.code_string, new_code.code_string
        old_lines, new_lines = old_text.split('\n'), new_text.split('\n')

        # compute code diff (ignoring horizontal and vertical whitespace)
        cs_1 = [stripped for line in old_lines if len(stripped := line.strip()) > 0]
        cs_2 = [stripped for line in new_lines if len(stripped := line.strip()) > 0]
        diff = [line for line in Differ().compare(cs_1, cs_2) if not line.startswith("?")]
        assert all(line.startswith(("+", "-", " ")) for line in diff)

        # get indices (in cs_1, cs_2) of lines to drop, add, and zip
        old_to_drop, new_to_add, old_to_zip, new_to_zip = [], [], [], []
        for i, line in enumerate(line for line in diff if not line.startswith("+")):
            if line.startswith("-"):
                old_to_drop.append(i)
            elif line.startswith(" "):
                old_to_zip.append(i)
        for i, line in enumerate(line for line in diff if not line.startswith("-")):
            if line.startswith("+"):
                new_to_add.append(i)
            elif line.startswith(" "):
                new_to_zip.append(i)

        # adjust indices to compensate for empty lines
        for lines, to_drop, to_zip in ((old_lines, old_to_drop, old_to_zip),
                                       (new_lines, new_to_add, new_to_zip)):
            for i, line in enumerate(lines):
                if len(line.strip()) == 0:
                    to_drop[:] = tuple(j+1 if j >= i else j for j in to_drop)
                    to_zip[:] = tuple(j+1 if j >= i else j for j in to_zip)

        # get per-line VGroups
        old_chars = [remove_invisible_chars(line) if len(line) > 0 else line for line in old_code.code.chars]
        new_chars = [remove_invisible_chars(line) if len(line) > 0 else line for line in new_code.code.chars]

        # get animations
        drop_anims = [FadeOut(old_chars[i]) for i in old_to_drop]
        add_anims = [FadeIn(new_chars[i]) for i in new_to_add]
        zip_anims = [Transform(old_chars[i], new_chars[j]) for i, j in zip(old_to_zip, new_to_zip)]
        self.to_remove += [anim.mobject for anim in add_anims + zip_anims]
        return AnimationGroup(
            AnimationGroup(*drop_anims),
            AnimationGroup(*zip_anims),
            AnimationGroup(*add_anims),
            lag_ratio=lag_ratio
        )

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(*self.to_remove)
        scene.add(self.to_add)
        return super().clean_up_from_scene(scene)
