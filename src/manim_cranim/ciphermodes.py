from manim import *
from numpy import ndarray
from .zoom import *
from .buffers import *
from .funcs import *
from .util import _enc
from .types import *
from collections.abc import Iterable


@zoomable
class ECBBlock(VGroup):
    def __init__(self, msg: Block | BS_TYPE = None, buff=1, direction=DOWN, c_pt=C_PT, c_ct=C_CT, block_size=16, *args, **kwargs):
        # internally, ensure msg is bytes & pt is Block
        if isinstance(msg, Block):
            pt = msg
            msg = pt.bytes
        else:
            pt = Block(msg, c_fills=c_pt, block_size=block_size) if msg is None or len(msg) >= 16 else PaddingBlock(msg, c_msg=c_pt, block_size=block_size)
        bs = pt.bs
        enc_msg = None
        if bs is not None and isinstance(bs, Iterable) and None not in bs:  # TODO should we check against list or against an iterable ABC?
            enc_msg = self._enc_msg(pt.bytes)
        enc = EncBox().scale(0.7)
        ct = Block(enc_msg, c_fills=c_ct, block_size=block_size)

        VGroup(pt, enc, ct).arrange(direction, buff=buff)

        pt_to_enc = BendyArrow(pt, direction, enc, -direction, add_tip=False)
        enc_to_ct = BendyArrow(enc, direction, ct, -direction)

        mobjs = {'pt': pt, 'enc': enc, 'ct': ct,
                 'pt_to_enc': pt_to_enc, 'enc_to_ct': enc_to_ct}

        for name, mobj in mobjs.items():
            setattr(self, name, mobj)

        super().__init__(*mobjs.values(), *args, **kwargs)

    @staticmethod
    def _enc_msg(msg):
        msg_blank = msg is None or (isinstance(msg, list | tuple) and None in msg)
        enc_msg = None
        if not msg_blank:
            enc_msg = _enc(msg)
        return enc_msg


@zoomable
class ECBBlocks(VGroup):
    def __init__(self, msg, *args, pbuff=0.5, block_size=16, direction=RIGHT, **kwargs):
        # TODO make non-default block_size actually work (requires passing to ECBBlock)
        self.block_size = block_size
        msg = self._to_blocks(msg)
        self.blocks = blocks = [ECBBlock(block, *args, block_size=block_size, direction=direction, **kwargs) for block in msg]
        super().__init__(*blocks)
        self.arrange(DOWN if direction is RIGHT else RIGHT, buff=pbuff)  # type: ignore  # TODO fix manim's annotation

    def rewrite(self, msg, *args, **kwargs):  # TODO add support for per-block c_fills etc
        msg = self._to_blocks(msg)
        for ecb_block, msg_block in zip(self.blocks, msg):
            ecb_block.rewrite(msg_block, *args, **kwargs)

    def _to_blocks(self, msg):
        return chunk_bytes(msg.bytes if isinstance(msg, Block) else msg, self.block_size)

    @property
    def pt(self):
        return Blocks.from_blocks(*[block.pt for block in self.blocks])

    @property
    def ct(self):
        return Blocks.from_blocks(*[block.ct for block in self.blocks])


