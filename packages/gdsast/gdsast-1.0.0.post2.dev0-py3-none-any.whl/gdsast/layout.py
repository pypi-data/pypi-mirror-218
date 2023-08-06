from .gdsast import *
from .geoms import Vector2D

def _gds_element_flip_rotate_pt(el, pt):
    if "mag" in el and el["element"] == "sref":
        raise NotImplemented
    if "strans" in el and el["strans"]&0x8000: # flipped
        pt = (pt[0], -pt[1])
    angle = el.get("angle", 0)
    if angle == 0:
        return pt
    elif angle == 90:
        return (-pt[1], pt[0])
    elif angle == 180:
        return (-pt[0], -pt[1])
    elif angle == 270:
        return (pt[1], -pt[0])
    angle = math.radians()
    sn = math.sin(angle)
    cs = math.cos(angle)
    return (int(pt[0]*cs - pt[1]*sn), int(pt[0]*sn + pt[1]*cs))

def _gds_element_update_pt(el, pt):
    pt = _gds_element_flip_rotate_pt(el, pt)
    x, y = el["xy"][0]
    return pt[0] + x, pt[1] + y

def _point_inside_geom(_geom, pt):
    v = Vector2D(pt[0], pt[1])
    if _geom["element"] == "boundary":
        return v.inside(_geom["xy"])
    elif _geom["element"] == "path":
        width = _geom["width"]
        def _boundary_pts():
            back = []
            def _ofs(pt1, pt2):
                dv = Vector2D(pt2[0] - pt1[0], pt2[1] - pt1[1]).normal().sized(width / 2)
                yield pt1 + dv
                yield pt2 + dv
                back.insert(0, pt1 - dv)
                back.insert(0, pt2 - dv)
            prev = None
            for pt in _geom["xy"]:
                if prev is not None:
                    yield from _ofs(prev, pt)
                prev = pt
            yield from back
        return v.inside(_boundary_pts())

def _box_pts(pts):
    xy = list(zip(*pts))    # -> [[all Xs], [all Ys]]
    if xy:
        yield list(map(min,xy)) # [min of all Xs, min of all Ys]
        yield list(map(max,xy)) # [max of all Xs, max of all Ys]

