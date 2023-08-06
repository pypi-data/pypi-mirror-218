from os.path import exists, abspath, dirname, join
from our_browser.listview import draw_listview
import cairo, math
import threading

from our_browser.draw_commons import (
    cr_set_source_rgb_any_hex, cr_set_source_rgb_any_hex_or_simple, hex2color, Scrollable, PRIOR_EVENT_HANDLERS,
    SELECT_CONTROL, HOVERED_NODES
)

DATA_PATH = join(dirname(__file__), 'data')

check_is_drawable = lambda node: node.tag and node.tag.text not in ('style', 'script', 'head', 'items') and not node.tag.text.startswith('!')

DEFAULT_STYLES = {
    'html': {
        'width': 'auto',
        'height': 'auto'
    }
}

class StrBreaked(str):
    _breaked = True

class InputControl:
    focus_into = None
    timer = None
    ending = False
    refresher = None
    text_syncer = None

    def set_refresher(self, func):
        self.refresher = func

    def set_text_syncer(self, func):
        self.text_syncer = func

    def set_focus(self, elem):
        if self.focus_into and self.focus_into != elem:
            self.focus_into.on_focus_lost()
        if not elem:
            self.focus_into = None
            if self.text_syncer:
                self.text_syncer("")
        elif hasattr(elem, 'on_timer'):
            if self.focus_into == elem:
                return
            self.focus_into = elem
            if self.text_syncer:
                text = elem.drawer.node.text
                if text == None:
                    text = ""
                self.text_syncer(text)

        if self.focus_into:
            self.focus_into.on_focus_got()
            self.ending = False
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        if self.ending:
            return
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(0.5, self.on_timer)
        self.timer.start()

    def stop_timer(self):
        if not self.timer:
            return
        self.ending = True
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def on_timer(self):
        if self.focus_into:
            self.focus_into.on_timer()
            self.start_timer()


INPUT_CONTROL = InputControl()

class Event:

    def __init__(self) -> None:
        pass


def make_drawable_tree(parent, drawer=None, with_html=False):

    _drawer = None

    for node in parent.children:
        if not drawer and node.tag and ((with_html and node.tag.text == 'html') or node.tag.text == 'body'):
            drawer = make_drawer(parent, node)

        elif check_is_drawable(node):
            make_drawer(parent, node)

        _drawer = make_drawable_tree(node, drawer, with_html=with_html)

    if not drawer:
        drawer = _drawer

    return drawer


def make_drawer(parent, node):
    style = getattr(node, 'style', None)

    drawer = None
    if style:
        if style.get('display', None) == 'flex':
            drawer = DrawerFlex(node)

        elif style.get('flex', None) != None:
            drawer = DrawerFlexItem(node)

    if not drawer:
        drawer = DrawerBlock(node)

    if drawer:
        if node.tag and node.tag.text == 'input':
            AbilityInput(drawer)

    return drawer


class DrawerNode:

    def __init__(self, node) -> None:
        self.node = node
        node.drawer = self

    def __str__(self) -> str:
        return '_drawer_ ' + str(self.node)

    def __repr__(self) -> str:
        return self.__str__()

    def focus(self):
        if self.node and hasattr(self, 'ability') and type(self.ability) == AbilityInput:
            INPUT_CONTROL.set_focus(self.ability)


class Rect:

    def __init__(self) -> None:
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'rect({self.left}, {self.top}, {self.width}, {self.height})'


def get_size_prop_from_node_or_parent(node, name, parent_prop, default=0):
    _nodes = [node]
    if node.parent:
        _nodes.append(node.parent)
    for n in _nodes:
        v = get_size_prop_from_node(n, name, parent_prop, default=None)
        if v != None:
            return v
    return default


def get_size_prop_from_node(node, name, parent_prop, default=0):
    prop = None
    if hasattr(node, name):
        prop = getattr(node, name)
    else:
        if not hasattr(node, 'style'):
            return 0
        prop = node.style.get(name, default)
    return get_size_prop_from_prop(prop, parent_prop, default)

def get_size_prop_from_prop(prop, parent_prop, default=0):
    if type(prop) == tuple:
        hproc = prop[0]
        if parent_prop == None:
            return default
        prop = hproc * parent_prop / 100.0
    elif type(prop) == str:
        if parent_prop == None:
            return default
        if prop == 'auto':
            prop = parent_prop
        else:
            prop = default
    return prop


def get_int_prop_from_node(node, name, default=None):
    prop = None
    if hasattr(node, name):
        prop = getattr(node, name)
    else:
        if not hasattr(node, 'style'):
            return 0
        prop = node.style.get(name, default)
    return prop


