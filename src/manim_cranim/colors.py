from manim import DARKER_GRAY
from manim.utils.color import interpolate_color, color_to_rgb, rgb_to_hex

# default fg and bg colors
C_BOX_BG = "#fcf6f2"  # default background of boxes
C_SCENE_BG = "#ece6e2"  # default background of the actual scene
C_STROKE = DARKER_GRAY
C_FILL = "#171717"

# colors from colorblind-friendly palette by Bang Wong. links:
# https://www.nature.com/articles/nmeth.1618
# https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
BW_GOLD = "#E69F00"
BW_SKYBLUE = "#56B4E9"
BW_GREEN = "#009E73"  # bluish green
BW_YELLOW = "#F0E442"
BW_BLUE = "#0072B2"
BW_ORANGE = "#D55E00"
BW_MAUVE = "#CC79A7"


C_IV = BW_GOLD
C_PAD = BW_SKYBLUE
C_PT = BW_GREEN
C_CT = BW_ORANGE
C_MAC = BW_MAUVE


def color_to_hex(color):
    # why doesn't manim have this built-in?
    return rgb_to_hex(color_to_rgb(color))

def lighten(color, amount=0.2):
    return color_to_hex(interpolate_color(color, "#FFFFFF", amount))
def darken(color, amount=0.15):
    return color_to_hex(interpolate_color(color, "#000000", amount))
