from manim_cranim import *
import pytest


def test_byte_box_basics():
    # super basic initialization stuff
    box = ByteBox()
    assert box.b is None
    assert box.byte == ''
    assert isinstance(box.text, MathTex)
    assert box.text.tex_string == r''
    assert box.old_text is None
    assert box.c_fill == C_BOX_BG
    assert box.c_text == C_STROKE
    assert box.escape == True
    assert len(box.submobjects) == 2

    # rewriting empty byte
    box.rewrite(b'\xFF')
    assert box.b == b'\xFF'
    assert box.byte == 'ff'
    assert isinstance(box.text, MathTex)
    assert box.text.tex_string == r'\texttt{ff}'
    assert isinstance(box.old_text, MathTex)
    assert box.old_text.tex_string == r''

    # rewriting again
    box.rewrite(0xAA, c_fill=RED, c_text=BLACK)
    assert box.b == 0xAA
    assert box.byte == 'aa'
    assert isinstance(box.text, MathTex)
    assert box.text.tex_string == r'\texttt{aa}'
    assert box.c_fill == RED
    assert box.c_text == BLACK


def test_byte_box_with_contents():
    # try nonempty initialization
    box = ByteBox('hi', c_fill=RED, c_stroke=BLACK, c_text=BLACK)
    assert box.b == 'hi'
    assert box.byte == 'hi'
    assert isinstance(box.text, MathTex)
    assert box.text.tex_string == r'\texttt{hi}'
    assert box.old_text is None
    assert box.c_fill == RED
    assert box.c_stroke == BLACK
    assert box.c_text == BLACK
    assert box.escape == True
    assert len(box.submobjects) == 2


def test_byte_box_bad_contents():
    # try some bad inputs
    with pytest.raises(ValueError):
        ByteBox(b'aaaa')
    with pytest.raises(ValueError):
        ByteBox([])   # type: ignore
    with pytest.raises(ValueError):
        ByteBox({})   # type: ignore
    with pytest.raises(ValueError):
        ByteBox(fill_color=17)


def test_block_basics():
    # initialization
    block = Block()
    assert block.block is None
    assert block.bs == ('',) * 16
    assert block.block_size == 16
    assert block.c_fills == [C_BOX_BG]*16
    assert block.c_texts == [C_STROKE]*16
    assert block.c_stroke == C_STROKE

    # rewrite
    block.rewrite(bytes(16))
    assert block.block == bytes(16)
    assert block.bs == ('00',) * 16
    assert block.bytes == bytes(16)
    assert block.c_fills == [C_BOX_BG]*16
    assert block.c_texts == [C_STROKE]*16
    assert block.c_stroke == C_STROKE

    # rewrite again
    block.rewrite(range(16), c_texts=WHITE)
    assert block.block == range(16)
    assert block.bs == tuple(hex(i)[2:].rjust(2, '0') for i in range(16))  # ('00', '01', ..., '09', '0a', ...)
    assert block.bytes == bytes(range(16))
    assert block.c_fills == [C_BOX_BG]*16
    assert block.c_texts == [WHITE]*16
    assert block.c_stroke == C_STROKE

    # make sure the block size check works
    with pytest.raises(BlockSizeError):
        block.rewrite(bytes(17))
    assert block.block == bytes(17)  # most recent input block still gets stored here even if there's an error (but no other fields are updated)
    assert block.bs == tuple(hex(i)[2:].rjust(2, '0') for i in range(16))  # ('00', '01', ..., '09', '0a', ...)
    assert block.bytes == bytes(range(16))
    assert block.c_fills == [C_BOX_BG]*16
    assert block.c_texts == [WHITE]*16
    assert block.c_stroke == C_STROKE

    # initialization
    block = Block(block_size=32)
    assert block.block is None
    assert block.bs == ('',) * 32
    assert block.block_size == 32
    assert block.c_fills == [C_BOX_BG]*32
    assert block.c_texts == [C_STROKE]*32
    assert block.c_stroke == C_STROKE

    # rewrite
    block.rewrite(bytes(32))
    assert block.block == bytes(32)
    assert block.bs == ('00',) * 32
    assert block.c_fills == [C_BOX_BG]*32
    assert block.c_texts == [C_STROKE]*32
    assert block.c_stroke == C_STROKE

    # rewrite again
    block.rewrite(range(32), c_texts=WHITE)
    assert block.block == range(32)
    assert block.bs == tuple(hex(i)[2:].rjust(2, '0') for i in range(32))  # ('00', '01', ..., '09', '0a', ...)
    assert block.c_fills == [C_BOX_BG]*32
    assert block.c_texts == [WHITE]*32
    assert block.c_stroke == C_STROKE

    # make sure the block size check works
    with pytest.raises(BlockSizeError):
        block.rewrite(bytes(17))
    assert block.block == bytes(17)
    assert block.bs == tuple(hex(i)[2:].rjust(2, '0') for i in range(32))  # ('00', '01', ..., '09', '0a', ...)
    assert block.c_fills == [C_BOX_BG]*32
    assert block.c_texts == [WHITE]*32
    assert block.c_stroke == C_STROKE


def test_padding_block_basics():
    pb = PaddingBlock()
    assert pb.block == pb.bs == ('10',) * 16
    #assert pb.bs == ('0f',) * 16
    assert pb.bytes == bytes([16]*16)
    assert pb.block_size == 16
    assert pb.c_fills == [C_PAD]*16
    assert pb.c_texts == [C_STROKE]*16
    assert pb.c_stroke == C_STROKE

    pb.rewrite(bytes(8))
    assert pb.block == pb.bs == ('00',)*8 + ('08',)*8
    assert pb.bytes == bytes([0]*8 + [8]*8)
    assert pb.block_size == 16
    assert pb.c_fills == [C_PT]*8 + [C_PAD]*8
    assert pb.c_texts == [C_STROKE]*16
    assert pb.c_stroke == C_STROKE

    pb.rewrite(bytes(12))
    assert pb.block == pb.bs == ('00',)*12 + ('04',)*4
    assert pb.bytes == bytes([0]*12 + [4]*4)
    assert pb.block_size == 16
    assert pb.c_fills == [C_PT]*12 + [C_PAD]*4
    assert pb.c_texts == [C_STROKE]*16
    assert pb.c_stroke == C_STROKE

    with pytest.raises(BlockSizeError):
        pb.rewrite(bytes(16))
    with pytest.raises(BlockSizeError):
        pb.rewrite(bytes(17))
    assert pb.block == pb.bs == ('00',)*12 + ('04',)*4
    assert pb.bytes == bytes([0]*12 + [4]*4)
    assert pb.block_size == 16
    assert pb.c_fills == [C_PT]*12 + [C_PAD]*4
    assert pb.c_texts == [C_STROKE]*16
    assert pb.c_stroke == C_STROKE


def test_blocks_basics():
    # no padding
    blocks = Blocks(bytes(16))
    assert blocks.bytes == bytes(16)
    blocks.rewrite(b'\xff'*16)
    assert blocks.bytes == b'\xff'*16

    # w/ padding
    blocks = Blocks(bytes(30))
    assert blocks.bytes == bytes(30) + b'\x02\x02'
    blocks.rewrite(bytes(31))
    assert blocks.bytes == bytes(31) + b'\x01'
    blocks.rewrite(bytes(17))
    assert blocks.bytes == bytes(17) + b'\x0f'*15

    # w/ ascii input
    blocks = Blocks("this is a message with length 32")
    # TODO validate attrs

    # w/ padding and ascii input
    blocks = Blocks("this is an odd-sized message of length 41")
    # TODO validate attrs