class Calced:

    def __init__(self) -> None:
        self.rect = Rect()
        self.calced = False
        self.last_size_0 = -1

    def calc_params(self, node, size, debug=False):
        background_color = color = border = border_radius = None
        border_left = border_right = border_top = border_bottom = None
        font_size = 11
        display = None
        flex = None
        flex_direction = None
        align_items = None
        justify_content = None
        text_align = None
        vertical_align = None
        position = None
        cursor = None
        if hasattr(node, 'style'):
            color = node.style.get('color', None)
            background_color = node.style.get('background-color', None)
            fs = node.style.get('font-size', None)
            if not fs and node.parent and node.parent.style:
                fs = node.parent.style.get('font-size', 11)
            if not fs:
                fs = 11
            font_size = int(fs)

            border = node.style.get('border', None)
            border_left = node.style.get('border-left', None)
            border_right = node.style.get('border-right', None)
            border_top = node.style.get('border-top', None)
            border_bottom = node.style.get('border-bottom', None)
            border_radius = int(node.style.get('border-radius', 0))

            display = node.style.get('display', None)
            #flex = node.style.get('flex', None)
            flex = get_int_prop_from_node(node, 'flex', default=None)
            flex_direction = node.style.get('flex-direction', None)
            align_items = node.style.get('align-items', None)
            justify_content = node.style.get('justify-content', None)
            text_align = node.style.get('text-align', None)
            vertical_align = node.style.get('vertical-align', None)
            _font_weight_default = 'bold' if node.tag and node.tag.text == 'b' else 'normal'
            self.font_weight = node.style.get('font-weight', _font_weight_default)

            position = node.style.get('position', None)
            cursor = node.style.get('cursor', None)

        self.color = color
        self.background_color = background_color
        self.border_radius = border_radius
        self.font_size = font_size

        self.border = border
        self.border_left = border_left
        self.border_right = border_right
        self.border_top = border_top
        self.border_bottom = border_bottom

        self.display = display
        self.flex = flex
        self.flex_direction = flex_direction
        self.align_items = align_items
        self.justify_content = justify_content
        self.text_align = text_align
        self.vertical_align = vertical_align

        self.position = position
        self.left = get_size_prop_from_node(node, 'left', size[0], 0)
        self.top = get_size_prop_from_node(node, 'top', size[1], 0)
        self.cursor = cursor

        self.padding = padding = get_size_prop_from_node_or_parent(node, 'padding', None)
        padding_2 = padding * 2
        text_width_real = text_width = size[0] - padding_2

        tag = node.tag.text

        image = None
        if tag == 'image':
            image = self.calc_image(node)

        self.max_width = max_width = get_size_prop_from_node(node, 'max-width', None)

        if not hasattr(node, 'lines'):
            node.lines = None
        self.calc_lines_etap = ''
        if node.text:
            if max_width and text_width > max_width:
                self.calc_lines_etap += 'm'
                text_width = max_width
            text_width_real = self.calc_lines(node, font_size, text_width, size)
        else:
            if node.lines:
                node.lines = None

        self.text_width = text_width
        self.text_width_real = text_width_real

        self.margin = margin = get_size_prop_from_node_or_parent(node, 'margin', None)

        width, height = self.calc_width_height(node, size, margin, padding_2, font_size, image)

        self.calc_rect(node, size, width, height, margin)

    def calc_width_height(self, node, size, margin, padding_2, font_size, image):
        height_default = 0
        if node.lines:
            height_default = font_size * len(node.lines) + margin + padding_2
        if image:
            image_height = image.get_height()
            if image_height > height_default:
                height_default = image_height + padding_2

        self._width = width = get_size_prop_from_node(node, 'width', size[0], -1)
        self._height = height = get_size_prop_from_node(node, 'height', size[1], -1) #height_default)

        if height < 0:
            height = height_default

        min_height = get_size_prop_from_node(node, 'min-height', None)
        max_height = get_size_prop_from_node(node, 'max-height', None)

        min_width = get_size_prop_from_node(node, 'min-width', None)

        if min_height > height:
            self._height = height = min_height

        # if max_width > 0 and (max_width < width or width <= 0):
        #     print("~~~~~~~~~~~~ max_width:", max_width, '<', width)
        #     self._width = width = max_width

        if size[1] < height:
            size = (size[0], height)

        self.min_height = min_height

        return width, height

    def calc_lines(self, node, font_size, text_width, size):
        #if node.lines == None or self.last_size_0 < text_width or True: # FIXME
        node.lines = node.text.split('\n')
        lines = node.lines
        font_size_w = self.calc_font_size_w(font_size)
        if text_width > font_size_w:
            self.calc_lines_etap += 'c'
            width_ln = round(text_width / font_size_w)
            i = len(lines) - 1
            max_real_ln = 0
            while i >= 0:
                add_i = i
                while add_i >= 0:
                    self.calc_lines_etap += 'f'
                    add_i, real_ln = self.fix_lines_line_for_ln(lines, add_i, width_ln, text_width, size)
                    if real_ln > max_real_ln:
                        max_real_ln = real_ln
                i -= 1
            if max_real_ln != width_ln:
                self.calc_lines_etap += 'r'
                text_width = round(max_real_ln * font_size_w)
        return text_width

    def fix_lines_line_for_ln(self, lines, i, width_ln, text_width, size):
        line = lines[i]
        ln = len(line)
        # __is_tst = line in ('Edit group', 'Create group')
        # if __is_tst:
        #     print('oOOooO line:', line, 'ln:', ln, 'width_ln:', width_ln, 'text_width:', text_width, 'size:', size)
        if ln > width_ln:
            self.calc_lines_etap += 's'
            ix = line[:width_ln].rfind(' ')
            # if __is_tst:
            #     print('  > oOOooO ix:', ix, 'line[:width_ln]:', line[:width_ln])
            if ix < 0:
                self.calc_lines_etap += 'b'
                return -1, ln
            line_add = line[ix+1:]
            line = line[:ix]
            line = StrBreaked(line)
            lines[i] = line
            add_i = i+1
            lines.insert(add_i, line_add)
            return add_i, width_ln
        return -1, ln

    @classmethod
    def calc_font_size_w(cls, font_size):
        return font_size * 0.46 #/2

    def calc_image(self, node):
        image = None
        self.image = None
        self.image_src = None
        if node.attrs:
            self.image_src = image_src = node.attrs.get('src', None)
            if image_src:
                image_src = abspath(image_src)
            if image_src and exists(image_src):
                image = self.image = cairo.ImageSurface.create_from_png(image_src)
        return image

    def calc_rect(self, node, size, width, height, margin):
        if hasattr(node, 'drawer') and node.level > 2:
            self.rect.width = (width if width >= 0 else size[0]) #- (0 if node.drawer.check_parent_flex() else 2*margin)
            self.rect.height = height
        else:
            self.rect.width = width if width >= 0 else size[0]
            self.rect.height = height

        if self.max_width > 0 and self.rect.width > self.max_width:
            self.rect.width = self.max_width

        if not self.calced:
            self.calced = True