class GDSLayout:
    def __init__(self):
        self.gds = None # AST
        self.sts = {}   # structures map by name

    def init(self, lib_name, units = None):
        self.sts = {}
        if not units:
            units = [0.001, 1e-09]
        self.gds = gds_create(lib_name, units)

    def load_file(self, filename):
        with open(filename,"rb") as f:
            _gds = gds_read(f)
            if self.gds is None:
                self.gds = _gds
                for st in _gds["structures"]:
                    self.sts[st["name"]] = st
            else:
                units = self.gds["units"]
                _units = _gds["units"]
                if units != _units:
                    raise NotImplemented
                for st in _gds["structures"]:
                    name = st["name"]
                    if name in self.sts:
                        # TODO: check is same
                        print(f"GDS is reusing structure '{name}'")
                        continue
                    self.sts[name] = st
                    self.gds["structures"].append(st)

    def get_structure(self, name):
        return self.sts.get(name)

    def new_structure(self, name):
        st = self.get_structure(name)
        if st is not None:
            self.gds["structures"].remove(st)
        st = gds_create_structure(name)
        self.gds["structures"].append(st)
        self.sts[name] = st
        return st

    def get_structure_geom_points(self, st, ignore = {"text"}):
        for el in st["elements"]:
            yield from self.get_element_points(el, ignore)

    def get_element_geom_points(self, el, ignore = {"text"}):
        el_type = el["element"]
        if not (ignore and el_type in ignore):
            if el_type == "sref":
                if "mag" in el:
                    raise NotImplemented
                x, y = el["xy"][0] # sref position
                for pt in self.get_structure_geom_points(el["name"]):
                    pt = _gds_element_flip_rotate_pt(el, pt)
                    yield pt[0] + x, pt[1] + y
            elif "xy" in el:
                yield from el["xy"]

    def get_structure_geom_box(self, name, ignore = {"text"}):
        st = self.sts[name]
        def _pts():
            for el in st["elements"]:
                yield from self.get_element_geom_box(el, ignore)
        return list(_box_pts(_pts()))

    def get_element_geom_box(self, el, ignore = {"text"}):
        def _pts():
            el_type = el["element"]
            if not (ignore and el_type in ignore) and "xy" in el:
                xy = el["xy"]
                if el_type == "sref":
                    if "mag" in el:
                        raise NotImplemented
                    x, y = xy[0] # sref position
                    for pt in self.get_structure_geom_box(el["name"], ignore):
                        pt = _gds_element_flip_rotate_pt(el, pt)
                        yield pt[0] + x, pt[1] + y
                else:
                    yield from _box_pts(xy)
        return list(_box_pts(_pts()))

    def new_gds(self, lib_name, st_names): # create new GDSLayout with only selected structures
        gds = GDSLayout()
        gds.init(lib_name, self.gds["units"])
        names = set()
        def _srefs(st):
            for el in st["elements"]:
                if el["element"] == "sref":
                    yield el
        def _populate(name):
            names.add(name)
            st = self.get_structure(name)
            assert(st), f"GDS referencing non existing structure '{name}"
            for el in _srefs(st):
                el_name = el["name"]
                if el_name in names:
                    continue
                _populate(el_name)
        for name in st_names:
            _populate(name)
        # dependancy sort
        ordered_names = sorted(names)
        i = 0
        nerr = 0
        while i<len(ordered_names):
            name = ordered_names[i]
            st = self.get_structure(name)
            if any(map(lambda el: el["name"] in  names, _srefs(st))):
                ordered_names.pop(i)
                ordered_names.append(name)
                nerr += 1
                assert(nerr < len(names)), "GDS structures have elements with cross dependancies"
            else:
                names.discard(name)
                i += 1
                nerr = 0
        for name in ordered_names:
            st = self.get_structure(name)
            gds.gds["structures"].append(st)
        return gds

    def save_structures(self, filename, lib_name, st_names):
        gds = self.new_gds(lib_name, st_names)
        gds.save_file(filename)

    def save_file(self, filename):
        with open(filename, "wb") as f:
            gds_write(f, self.gds)

    def extract_pins(self, cell_name):
        st = self.get_structure(cell_name)
        assert(st),f"Unknown '{cell_name}' cell"
        def _labels(st):
            for el in st["elements"]:
                if el["element"] == "text":
                    yield el["xy"][0], el["layer"], el["text"]
                elif el["element"] == "sref":
                    for pt, layer, text in _labels(self.get_structure(el["name"])):
                        yield _gds_element_update_pt(el, pt), layer, text
        layer2labs = {}
        for pt, layer, label in _labels(st):
            if layer in layer2labs:
                labs = layer2labs[layer]
            else:
                labs = layer2labs[layer] = {}
            if label in labs:
                pts = labs[label]
            else:
                pts = labs[label] = set()
            pts.add(pt)
        pmin, pmax = self.get_structure_geom_box(cell_name)
        def _update_xy(sref, xy):
            for pt in xy:
                yield _gds_element_update_pt(sref, pt)
        def _geoms(st): # all geometries in the structure
            for el in st["elements"]:
                el_type = el["element"]
                if el_type == "sref":
                    for geom in _geoms(self.get_structure(el["name"])):
                        _geom = geom.copy()
                        _geom["xy"] = list(_update_xy(el, geom["xy"]))
                        yield _geom
                if el_type in ("boundary", "path"):
                    yield el
        def _edge_geoms(): # only geometries that touch edges
            for _geom in _geoms(st):
                for pt in _geom["xy"]:
                    if (pt[0] == pmin[0] or
                        pt[1] == pmin[1] or
                        pt[0] == pmax[0] or
                        pt[1] == pmax[1]):
                        yield _geom
                        break
        def _find_geom_label(_geom):
            layer = _geom["layer"]
            if layer in layer2labs:
                for label, pts in layer2labs[layer].items():
                    for pt in pts:
                        if _point_inside_geom(_geom,pt):
                            return label
        def _labeled_edge_geoms(): # all geometries that have label inside them
            for _geom in _edge_geoms():
                label = _find_geom_label(_geom)
                if label:
                    yield label, _geom
        pins = {orient: {} for orient in ('N','S','W','E')} # map chain: orient->label->layer->(pt,width) 
        def _add_pin(orient, label, layer, pt, width):
            side_pins = pins[orient]
            key = (label, layer)
            if label in side_pins:
                lmap = side_pins[label]
            else:
                lmap = side_pins[label] = {}
            if layer in lmap:
                pts = lmap[layer]
            else:
                pts = lmap[layer] = set()
            pts.add((pt, width))
        for label, _geom in _labeled_edge_geoms():
            if _geom["element"] == "path":
                width = _geom["width"]
                layer = _geom["layer"]
                for pt in _geom["xy"]:
                    if pt[0] == pmin[0]:
                        _add_pin('W', label, layer, pt, width)
                    elif pt[0] == pmax[0]:
                        _add_pin('E', label, layer, pt, width)
                    elif pt[1] == pmin[1]:
                        _add_pin('S', label, layer, pt, width)
                    elif pt[1] == pmax[1]:
                        _add_pin('N', label, layer, pt, width)
            elif _geom["element"] == "boundary":
                layer = _geom["layer"]
                prev = None
                for pt in _geom["xy"]:
                    if prev is not None:
                        if prev[0] == pt[0]:
                            if pt[0] == pmin[0]:
                                _add_pin('W', label, layer, (pt[0], (prev[1] +pt[1])//2), abs(pt[1] - prev[1]))
                            elif pt[0] == pmax[0]:
                                _add_pin('E', label, layer, (pt[0], (prev[1] +pt[1])//2), abs(pt[1] - prev[1]))
                        elif prev[1] == pt[1]:
                            if pt[1] == pmin[1]:
                                _add_pin('S', label, layer, ((prev[0] +pt[0])//2, pt[1]), abs(pt[0] - prev[0]))
                            elif pt[1] == pmax[1]:
                                _add_pin('N', label, layer, ((prev[0] +pt[0])//2, pt[1]), abs(pt[0] - prev[0]))
                    prev = pt
        return pins  # map chain: orient->label->layer->[(pt,width)] of edge points of labeled geometries

