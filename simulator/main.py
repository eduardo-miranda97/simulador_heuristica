# -*- coding:utf-8 -*-

from structure_map import StructureMap
from static_map import StaticMap

structure_map = StructureMap("Centro Culto", "./centroCulto.map")
structure_map.load_map()

static_map = StaticMap("Centro Culto")
static_map.load_static_map(structure_map)