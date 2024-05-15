from manim import *
from .zoom import *
from .colors import *
from .named import *


@zoomable
class BendyArrow(Line):
    def __init__(self, mob_from, side_from, mob_to, side_to, start_margin=0, end_margin=0.01, offset_ratio=0.5, add_tip=True, tip_shape=None, tip_length=0.17, tip_width=0.17, color=C_STROKE, *args, **kwargs):
        start = mob_from.get_edge_center(side_from) + start_margin*side_from
        end = mob_to.get_edge_center(side_to) + end_margin*side_to

        match list(side_from), list(side_to):
            case [0, 1 | -1, 0], [0, 1 | -1, 0]:  # CASE: from top or bottom, to top or bottom
                mid_y = (1-offset_ratio)*start[1] + offset_ratio*end[1]   # y-align between start and end
                mid = [(start[0], mid_y, 0),      # x-align two points: one for start, one for end
                       (end[0], mid_y, 0)]
            case [0, 1 | -1, 0], [1 | -1, 0, 0]:  # CASE: from top or bottom, to left or right
                mid = [(start[0], end[1], 0)]     # x-align with start, y-align with end

            case [1 | -1, 0, 0], [1 | -1, 0, 0]:  # CASE: from left or right, to left or right
                mid_x = (1-offset_ratio)*start[0] + offset_ratio*end[0]   # x-align between start and end
                mid = [(mid_x, start[1], 0),          # y-align two points: one for start, one for end
                       (mid_x, end[1], 0)]
            case [1 | -1, 0, 0], [0, 1 | -1, 0]:  # CASE: from left or right, to top or bottom
                mid = [(end[0], start[1], 0)]     # y-align with start, x-align with end
            case _:
                raise ValueError

        if len(mid) == 2 and mid[0] == mid[1]:
            mid = [mid[0]]

        # draw multipart line
        # we have to start with the last segment of the line, then add the tip,
        # then add the rest of the line, or else adding the tip will throw
        # everything off skew (strange but true)
        path = [start, *mid, end]
        super().__init__(*path[-2:], *args, color=color, **kwargs)
        if add_tip:
            self.add_tip(tip_shape=tip_shape, tip_length=tip_length, tip_width=tip_width)
        self.set_points_as_corners(path)


@zoomable
class FuncBox(VMobject):
    def __init__(self, func_name, rect_kwargs=None, text_kwargs=None, c_fill=C_BOX_BG, c_text=None, c_stroke=C_STROKE, mathtex=True, buff=SMALL_BUFF, **kwargs):
        super().__init__(color=c_fill, **kwargs)

        if c_text is None:
            c_text = c_stroke if c_fill==C_BOX_BG else C_BOX_BG
        text_kwargs = {
            "color": c_text,
            **(text_kwargs or {})
        }
        text = self.text = (MathTex if mathtex else Tex)(func_name, **text_kwargs)

        rect_kwargs = {
            'width': max(0.75, text.width + 2*buff),
            'height': max(0.75, text.height + 2*buff),
            'fill_color': c_fill,
            'stroke_color': c_stroke,
            'fill_opacity': 1.0,
            **(rect_kwargs or {})
        }
        box = self.box = Rectangle(**rect_kwargs)
        #text.move_to(box)
        self.add(box, text)

    def write_anim(self):
        return AnimationGroup(FadeIn(self.box), Write(self.text))

    def unwrite_anim(self):
        return AnimationGroup(FadeOut(self.box, self.text))

    def get_arrows(self, input_info, output_info, color=C_STROKE, include_src_arrow=False, include_dst_arrow=True, **kwargs):
        src, src_side, src_box_side = input_info
        dst, dst_box_side, dst_side = output_info
        arrow_1 = BendyArrow(src, src_side, self, src_box_side, add_tip=include_src_arrow, color=color, **kwargs)
        arrow_2 = BendyArrow(self, dst_box_side, dst, dst_side, add_tip=include_dst_arrow, color=color, **kwargs)
        return VGroup(arrow_1, arrow_2)

    @staticmethod
    def _normalize_info(info):
        return list(info) if isinstance(info, list | tuple) else [info, DOWN, UP]

    @classmethod
    def with_arrows(cls, input_info, output_info, *args, include_src_arrow=False, include_dst_arrow=True, **kwargs):
        input_info = cls._normalize_info(input_info)
        output_info = cls._normalize_info(output_info)

        box = cls(*args, **kwargs)
        src, src_side, _ = input_info
        dst, _, dst_side = output_info
        pos = (src.get_edge_center(src_side) + dst.get_edge_center(dst_side)) / 2
        box.move_to(pos)

        arrows = box.get_arrows(input_info, output_info, kwargs.get("stroke_color", C_STROKE), include_src_arrow, include_dst_arrow)
        return NamedVGroup({"arrow_to": arrows[0], "box": box, "arrow_from": arrows[1]})


class EncBox(FuncBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, func_name="E_k", **kwargs)


class DecBox(FuncBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, func_name="D_k", **kwargs)


class FlowThru(AnimationGroup):
    # for e.g. indicating flows of information through arrows in wire diagrams
    def __init__(self, *shapes, weight=5, time_width=0.2, lag_ratio=0.9, box_time_fac=0.75, scale=1.4, **kwargs):
        anims = []
        run_time = kwargs.get("run_time", 1.0)
        num_funcs = 0
        # first pass: determine total path length
        path_len = 0
        for shape in shapes:
            new_stroke = shape.get_stroke_width() + weight
            new_shape = shape.copy()
            if hasattr(new_shape, "tip"):  # don't include arrow tips (they look bad)
                new_shape.remove(new_shape.tip)
            if isinstance(shape, FuncBox):
                num_funcs += 1
            else:
                path_len += new_shape.get_arc_length()

        path_len += box_time_fac * num_funcs

        # second pass: make animations (with scaled runtimes)
        for shape in shapes:
            new_stroke = shape.get_stroke_width() + weight
            new_shape = shape.copy().set_stroke(width=new_stroke)
            if hasattr(new_shape, "tip"):  # don't include arrow tips (they look bad)
                new_shape.remove(new_shape.tip)
            shape_len = box_time_fac if isinstance(shape, FuncBox | XOR) else new_shape.get_arc_length()
            anim_time = run_time * shape_len / path_len
            if isinstance(shape, FuncBox | XOR):
                anim = Wiggle(shape, run_time=anim_time, n_wiggles=2, scale_value=scale)
            else:
                anim = ShowPassingFlash(new_shape, time_width=time_width, run_time=anim_time)
            anims.append(anim)
        super().__init__(*anims, lag_ratio=lag_ratio, **kwargs)


@zoomable
class XOR(VMobject):
    def __init__(self, *args, radius=1/6, color=C_STROKE, **kwargs):
        # could also do this with MathTex(r"\oplus"), but then it would scale as text instead of scaling alongside arrows etc
        super().__init__(*args, **kwargs)
        circle = Circle(radius)
        hor = Line(circle.get_edge_center(LEFT), circle.get_edge_center(RIGHT))
        ver = Line(circle.get_edge_center(UP), circle.get_edge_center(DOWN))
        self.add(hor, ver, circle)
        self.set_color(color)
