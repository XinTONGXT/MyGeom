# MyGeom.py - API for easier Salome geompy usage
#
# Copyright (C) year  Stefan Reiterer - stefan.reiterer@magnasteyr.com
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

from numpy import array
from numpy import float64 as data_type

# For future Versions of salome!
# from salome.geom import geomBuilder
# geompy = geomBuilder.New(salome.myStudy)

# Define help classes for more structured programming
class MyGeomObject(object):
    """
    Base class for all custom geometrical objects
    """
    def __init__(self,geomObject):
        self.geomObject = geomObject

    def addToStudy(self,studyName):
        """
        Adds Vertex to study and adds
        the name in the study
        """
        geompy.addToStudy(self.geomObject,studyName)
        self.studyName = studyName

    def getStudyName(self):
        return self.studyName

    def getGeomObject(self):
        return self.geomObject

    def setGeomObject(self,geom_object):
        self.geomObject = geom_object
    



class MyVertex(MyGeomObject):
    """
    Help class for storing vertices.
    Additionally stores coordinate of
    the Vertex

    """
    
    def __init__(self,x, y = 0.0, z = 0.0):

        if isinstance(x,GEOM._objref_GEOM_Object):
            if x.GetShapeType() == GEOM.VERTEX:
                self.setCoord(geompy.GetPosition(x)[:3])
                self.setGeomObject(x)
            else:
                raise ValueError("Error: This is no vertex!")
        elif isinstance(x,MyVertex):
            self.setCoord(x.getCoord())
            self.setGeomObject(x.getGeomObject())
        else:
            self.setCoord((x,y,z))
            self.setGeomObject(geompy.MakeVertex(x,y,z))

    def __eq__(self,q):
        """
        Two points are considered equal iff
        the coordinates are the same
        """
        if all(self.getCoord() == q.getCoord()):
            return True
        else:
            return False

    def setCoord(self,coord):
        self.coord = array(coord,dtype=data_type)
        
    def getCoord(self):
        return self.coord

class MyLine(MyGeomObject):
    """
    Help class for storing lines
    Holds two instances of MyVertex
    """
    def __init__(self,line_or_point,q = None):

        type = None
        
        if isinstance(line_or_point,MyVertex):
            self.p = line_or_point
                        
        elif isinstance(line_or_point,GEOM._objref_GEOM_Object):
            type = geompy.ShapeIdToType(line_or_point.GetType())
            if type == 'LINE':
                subshapes = geompy.SubShapeAll(line_or_point,geompy.ShapeType['VERTEX'])
                self.p = MyVertex(subshapes[0])
                self.q = MyVertex(subshapes[-1])
            elif type == 'POINT':
                self.p = MyVertex(line_or_point)
        else:
            raise ValueError("This constructor does not support that option!")

                
        if q is None and (type != 'LINE' or type is None):
            raise ValueError("Second argument missing!")
        elif q is None and type == 'LINE':
            pass
        elif isinstance(q,GEOM._objref_GEOM_Object):
            type_q = geompy.ShapeIdToType(q.GetType())
            if type_q == 'POINT':
                self.q = MyVertex(q)
            else:
                raise ValueError("Error: second point is wrong type")
        elif isinstance(q,MyVertex):
                self.q = q
        else:
            raise ValueError("Error: second point is wrong type")
                    
        self.geomObject = geompy.MakeLineTwoPnt(self.p.geomObject,self.q.geomObject)

        
    def getP(self):
        return self.p

    def setP(self,p):
        if isinstance(p,MyVertex):
            self.p = p
        elif isinstance(p,GEOM._objref_GEOM_Object):
            type = geompy.ShapeIdToType(line_or_point.GetType())

            if type == 'POINT':
                self.p = MyVertex(p)
            else:
                raise ValueError("Error: Point is wrong type!")

        else:
            raise ValueError("Error: Point is wrong type!")
        
    def getQ(self):
        return self.q

    def setQ(self,q):
        if isinstance(q,MyVertex):
            self.q = q
        elif isinstance(p,GEOM._objref_GEOM_Object):
            type = geompy.ShapeIdToType(line_or_point.GetType())

            if type == 'POINT':
                self.q = MyVertex(q)
            else:
                raise ValueError("Error: Point is wrong type!")

        else:
            raise ValueError("Error: Point is wrong type!")

    def __eq__(self,other):
        """
        Two Lines are considered to be the same iff they have the same endpoints
        (without order)
        """
        if (self.getP() == other.getP() and self.getQ() == other.getQ()) or (self.getQ() == other.getP() and self.getP() == other.getQ()):
            return True
        else:
            False