class DrawerBlock(DrawerNode):

    def __init__(self, node) -> None:
        super().__init__(node)
        self.ability = None
        self.calced = Calced()

    def check_parent_flex(self):
        parent = getattr(self.node.parent, 'drawer', None)
        if parent:
            parent_calced = getattr(parent, 'calced', None)
            if parent_calced and getattr(parent_calced, 'display', None) == 'flex':
                return parent

    def calc_size(self, size, pos, pos_parent, debug=False):

        self.calced.calc_params(self.node, size, debug=debug)

        tag = self.node.tag.text if self.node.tag else None

        pos_my = (pos[0] + self.calced.margin, pos[1] + self.calced.margin)
        size_my = (self.calced.rect.width, self.calced.rect.height)

        self.pos = pos_my
        self.size_my = size_my

        parent = self.check_parent_flex()
        if parent:
            align_items = parent.calced.align_items
            if align_items == 'center':
                self.pos = (self.pos[0], round(parent.pos[1] + parent.size_my[1]/2 - size_my[1]/2)) #size_calced[1]/2)

        if self.calced.position == 'absolute':
            self.pos = (pos_parent[0]+self.calced.left, pos_parent[1]+self.calced.top)

        pos_my = (self.pos[0], self.pos[1])

        size_calced = self.calc_children(pos_my, size_my)

        self.size_calced = size_calced if size_calced != None else size_my

        if self.calced.text_width_real != self.calced.text_width:
            w_by_text = self.calced.text_width_real + self.calced.padding * 2
            if w_by_text > self.size_calced[0]:
                self.size_calced = (w_by_text, self.size_calced[1])

        return size_my

    def calc_children(self, pos_my, size_my):

        _ps = (pos_my[0], pos_my[1])
        size_calced = (size_my[0], size_my[1])

        _size_calced = size_calced
        for node in self.node.children:
            if not hasattr(node, 'drawer'):
                continue

            drawer = node.drawer

            _size_my = drawer.calc_size(size_my, (_ps[0], _ps[1]), pos_my)#, debug=image_button)

            if drawer.calced.position == 'absolute':
                continue

            _ps, _size_calced = self.add_subnode_pos_size(node, _ps, _size_calced, self.calced.margin)

        parent_drawer = getattr(self.node.parent, 'drawer', None)
        if parent_drawer and getattr(parent_drawer.calced, 'display', None) == 'flex':
            size_calced = size_calced
        else:
            size_calced = _size_calced

        h = _ps[1] - pos_my[1]
        if h > size_calced[1]:
            size_calced = (size_calced[0], h)

        return size_calced

    def add_subnode_pos_size(self, node, pos_my, size_calced, margin, vertical=True):
        pos = [pos_my[0], pos_my[1]]
        drawer = node.drawer
        wh = drawer.size_calced
        mg = drawer.calced.margin
        if mg:
            mg_2 = mg*2
            if vertical:
                wh = (wh[0], wh[1]+mg_2)
            else:
                wh = (wh[0]+mg_2, wh[1])

        if vertical:
            static_i, change_i = 0, 1
        else:
            static_i, change_i = 1, 0

        if vertical:
            if wh[1] > size_calced[1]:
                size_calced = (size_calced[0], wh[1])

            if wh[0] > size_calced[0]:
                size_calced = (wh[0], size_calced[1])

            if pos[0] + wh[0] - pos_my[0] > size_calced[0]:
                size_calced = (pos[0] + wh[0] - pos_my[0], size_calced[1])

        else:
            if wh[0] > size_calced[0]:
                size_calced = (wh[0], size_calced[1])

            if wh[1] > size_calced[1]:
                size_calced = (size_calced[0], wh[1])

            if pos[1] + wh[1] - pos_my[1] > size_calced[1]:
                size_calced = (size_calced[0], pos[1] + wh[1] - pos_my[1])

        pos[change_i] += wh[change_i] #+ mg #margin

        return pos, size_calced

    def draw(self, cr, absolutes=False):

        ps, size_calced = self.pos, self.size_calced

        background_color = self.calced.background_color
        border_radius = self.calced.border_radius
        color = self.calced.color
        font_size = self.calced.font_size
        font_weight = self.calced.font_weight
        border = self.calced.border
        image = getattr(self.calced, 'image', None)

        rect = (ps[0], ps[1], size_calced[0], size_calced[1])

        tag = self.node.tag.text if self.node.tag else None
        is_absolute = self.calced.position == 'absolute'
        if not absolutes or is_absolute:

            if background_color:
                self.draw_background(cr, background_color, rect, radius=border_radius)

            if image:
                self.draw_image(cr, image, rect)

            if border:
                self.draw_border(cr, rect, 'full', border[0], border[1], border[2], radius=border_radius)
            for nm in ('left', 'right', 'top', 'bottom'):
                bd = getattr(self.calced, 'border_'+nm, None)
                if bd:
                    self.draw_border(cr, rect, nm, bd[0], bd[1], bd[2])

            padding = self.calced.padding
            self.draw_lines(cr, self.node.lines, (ps[0]+padding, ps[1]+padding), size_calced[0]-padding*2,
                font_size, font_weight, self.calced.text_align, self.calced.vertical_align, color)

            if self.ability:
                self.ability.draw(cr, rect)

            if tag == 'listview':
                listview = self.node.attrs.get('data_model', None)
                if listview and listview.template:
                    draw_listview(self, listview, cr, absolutes=absolutes)
                    return

        if tag in ('template', 'listview'):
            return

        for node in self.node.children:

            if not hasattr(node, 'drawer'):
                continue

            node.drawer.draw(cr, absolutes if not is_absolute else False)

    def draw_background(self, cr, background_color, rect, radius=None):
        rect = (rect[0], rect[1], rect[2]+1-1, rect[3]+1-1)
        cr_set_source_rgb_any_hex(cr, background_color)
        if radius:
            roundrect(cr, rect[0], rect[1], rect[2], rect[3], radius)
        else:
            cr.rectangle(*rect)
        cr.fill()

    def draw_border(self, cr, rect, nm, border_width, border_type, border_color, radius=None):
        cr_set_source_rgb_any_hex(cr, border_color)
        cr.set_line_width(border_width)
        if nm == 'full':
            rect = (rect[0]+0.5, rect[1]+0.5, rect[2]-1+1, rect[3]-1+1)
            if radius:
                roundrect(cr, rect[0], rect[1], rect[2], rect[3], radius)
            else:
                cr.rectangle(*rect)
        else:
            if nm == 'left':
                x1, y1, x2, y2 = rect[0], rect[1], rect[0], rect[1]+rect[3]
            elif nm == 'right':
                x1, y1, x2, y2 = rect[0]+rect[2]+0.5, rect[1], rect[0]+rect[2]+0.5, rect[1]+rect[3]
            elif nm == 'top':
                x1, y1, x2, y2 = rect[0], rect[1]+0.5, rect[0]+rect[2], rect[1]+0.5
            elif nm == 'bottom':
                x1, y1, x2, y2 = rect[0], rect[1]+rect[3], rect[0]+rect[2], rect[1]+rect[3]
            cr.move_to(x1, y1)
            cr.line_to(x2, y2)
        cr.stroke()

    def draw_lines(self, cr, lines, pos, width, font_size, font_weight, text_align, vertical_align, color):
        if not lines:
            return

        cr_set_source_rgb_any_hex_or_simple(cr, color, (0.1, 0.1, 0.1))

        cr.set_font_size(font_size)
        ff_tmp = None
        if font_weight == 'bold':
            ff_tmp = cr.get_font_face()
            cr.select_font_face(ff_tmp.get_family(), cairo.FONT_SLANT_NORMAL,
                cairo.FONT_WEIGHT_BOLD)
        x, y = pos
        y0 = y
        if self.ability:
            scroll_pos_y = getattr(self.ability, 'scroll_pos_y', 0)
            if scroll_pos_y:
                y -= scroll_pos_y
        x += 0.5
        dy = font_size*0.82
        x0 = x
        is_right_aligned = text_align == 'right'
        is_center_aligned = text_align == 'center'
        is_vert_middle_aligned = vertical_align in ('middle', 'center')
        if is_vert_middle_aligned:
            #print(":::::", "y:", y, "size:", self.size_calced[1], "dy:", dy)
            y0 = y = y + (self.size_calced[1] / 2.0) - dy/2 - self.calced.padding

        _smiles = []
        fw_size_w = self.calced.calc_font_size_w(font_size)
        _selected_lines = []
        for line in lines:
            _selected_line = None
            _x = x
            _, _, line_width, _ = cr.text_extents(line)[:4]
            if is_right_aligned:
                _x = x + width - line_width
            elif is_center_aligned:
                _x = x + width/2 - line_width/2
            if y >= y0:
                y_bottom = y + dy
                if SELECT_CONTROL._double_clicked and SELECT_CONTROL.start != None:
                    if (
                        (y < SELECT_CONTROL.start[1] < y_bottom) and ( _x < SELECT_CONTROL.start[0] < x + width )
                    ):
                        dln = 0
                        line_width_2 = 0
                        dline = ''
                        while _x + line_width_2 < SELECT_CONTROL.start[0]:
                            dline = line[:dln]
                            _, _, line_width_2, _ = cr.text_extents(dline)[:4]
                            if len(dline) == len(line):
                                break
                            dln += 1
                        dline = ' '.join(dline.split(' ')[:-1]) + ' '
                        _, _, line_width_2, _ = cr.text_extents(dline)[:4]
                        is_first_word = False
                        if dline == ' ':
                            line_width_2 = -1
                            dline = ''
                            is_first_word = True
                        SELECT_CONTROL.start[0] = int(_x + line_width_2) + 1 #+ 1)
                        _word = line[len(dline):].split(' ')[0]
                        print('[ left line ]:', dline, "[ word ]:", _word)
                        _, _, line_width_3, _ = cr.text_extents(_word)[:4]
                        if is_first_word:
                            line_width_3 += 1
                        SELECT_CONTROL.end = [SELECT_CONTROL.start[0]+line_width_3, SELECT_CONTROL.start[1]]
                if SELECT_CONTROL.start != None and SELECT_CONTROL.end != None:
                    _start, _end = SELECT_CONTROL.start, SELECT_CONTROL.end
                    if _start[1] > _end[1]+5:
                        _start, _end = _end, _start
                    elif y <= _start[1] <= _end[1] <= y_bottom and _start[0] > _end[0]:
                        _start, _end = _end, _start
                    _ramki_x = None
                    if SELECT_CONTROL.listview:
                        _lv_pos = SELECT_CONTROL.listview.drawer.pos
                        _lv_size = SELECT_CONTROL.listview.drawer.calced.rect.width, SELECT_CONTROL.listview.drawer.calced.rect.height
                        _ramki_x = (_lv_pos[0], _lv_pos[0] + _lv_size[0])
                    drawed = None
                    x_right = _x + line_width
                    b_color = '#cccccc'
                    if (
                        (_start[1] < y and y_bottom < _end[1])
                    ):
                        #self.draw_background(cr, '#cccccc', (_x, y, line_width, dy))
                        _, _, line_width_2, _ = cr.text_extents(line)[:4]
                        drawed = (_x, y, line_width_2, dy)
                        _selected_line = line
                    elif (y <= _start[1] <= y_bottom and y_bottom < _end[1]):
                        b_color = '#ffcccc'
                        if _start[0] <= _x:
                            drawed = (_x, y, line_width, dy)
                            _selected_line = line
                        else:
                            dx = _start[0] - _x
                            dx_ln = round(dx / fw_size_w) - 3
                            if dx_ln < 0:
                                dx_ln = 0
                            if dx_ln >= 0:
                                dx_2 = dx - 10
                                if dx_2 < 0:
                                    textWidth = dx_2 = 0
                                    dline = line
                                while dx_2 < dx:
                                    textWidth = dx_2
                                    dline = line[:dx_ln]
                                    _, _, dx_2, _ = cr.text_extents(dline)[:4]
                                    dx_ln += 1
                                    if len(dline) == len(line):
                                        textWidth = dx_2
                                        break
                                _line = line[len(dline)-1:]
                                if getattr(line, '_breaked', False):
                                    _line = StrBreaked(_line)
                                _, _, line_width_2, _ = cr.text_extents(_line)[:4]
                                b_color = '#ffcccc'
                                dx_width = textWidth #dx_width = dx_ln * fw_size_w
                                if dx_width < 0:
                                    print('!!!!!>>>>>', dx_width)
                                #self.draw_background(cr, '#cccccc', (_x+dx_width, y, line_width-dx_width, dy))
                                drawed = (_x+dx_width, y, line_width_2, dy)#line_width-dx_width, dy)
                                _selected_line = _line
                    elif (y <= _end[1] <= y_bottom and _start[1] < y):
                        dx = line_width - (x_right - _end[0])
                        if dx > 0:
                            dx_ln = round(dx / fw_size_w) - 3
                            if dx_ln < 0:
                                dx_ln = 0
                            if dx_ln >= 0:
                                dx_2 = dx - 10
                                if dx_2 < 0:
                                    textWidth = dx_2 = 0
                                dline = None
                                while dx_2 < dx:
                                    textWidth = dx_2
                                    dline = line[:dx_ln]
                                    _, _, dx_2, _ = cr.text_extents(dline)[:4]
                                    dx_ln += 1
                                    if len(dline) == len(line):
                                        textWidth = dx_2
                                        break
                                if dline != None:
                                    _selected_line = dline
                                dx_width = textWidth #dx_width = dx_ln * fw_size_w
                                #self.draw_background(cr, '#cccccc', (_x, y, line_width-dx_width, dy))
                                b_color = '#ccffcc'
                                drawed = (_x, y, dx_width, dy)
                    elif (
                        (y <= _start[1] <= _end[1] <= y_bottom) and
                        (_x <= _start[0] <= _end[0] <= x_right or (_ramki_x != None and _ramki_x[0] <= _start[0] <= _end[0] <= _ramki_x[1]))
                    ):
                        b_color = '#ccccff'
                        _line1 = line
                        if _start[0] < _x:
                            dx1 = 0
                            dx_ln = 0
                        else:
                            # dx1 = _start[0] - _x
                            # dx1 = round(dx1 / fw_size_w) * fw_size_w
                            dx1 = _start[0] - _x
                            dx_ln = round(dx1 / fw_size_w) - 3
                            if dx_ln < 0:
                                dx_ln = 0
                            if dx_ln >= 0:
                                dx_2 = dx1 - 10
                                _dline = ''
                                if dx_2 < 0:
                                    textWidth = dx_2 = 0
                                while dx_2 < dx1:
                                    textWidth = dx_2
                                    _dline = line[:dx_ln]
                                    _, _, dx_2, _ = cr.text_extents(_dline)[:4]
                                    dx_ln += 1
                                    if len(_dline) == len(line):
                                        textWidth = dx_2
                                        break
                                _line1 = line[len(_dline)-1:]
                                _, _, line_width_2, _ = cr.text_extents(_line1)[:4]
                                dx1 = textWidth

                        if _end[0] > x_right:
                            dx2 = x_right - _x - dx1
                            _selected_line = _line1
                        else:
                            # dx2 = x_right - _end[0]
                            # dx2 = round(dx2 / fw_size_w) * fw_size_w
                            _line0 = _line1 #line[dx_ln:]
                            dx2 = _end[0] - _x - dx1
                            dx_ln = round(dx2 / fw_size_w) - 3
                            if dx_ln < 0:
                                dx_ln = 0
                            dline = _line0
                            if dx_ln >= 0:
                                dx_2 = dx2 - 10
                                if dx_2 < 0:
                                    textWidth = dx_2 = 0
                                while dx_2 < dx2:
                                    textWidth = dx_2
                                    dline = _line0[:dx_ln]
                                    _, _, dx_2, _ = cr.text_extents(dline)[:4]
                                    dx_ln += 1
                                    if len(dline) == len(_line0):
                                        textWidth = dx_2
                                        break
                                # _line2 = line[len(dline)-1:]
                                # _, _, line_width_2, _ = cr.text_extents(_line2)[:4]
                                dx2 = textWidth
                            _selected_line = dline

                        #self.draw_background(cr, '#cccccc', (_x+dx1, y, line_width-dx1-dx2, dy))
                        drawed = (_x+dx1, y, dx2, dy)
                        #drawed = (_x+dx1, y, line_width-dx1-dx2, dy)

                    if drawed != None:
                        if drawed[2] <= 0 or drawed[3] <= 0:
                            drawed = None
                        elif _ramki_x != None:
                            if drawed[0] < _ramki_x[0]:
                                # if _selected_line:
                                #     _selected_line += ":!1<ramki:{}|drawed:{}>".format(_ramki_x, drawed)
                                if drawed[0] + drawed[2] < _ramki_x[0]:
                                    drawed = None
                                else:
                                    drawed = (_ramki_x[0], drawed[1], drawed[2], drawed[3])
                            if drawed != None and _ramki_x[1] < drawed[0] + drawed[2]:
                                _li_wi = _ramki_x[1] - drawed[0]
                                if _li_wi <= 0:
                                    drawed = None
                                else:
                                    # if _selected_line:
                                    #     _selected_line += ":!2"
                                    drawed = (drawed[0], drawed[1], _li_wi, drawed[3])
                            if drawed != None and (_ramki_x[1] <= drawed[0] or drawed[0] + drawed[2] < _ramki_x[0]):
                                drawed = None
                    if drawed != None:
                        self.draw_background(cr, b_color, drawed)
                        cr_set_source_rgb_any_hex_or_simple(cr, color, (0.1, 0.1, 0.1))
                    else:
                        _selected_line = None
                    if _selected_line != None:
                        _selected_lines.append(_selected_line)

                cr.move_to(_x, y_bottom) #+5
                cr.show_text(line)

                sm_i = -1
                while True:
                    sm_i = line.find('😉', sm_i+1)
                    if sm_i < 0:
                        break
                    image = cairo.ImageSurface.create_from_png(join(DATA_PATH, 'smile_10.png'))
                    _, _, sm_width, _ = cr.text_extents(line[:sm_i])[:4]
                    _smiles.append((image, (_x+sm_width, y, fw_size_w*2.3, fw_size_w*2.3)))

            y += font_size

        for image, rect in _smiles:
            self.draw_image(cr, image, rect, resize_imp=True)

        if ff_tmp:
            cr.set_font_face(ff_tmp)

        if _selected_lines:
            SELECT_CONTROL._selected_lines += _selected_lines

    def draw_image(self, cr, image, rect, resize_imp=False):
        r = (rect[0], rect[1], rect[2], rect[3])
        img_w, img_h = image.get_width(), image.get_height()
        wk, hk = (
            1 if self.calced._width < 0 and not resize_imp else rect[2]/img_w,
            1 if self.calced._height < 0 and not resize_imp else rect[3]/img_h
        )
        boo = wk != 1 or hk != 1
        if boo:
            r = (rect[0]/wk, rect[1]/hk, rect[2]/wk, rect[3]/hk)
            cr.scale(wk, hk)
        cr.set_source_surface(image, r[0], r[1])
        cr.paint()
        if boo:
            cr.scale(1/wk, 1/hk)

    def propagateEvent(self, pos, event_name):
        changed = False

        if self.checkPostIntoMe(pos) or self in PRIOR_EVENT_HANDLERS:
            # if self.node not in HOVERED_NODES:
            #     HOVERED_NODES.add(self.node)
            if not self.node.is_hovered:
                self.node.is_hovered = True
                changed = True
                if self.calced.cursor:
                    self.node.app.mainPanel.changeCursor(self.calced.cursor)

            if self.ability:
                if self.ability.doEvent(pos, event_name):
                    changed = True # return True

            ev = self.node.attrs.get(event_name, None) if self.node.attrs else None
            if ev:
                _event = Event()
                _event.pos = pos
                _event.event_name = event_name
                _event.node = self.node
                _ev_ret = ev(_event)
                if _ev_ret:
                    if _ev_ret == 'prior':
                        PRIOR_EVENT_HANDLERS.insert(0, self)
                    elif _ev_ret == 'out_prior':
                        PRIOR_EVENT_HANDLERS.remove(self)
                    changed = _ev_ret # return True

            if self.node.tag and self.node.tag.text =='listview':
                listview = self.node.attrs['data_model']
                if event_name == 'ondown':
                    SELECT_CONTROL.listview = self.node
                ret = listview.doEvent(pos, event_name)
                if ret:
                    changed = True # return ret

        # else:
        #     if self.node.is_hovered:
        #         self.node.is_hovered = False
        #         changed = True
        #         if getattr(self.calced, 'cursor', None):
        #             self.node.app.mainPanel.changeCursor(None)

        #     if self.node.tag and self.node.tag.text =='listview':
        #         listview = self.node.attrs['data_model']
        #         listview.doEventOut(pos, event_name)

        return changed

    def propagateEventOut(self, pos, event_name):
        changed = False

        if self.checkPostIntoMe(pos):# or self in PRIOR_EVENT_HANDLERS:
            pass
        else:
            # if self.node in HOVERED_NODES:
            #     HOVERED_NODES.remove(self.node)
            if self.node.is_hovered:
                self.node.is_hovered = False
                changed = True
                if getattr(self.calced, 'cursor', None):
                    self.node.app.mainPanel.changeCursor(None)

            if self.node.tag and self.node.tag.text =='listview':
                listview = self.node.attrs['data_model']
                listview.doEventOut(pos, event_name)

        return changed


    def checkPostIntoMe(self, pos):
        if not hasattr(self, 'pos'):
            return False

        return (
            hasattr(self, 'size_calced') and
            self.pos[0] <= pos[0] < self.pos[0] + self.size_calced[0] and
            self.pos[1] <= pos[1] < self.pos[1] + self.size_calced[1]
        )

    def find_node_by_pos_and_tags(self, x, y, tags):
        if self.node.tag and self.node.tag.text in tags:
            if (
                self.pos[0] <= x < self.pos[0] + self.size_calced[0] and
                self.pos[1] <= y < self.pos[1] + self.size_calced[1]
            ):
                return self

        for node in self.node.children:
            if not hasattr(node, 'drawer'):
                continue
            lv = node.drawer.find_node_by_pos_and_tags(x, y, tags)
            if lv:
                return lv

        return None

    def find_listview_by_pos(self, x, y):
        return self.find_node_by_pos_and_tags(x, y, ('listview',))

    def find_nodes_in_pos(self, x, y, lst=None):
        if lst == None:
            lst = []
        if (
            self.pos[0] <= x < self.pos[0] + self.size_calced[0] and
            self.pos[1] <= y < self.pos[1] + self.size_calced[1]
        ):
            lst.append(self)
        else:
            return lst

        for node in self.node.children:
            if not hasattr(node, 'drawer'):
                continue
            lst += node.drawer.find_nodes_in_pos(x, y, lst)

        return lst


