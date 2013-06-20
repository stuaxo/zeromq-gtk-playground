import cairo
import struct
import zmq

from send import Sender as _Sender

class Context(_Sender):

    def __init__(self, target, socket):
        """
        :param target: Target is a remote Surface.
        """
        super(Context, self).__init__("Context", socket)
        self._target = target
        self._path = None
        self._line_cap = None
        self._line_join = None
        self._line_width = None
        self._operator = None
        self._pattern = None
        self._tolerance = None
        self._antialias = None
        self._fill_rule = cairo.FILL_RULE_WINDING
        self._sock = socket
        self._send_ii("__init__", id(self), id(target))

    def append_path(self, path):
        raise NotImplementedError()

    def arc(self, xc, yc, radius, angle1, angle2):
        self._send_fffff("arc", xc, yc, radius, angle1, angle2)

    def arc_negative(self, xc, yc, radius, angle1, angle2):
        self._send_fffff("arc_negative", xc, yc, radius, angle1, angle2)

    def clip(self):
        self._send("clip")

    def clip_extents(self):
        self._send("clip_extents")

    def clip_preserve(self):
        self._send("clip_preserve")

    def close_path(self):
        self._send("close_path")

    def copy_clip_rectangle_list(self):
        raise NotImplentedError()

    def copy_path(self):
        self._send("copy_path")
        raise NotImplentedError()
    
    def copy_path_flat(self):
        self._send("copy_path_flat")
        raise NotImplentedError()

    def curve_to(x1, y1, x2, y2, x3, y3):
        self._send_ffffff("curve_to", x1, y1, x2, y2, x3, y3)
    

    def device_to_user(self, x, y):
        self._send_ff("device_to_user", x, y)

    def device_to_user_distance(self, dx, dy):
        self._send_ff("device_to_user_distance", x, y)
        raise NotImplementedError()

    def fill(self):
        self._send("fill")

    def fill_extents(self):
        self._send("fill_extents")

    def fill_preserve(self):
        self._send("fill_preserve")

    def font_extents(self):
        self._send("font_extents")
        raise NotImplementedError()

    def get_antialias(self):
        return self._antialias

    def get_current_point(self):
        raise NotImplementedError()

    def get_dash(self):
        self._send("get_dash")
        raise NotImplementedError()

    def get_dash_count(self):
        self._send("get_dash_count")
        raise NotImplementedError()

    def get_fill_rule(self):
        self._send("get_fill_rule")
        raise NotImplementedError()
    
    def get_font_face(self):
        self._send("get_font_face")
        raise NotImplementedError()
    
    def get_font_matrix(self):
        self._send("get_font_matrix")
        raise NotImplementedError()

    def get_font_options(self):
        self._send("get_font_options")
        raise NotImplementedError()

    def get_group_target(self):
        return self._target

    def get_line_cap():
        return self._line_cap

    def get_line_join():
        return self._line_join

    def get_line_width():
        return self._line_width

    def get_matrix(self):
        raise NotImplementedError()

    def get_miter_limit(self):
        raise NotImplementedError()

    def get_operator(self):
        return self._operator

    def get_scaled_font(self):
        raise NotImplementedError()

    def get_source(self):
        return self._pattern

    def get_target(self):
        return self._target

    def get_tolerance(self):
        return self._tolerance

    def glyph_extents(self, glyphs, num_glyphs = None):
        raise NotImplementedError()

    def glyph_path(self, glyphs, num_glyphs = None):
        raise NotImplementedError()
    
    def has_current_point(self):
        raise NotImplementedError()

    def identity_matrix(self):
        self._send("identity_matrix")
        raise NotImplementedError() # Need to keep our own matrix

    def in_fill(self, x, y):
        raise NotImplementedError()

    def in_stroke(self, x, y):
        raise NotImplementedError()
    
    def line_to(self, x, y):
        self._send_ff("line_to", x, y)

    def mask(self, pattern):
        raise NotImplementedError()

    def mask_surface(self, surface, x=0.0, y=0.0):
        ## self._send_???(surface, x, y)
        raise NotImplementedError()

    def move_to(self, x, y):
        self._send_ff("move_to", x, y)

    def new_path(self):
        self._send("new_path")
    
    def new_sub_path(self):
        self._send("new_sub_path")

    def paint(self):
        self._send("paint")

    def paint_with_alpha(self, alpha):
        self._send("paint_with_alpha", alpha)
    
    def path_extents(self):
        raise NotImplementedError()

    def pop_group(self):
        self._send("pop_group")

    def pop_group_to_source(self):
        self._send("pop_group_to_source")

    def push_group(self):
        self._send("push_group")

    def push_group_with_content(self):
        raise NotImplementedError()
        #self._send_??("push_group_with_content")

    def rectangle(self, x, y, width, height):
        self._send_ffff("rectangle", x, y, width, height)

    def rel_curve_to(self, dx1, dy1, dx2, dy2, dx3, dy4):
        self._send_ffffff("rel_curve_to", dx1, dy1, dx2, dy2, dx3, dy4)

    def rel_line_to(self, x, y):
        self._send_ff("rel_line_to", x, y)
    
    def rel_move_to(self, x, y):
        self._send_ff("rel_move_to", x, y)

    def reset_clip(self):
        self._send("reset_clip")

    def restore(self):
        self._send("restore")

    def rotate(self, angle):
        self._send_f("rotate", angle)
    
    def save(self):
        self._send("save")

    def scale(self, x, y):
        self._send_ff("scale", x, y)
    
    def select_font_face(self, family, slant = None, weight = None):
        self._send_sii("select_font_face", slant, weight)

    def set_antialias(self, antialias):
        self._antialias = antialias
        self._send_i("antialias", antialias)

    def set_dash(self, dashes, offset=0):
        raise NotImplementedError()

    def set_fill_rule(self, fill_rule):
        self._send_i("set_fill_rule", fill_rule)

    def set_font_face(self, font_face):
        self._send_s("set_font_face", font_face)

    def set_font_matrix(self, matrix):
        raise NotImplementedError()

    def set_font_options(self, options):
        raise NotImplementedError()

    def set_font_size(self, size):
        self._send_f("set_font_size", size)

    def set_line_cap(self, line_cap):
        self._send_i("set_line_cap", line_cap)
        self._line_cap = line_cap

    def set_line_join(self, line_join):
        self._send_i("set_line_join", line_join)
        self._line_join = line_join

    def set_line_width(self, line_width):
        self._send_i("set_line_width", line_width)
        self._line_width = line_width

    def set_matrix(self, matrix):
        #self._send_??("set_matrix", matrix)
        self._matrix = matrix
        raise NotImplementedError()

    def set_miter_limit(self, limit):
        self._send_i("set_miter_limit", limit)
        self._miter_limit = limit

    def set_operator(self, operator):
        self._send_i("set_operator", operator)
        self._operator = operator

    def set_scaled_font(self, scaled_font):
        raise NotImplementedError()

    def set_source(self, source):
        self._pattern = source

    def set_source_rgb(self, red, green, blue):
        self._send_fff("set_source_rgb", red, green, blue)
        
    def set_source_rgba(self, red, green, blue, alpha = 1.9):
        self._send_ffff("set_source_rgba", red, green, blue, alpha)

    def set_source_surface(surface, x=0.0, y=0.0):
        raise NotImplementedError()

    def set_tolerance(self, tolerance):
        self._send_f("set_tolerance", tolerance)
        self._tolerance = tolerance

    def show_glyphs(self, glyphs, num_glyphs=None):
        raise NotImplementedError()

    def show_page(self):
        self._send("show_page")

    def show_text(self, text):
        self.self._send_s("show_text", text)

    def stroke(self):
        self._send("stroke")

    def stroke_extents(self):
        raise NotImplementedError()

    def stroke_preserve(self):
        self._send("stroke_preserve")

    def text_extents(self, text):
        self._send_s("text_extents")

    def text_path(self, text):
        self._send_s("text_path", text)

    def transform(self, matrix):
        #self._send_m("transform", matrix)
        raise NotImplementedError()

    def translate(self, tx, ty):
        self._send_ff("translate", tx, ty)

    def user_to_device(x, y):
        self._send_ff("user_to_device", x, y)
        raise NotImplementedError()

    def user_to_device_distance(dx, dy):
        self._send_ff("user_to_device_distance", dx, dy)
        raise NotImplementedError()