# Perhaps deprecate this and replace it by face construction and
# explosion

class MyVector(MyGeomObject):
    """
    Help class for vectors
    """
    def __init__(self,vec_or_point,q = None):
        
        if isinstance(vec_or_point,MyVertex):
            p_type = 'MyVertex'
        elif isinstance(vec_or_point,GEOM._objref_GEOM_Object):
            p_type = geompy.ShapeIdToType(vec_or_point.GetType())
        else:
            raise ValueError("This constructor does not support that option!")

        if isinstance(q,MyVertex):
            q_type = 'MyVertex'
        elif isinstance(q,GEOM._objref_GEOM_Object):
            q_type = geompy.ShapeIdToType(vec_or_point.GetType())
        elif q is None:
            pass
        else:
            raise ValueError("This constructor does not support that option!")

        
        if q is None:
            if p_type == 'MyVertex':
                self.q = vec_or_point
                self.p = MyVertex(0.0)
            elif p_type == 'POINT':
                self.q = MyVertex(vec_or_point)
                self.p = MyVertex(0.0)
            elif p_type == 'VECTOR':
                subshapes = geompy.SubShapeAll(vec_or_point,geompy.ShapeType['VERTEX'])
                self.p = MyVertex(subshapes[0])
                self.q = MyVertex(subshapes[-1])
            else:
                raise ValueError('Error: Wrong Type!')
        elif q_type == 'POINT': 
            self.q = MyVertex(q)
            if p_type == 'MyVertex': 
                self.p = vec_or_point
            elif  p_type == 'POINT':
                self.p = MyVertex(vec_or_point)
            else:
                raise ValueError('Error: Wrong Type!')
        elif q_type == 'MyVertex':
            self.q = q
            if p_type == 'MyVertex': 
                self.p = vec_or_point
            elif  p_type == 'POINT':
                self.p = MyVertex(vec_or_point)
            else:
                raise ValueError('Error: Wrong Type!')
        else:
            raise ValueError('Error: Wrong Type!')

        
        self.geomObject = geompy.MakeVector(self.p.geomObject,self.q.geomObject)

        
    def getP(self):
        return self.p

    def getQ(self):
        return self.q
           
            

    def __eq__(self,other):
        """
        Two Vectors are considered to be the same iff they have the same startpoints and endpoints. Thats the only difference between a vector and a line.
        (without order)
        """
        if (self.getP() == other.getP() and self.getQ() == other.getQ()):
            return True
        else:
            False



class MyFace(MyGeomObject):
    """
    Help class for faces, and face related stuff
    """

    def __init__(self,face):
        """
        This init is a stub! It will be extended Later!
        """

        if face.GetShapeType() == GEOM.FACE:
            self.geomObject = face
        elif isinstance(face,MyFace):
            self.geomObject = face.getGeomObject()
        else:
            raise ValueError("Error: Shape is not a Face!")

    def ChangeOrientation(self,make_copy = False):
        if make_copy:
            return MyFace(geompy.ChangeOrientation(self.geomObject))
        else:
            self.geomObject = geompy.ChangeOrientation(self.geomObject) 

        

class MyQuadrangleFromLines(MyGeomObject):
    """
    Help class for Quadrangles built from
    Lines.
    """

    def __init__(self,edges):
        self.geomObject = geompy.MakeFaceWires(
            [edge.geomObject for edge in edges],1)
        self.edges = edges
 
def addListToStudy(liste,string):
    """
    Function to add list of geom objects to a study,
    with numbered name
    """
    i = 0
    for object in liste:
        object.addToStudy(string + str(i))
        i+=1

def ExplodeSubShape(my_geom_object,type,add_to_study = True):
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
