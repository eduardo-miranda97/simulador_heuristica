# -*- coding:utf-8 -*-

from static_map import StaticMap
from structure_map import StructureMap
from wall_map import WallMap

structure_map = StructureMap("Centro Culto", "./centroCulto.map")
structure_map.load_map()

wall_map = WallMap("Centro Culto")
wall_map.load_wall_map(structure_map)
wall_map.draw_wall_map("")

static_map = StaticMap("Centro Culto")
static_map.load_static_map(structure_map)
static_map.draw_static_map("")