def roundrect(context, x, y, width, height, r):
    context.new_sub_path()
    context.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    context.arc(x+width-r, y+r, r, 3*math.pi/2, 0)
    context.arc(x+width-r, y+height-r, r, 0, math.pi/2)
    context.arc(x+r, y+height-r, r, math.pi/2, math.pi)
    context.close_path()


class DrawerFlex(DrawerBlock):

    def calc_children(self, pos_my, size_my):
        flex_sum = 0
        static_sum = 0

        _ps = (pos_my[0], pos_my[1])
        size_calced = (size_my[0], size_my[1])

        self.flex_point = 0
        flex_vertical = self.calced.flex_direction == 'column'
        justify_content = self.calced.justify_content

        for node in self.node.children:
            if hasattr(node, 'drawer'):
                drawer = node.drawer
                drawer.calc_size(size_my, (_ps[0], _ps[1]), pos_my)
                if drawer.calced.position == 'absolute':
                    continue
                flex = drawer.calced.flex
                if flex:
                    flex_sum += flex
                else:
                    mg = drawer.calced.margin
                    static_sum += (drawer.calced.rect.height if flex_vertical else drawer.calced.rect.width) + mg*2

        self.flex_point = ((size_my[1 if flex_vertical else 0]-static_sum) / flex_sum) if flex_sum > 0 else 0

        if justify_content == 'center' and flex_sum == 0:
            if flex_vertical:
                _ps = (_ps[0], round(_ps[1]+(size_calced[1]-static_sum)/2))
            else:
                _ps = (round(_ps[0]+(size_calced[0]-static_sum)/2), _ps[1])

        _size_calced = size_calced
        for node in self.node.children:
            if not hasattr(node, 'drawer'):
                continue

            drawer = node.drawer
            if drawer.calced.position == 'absolute':
                continue

            _size_my = drawer.calc_size(size_my, (_ps[0], _ps[1]), pos_my)

            if hasattr(drawer, 'add_node_pos_size'):
                _ps, _size_calced = drawer.add_node_pos_size(_ps, _size_calced, self.flex_point, flex_vertical)
            else:
                _ps, _size_calced = self.add_subnode_pos_size(node, _ps, _size_calced, self.calced.margin, vertical=flex_vertical)

        if flex_vertical:
            pass
        else:
            if _size_calced[1] > size_calced[1]:
                size_calced = (size_calced[0], _size_calced[1])

        return size_calced