@zoomable
class CBCBlock(VGroup):
    def __init__(self, msg=None, iv=None, prev=None, c_pt=C_PT, c_ct=C_CT, buff=1, margin=2, direction: ndarray=RIGHT, show_pad_bytes=True, padfunc=PaddingBlock._get_padding, dec=False, *args, **kwargs):
        # TODO FIXME refactor into helper mathods
        self.prev = prev
        if prev is not None:
            prev.next = self
        self.next = None

        msg_blank = msg is None or (isinstance(msg, list) and None in msg)  # TODO should we check against list or against an iterable ABC?

        if prev is not None:
            try:
                iv = bytes.fromhex(''.join(prev.ct.bs))
            except TypeError:
                pass
        if iv is None and not msg_blank: iv = blk()

        iv_blank = iv is None or (isinstance(iv, list) and None in iv)

        enc_msg = None
        if not (msg_blank or iv_blank):
            #msg = Block._normalize_buffer(msg)
            #iv = Block._normalize_buffer(iv)
            enc_msg = _enc(bytes_xor(msg, iv))

        # TODO FIXME block size hardcoded here :(
        pt = Block(msg, c_fills=c_pt) if msg is None or len(msg) >= 16 \
             else PaddingBlock(msg, c_msg=c_pt, padfunc=padfunc if show_pad_bytes else lambda l: [None]*l)
        xor = XOR(stroke_width=2)
        func = (DecBox if dec else EncBox)().scale(0.7)
        ct = Block(enc_msg, c_fills=c_ct)

        perp_dir = DOWN if direction is RIGHT or direction is LEFT else RIGHT
        main_group = VGroup(pt, xor, func, ct).arrange(perp_dir, buff=buff)  # type: ignore
        self.main_group = main_group

        block_margin = margin*direction
        if direction is UP or direction is DOWN:
            block_margin *= 2

        if prev is not None:
            align_side = UP if (direction is RIGHT or direction is LEFT) else LEFT
            main_group.next_to(prev, block_margin).align_to(prev, align_side)

        pt_to_xor = self.bendy_arrow(pt, perp_dir, xor, -perp_dir, rev=dec)
        xor_to_enc = self.bendy_arrow(xor, perp_dir, func, -perp_dir, rev=dec)
        enc_to_ct = self.bendy_arrow(func, perp_dir, ct, -perp_dir, rev=dec)

        mobjs = {'pt': pt, 'xor': xor, 'enc': func, 'ct': ct, 'pt_to_xor':
                pt_to_xor, 'xor_to_enc': xor_to_enc, 'enc_to_ct': enc_to_ct}

        if prev is None:
            if direction is RIGHT:
                iv_dir_1 = UP
                iv_dir_2 = LEFT
            elif direction is DOWN:
                iv_dir_1 = LEFT
                iv_dir_2 = UP
            elif direction is LEFT:
                iv_dir_1 = UP
                iv_dir_2 = RIGHT
            else:  #  direction is UP
                iv_dir_1 = UP
                iv_dir_2 = DOWN

            iv_block = Block(iv, c_fills=C_IV)
            mobjs['iv'] = iv_block
            iv_block.next_to(ct, -block_margin)
            iv_to_xor = self.bendy_arrow(iv_block, iv_dir_1, xor, iv_dir_2)
            mobjs['iv_to_xor'] = iv_to_xor
        else:
            if direction is RIGHT or direction is LEFT:
                # construct helpers for final line
                helper_pt = Point((prev.ct.get_edge_center(direction) + ct.get_edge_center(-direction)) / 2 + DOWN)
                ct_to_xor_1 = self.bendy_arrow(prev.ct, DOWN, helper_pt, -direction, add_tip=False)
                ct_to_xor_2 = self.bendy_arrow(helper_pt, UP, xor, -direction)

                # construct final line
                points = list(ct_to_xor_1.points) + list(ct_to_xor_2.points)
                ct_to_xor_2.set_points_as_corners(points)
                mobjs['ct_to_xor'] = ct_to_xor_2
            else:
                mobjs['ct_to_xor'] = self.bendy_arrow(prev.ct, direction, xor, -direction)

        for name, mobj in mobjs.items():
            setattr(self, name, mobj)
        super().__init__(self.pt,
                         *([self.iv, self.iv_to_xor] if "iv" in mobjs else [self.ct_to_xor]),
                         self.pt_to_xor, self.xor, self.xor_to_enc, self.enc, self.enc_to_ct,
                         self.ct,
                         *args, **kwargs)

        if prev is None:
            self.center()

    @staticmethod
    def bendy_arrow(mob_1, dir_1, mob_2, dir_2, rev=False, **kwargs):
        args_1 = (mob_1, dir_1)
        args_2 = (mob_2, dir_2)
        args = (*args_2, *args_1) if rev else (*args_1, *args_2)
        return BendyArrow(*args, **kwargs)

    def rewrite(self, bs=None, c_pt=C_PT, c_ct=C_CT, chain=True):
        self.pt.rewrite(bs, c_fills=c_pt)  # type: ignore
        self._update_ct(c_ct)
        if chain:
            block = self
            while (block := block.next) is not None:
                block._update_ct(c_ct)
        return self

    def _update_ct(self, c_fills=C_CT):
        self.ct.rewrite(self._get_ct(), c_fills=c_fills)  # type: ignore

    def _get_ct(self, quiet=True):
        assert self.prev is not None or hasattr(self, "iv")
        iv_bytes = self.iv.bytes if hasattr(self, "iv") else self.prev.ct.bytes  # type: ignore
        pt_bytes = self.pt.bytes
        #iv = bytes.fromhex(''.join(iv_bs))
        #pt = bytes.fromhex(''.join(self.pt.bs))  # type: ignore
        ct = _enc(bytes_xor(pt_bytes, iv_bytes, quiet=quiet))
        return ct


@zoomable
class CBCBlocks(VGroup):
    def __init__(self, msg, block_size=16, direction=DOWN, **kwargs):
        # TODO make non-default block_size actually work (requires passing to CBCBlock)
        self.block_size = block_size
        msg = chunk_bytes(msg.bytes if isinstance(msg, Block) else msg, 16)  # NOTE in a perfect world this hardcoded 16 should be block_size
        _cbc = None
        self.blocks = blocks = [
            _cbc := CBCBlock(block, prev=_cbc, direction=direction, **kwargs)
            for block in msg
        ]
        Group(*blocks).center()
        super().__init__(*blocks)

    def rewrite(self, msg, *args, **kwargs):  # TODO add support for per-block c_fills etc
        msg = self._to_blocks(msg)
        for ecb_block, msg_block in zip(self.blocks, msg):
            ecb_block.rewrite(msg_block, *args, **kwargs)

    def _to_blocks(self, msg):
        return chunk_bytes(msg.bytes if isinstance(msg, Block) else msg, self.block_size)
