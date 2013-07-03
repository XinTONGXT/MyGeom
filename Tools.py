# MyGeom Module - API for easier Salome geompy usage
# Tools.py: Tool functions for MyGeom module
#
# Copyright (C) 2013  Stefan Reiterer - stefan.reiterer@magnasteyr.com or maldun.finsterschreck@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from __future__ import print_function

import salome
import geompy
import GEOM

from MyGeom.Types import *

from numpy import array, ndarray
from numpy import float64 as data_type

# For future Versions of salome!
# from salome.geom import geomBuilder
# geompy = geomBuilder.New(salome.myStudy)

def add_list2study(liste,string):
    """
    Function to add list of geom objects to a study,
    with numbered name
    """
    i = 0
    for object in liste:
        object.addToStudy(string + str(i))
        i+=1

def explode_sub_shape(my_geom_object,type,add_to_study = True):
    """
    Explode Sub Shapes of certain Type. If add_to_study is
    True add all objects to study
    """
    geom_object = my_geom_object.geomObject
    subshapes = geompy.SubShapeAll(geom_object,geompy.ShapeType[type])
    if add_to_study:
        for sub in subshapes:
            name = geompy.SubShapeName(sub,geom_object)
            geompy.addToStudyInFather(geom_object,sub,name)

    return subshapes

def create_local_coordinates(face, coord_u, coord_v):
    """
    Creates MyVertex list of a local coordinate system for a given degree.
    
    Parameters
    ----------
    face : GEOM.FACE or MyFace
           Face from Salome or MyFace 
        be such that a is 'square', ie., prod(Q) == prod(b.shape).
    coord_u : array, one dimensional
              local u coordinates
    
    coord_v : array, one dimensional

    Returns
    -------
    vertices : list of vertices, shape is the same as the input array

    Examples
    --------
    """

    if not isinstance(face,MyFace):
        face = MyFace(face)

    make_vertex = face.makeVertexOnSurface

    vertices = [[make_vertex(u,v) for v in coord_v] for u in coord_u]
    return vertices