class AbilityBase:

    def __init__(self, drawer) -> None:
        self.drawer = drawer
        drawer.ability = self

    def draw(self, cr, rect):
        pass

    def doEvent(self, pos, event_name):
        pass


class AbilityInput(AbilityBase, Scrollable):

    def __init__(self, drawer) -> None:
        super().__init__(drawer)
        Scrollable.__init__(self)
        self.cursor_visible = False
        self.cursor_pos = 0

    @property
    def mean_h(self):
        return 20

    def draw(self, cr, rect):

        scroll_area_height = self.calc_scroll_area_height()

        drawer = self.drawer
        _ps = lv_pos = getattr(drawer, 'pos', (0, 0))
        _sz = getattr(drawer, 'size_calced', (0, 0))

        need_scroll = scroll_area_height > _sz[1]
        if need_scroll:
            _sz = lv_size = self.draw_scroll(cr, _ps, _sz)
            _items_count = self.getItemsCount()
            self.draw_scroll_pos(cr, lv_pos, lv_size)

        if not self.cursor_visible:
            return
        padding = self.drawer.calced.padding
        cr.set_source_rgb(*hex2color('#000000'))
        cr.set_line_width(1)

        fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()

        y00 = rect[1]+padding-fdescent
        x0, y0 = rect[0]+padding, y00 - self.scroll_pos_y

        is_vert_middle_aligned = self.drawer.calced.vertical_align in ('middle', 'center')
        if is_vert_middle_aligned:
            dy = fheight*0.82
            y0 = y0 + (self.drawer.size_calced[1] / 2.0) - dy/2 - self.drawer.calced.padding

        cursor_height = fheight #14 #20
        x1, y1, x2, y2 = x0, y0, x0, y0 + cursor_height + fdescent

        lines = self.drawer.node.lines

        k = 0
        if lines:
            cutted_lines = []
            for i, li in enumerate(lines):
                dk = self.cursor_pos - k
                if dk >= 0:
                    _fin = False
                    ln = len(li)
                    if dk < ln:
                        li = li[:dk]
                        _fin = True
                    elif dk == ln:
                        _fin = True
                    cutted_lines.append(li)
                    k += ln
                    if _fin:
                        break
                k += 1

            if cutted_lines:
                hi = len(cutted_lines)
                line = cutted_lines[-1]
                wi = len(line)

                hadd = (hi - 1) * fascent + fdescent #(fheight*0.77)
                xoff, yoff, textWidth, textHeight = cr.text_extents(line)[:4]
                wadd = textWidth - fdescent

                x1, y1, x2, y2 = x0+wadd, y0+hadd-fdescent, x0+wadd, y0+hadd + cursor_height

        if self.drawer.node.text:
            if self.cursor_pos > len(self.drawer.node.text):
                self.cursor_pos = len(self.drawer.node.text)

        if y1 >= y00:
            cr.move_to(x1+0.5, y1)
            cr.line_to(x2+0.5, y2)
            cr.stroke()

    def moveCursor(self, way):
        if type(way) == int:
            self.cursor_pos = way
        else:
            if way == 'left':
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            elif way == 'right':
                self.cursor_pos += 1
            elif way == 'home':
                self.cursor_pos = 0
            elif way == 'end':
                self.cursor_pos = len(self.drawer.node.text)
            elif way == 'up':
                lst = self.drawer.node.text[:self.cursor_pos].split('\n')
                if len(lst) > 1:
                    lst[:], last_deleted_ln = lst[:-1], len(lst[-1])
                    last_ln = len(lst[-1])
                    if last_deleted_ln > last_ln:
                        last_deleted_ln = last_ln
                    self.cursor_pos = len('\n'.join(lst)) - last_ln + last_deleted_ln
            elif way == 'down':
                lst1 = self.drawer.node.text[:self.cursor_pos].split('\n')
                lst2 = self.drawer.node.text[self.cursor_pos:].split('\n')
                if len(lst2) > 1:
                    last_ln = len(lst1[-1])
                    ln_0 = len(lst2[0])
                    ln_1 = len(lst2[1])
                    if last_ln > ln_1:
                        last_ln = ln_1
                    self.cursor_pos = len('\n'.join(lst1)) + ln_0 + 1 + last_ln

        self.cursor_visible = True
        INPUT_CONTROL.start_timer()
        return True

    def doEvent(self, pos, event_name):
        if event_name == 'onclick':
            INPUT_CONTROL.set_focus(self)
            return self
        return Scrollable.doEvent(self, pos, event_name)

    def on_timer(self):
        self.toggle()

    def toggle(self):
        self.cursor_visible = not self.cursor_visible
        if INPUT_CONTROL.refresher:
            INPUT_CONTROL.refresher()

    def on_focus_got(self):
        self.cursor_visible = True

    def on_focus_lost(self):
        self.cursor_visible = False

    def setText(self, text):
        self.drawer.node.text = text

        _attrs = self.drawer.node.attrs
        if _attrs and 'onchange' in _attrs:
            _attrs['onchange'](self.drawer.node)

    def addText(self, text):
        if not self.drawer.node.text:
            self.drawer.node.text = ""

        if self.cursor_pos < 0:
            self.cursor_pos = 0
        elif self.cursor_pos > len(self.drawer.node.text):
            self.cursor_pos = len(self.drawer.node.text)

        if text == None:
            if self.cursor_pos > 0:
                self.drawer.node.text = self.drawer.node.text[:self.cursor_pos-1] + self.drawer.node.text[self.cursor_pos:]
        else:
            if len(self.drawer.node.text) == 0:
                self.drawer.node.text += text
            else:
                self.drawer.node.text = self.drawer.node.text[:self.cursor_pos] + text + self.drawer.node.text[self.cursor_pos:]

        _attrs = self.drawer.node.attrs
        if _attrs and 'onchange' in _attrs:
            _attrs['onchange'](self.drawer.node)

    def getDrawer(self):
        return self.drawer

    def getItemsCount(self):
        lines = self.drawer.node.lines
        if lines != None:
            return len(lines)
        return 0


class DrawerFlexItem(DrawerBlock):

    def calc_children(self, pos_my, size_my):
        try:
            flex_vertical = self.node.parent.drawer.calced.flex_direction == 'column'
        except:
            print('????', self.node.parent)
            raise

        if flex_vertical:
            size_my = (size_my[0], round(self.node.parent.drawer.flex_point * self.calced.flex))
        else:
            size_my = (round(self.node.parent.drawer.flex_point * self.calced.flex), size_my[1])

        size_calced = super().calc_children(pos_my, size_my)

        if flex_vertical:
            return (size_calced[0], self.node.parent.drawer.flex_point * self.calced.flex)
        else:
            return (self.node.parent.drawer.flex_point * self.calced.flex, size_calced[1])

    def add_node_pos_size(self, pos_my, size_calced, flex_point, flex_vertical):
        pos = (
            (pos_my[0], round(pos_my[1] + flex_point * self.calced.flex))
            if flex_vertical else
            (round(pos_my[0] + flex_point * self.calced.flex), pos_my[1])
        )
        wh = self.size_calced

        if flex_vertical:
            if wh[0] > size_calced[0]:
                size_calced = (wh[0], size_calced[1])
        else:
            if wh[1] > size_calced[1]:
                size_calced = (size_calced[0], wh[1])

        return pos, size_calced


def _propagateEvent(root_node, pos, event_name):
    # changed = False
    # for node in HOVERED_NODES:
    #     changed = _propagateEventOut(root_node, pos, event_name) or changed
    changed = _propagateEventOut(root_node, pos, event_name)
    nodes = _findNodesInPos(root_node, pos)
    for node in nodes[::-1]:
        ret = _propagateEventDo(node, pos, event_name)
        #print('propagate', id(node), node.tag.text, '->', ret, '=', ret == 'grab')
        if ret == 'grab':
            return ret
        changed = changed or ret
    return _propagateEventDo(root_node, pos, event_name) or changed

def _propagateEventOut(node, pos, event_name):
    changed = False

    if node.tag and node.tag.text == 'template':
        return changed

    if hasattr(node, 'drawer'):
        changed = node.drawer.propagateEventOut(pos, event_name)

    for ch in node.children:
        changed = _propagateEventOut(ch, pos, event_name) or changed

    return changed

def _propagateEventDo(node, pos, event_name):
    drawer = getattr(node, 'drawer', None)
    changed = False

    tag = node.tag.text if node.tag else None
    if tag == 'template':
        return changed

    if drawer:
        changed = drawer.propagateEvent(pos, event_name) or changed

    #print('propagateDo', id(node), node.tag.text, '->', changed, '=', changed == 'grab')

    return changed


def _findNodesInPos(node, pos):
    nodes = []

    tag = node.tag.text if node.tag else None
    if tag == 'template':
        return nodes

    drawer = getattr(node, 'drawer', None)
    if drawer and drawer.checkPostIntoMe(pos):
        nodes.append(node)

    for ch in node.children:
        nodes += _findNodesInPos(ch, pos)

    return nodes


# def _findAbsolute(node, pos):
#     absolutes = []

#     tag = node.tag.text if node.tag else None
#     if tag == 'template':
#         return absolutes

#     drawer = getattr(node, 'drawer', None)
#     if drawer and drawer.checkPostIntoMe(pos):
#         if drawer.calced.position == 'absolute':
#             absolutes.append(node)

#     for ch in node.children:
#         absolutes += _findAbsolute(ch, pos)
#     return absolutes

