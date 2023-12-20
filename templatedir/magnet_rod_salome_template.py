#!/usr/bin/env python
"""
 Description: Salome script to create and mesh files
 Author: Francisco Jimenez
 Date Created: 2023-12-19
 Salome version: 9.11
 Comments: You can open this script in Salome GUI 
"""

###
### This file is generated automatically by SALOME v9.11.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

SCALE_FACTOR = 1 #  mm
#SCALE_FACTOR = 0.001 # m

MAGNET_DIAMETER = 1*SCALE_FACTOR
MAGNET_HEIGHT = 1*SCALE_FACTOR
ROD_DIAMETER = 0.1*SCALE_FACTOR
ROD_LENGTH = 2*SCALE_FACTOR
RADIUS = 1*SCALE_FACTOR
ROTATION_ANGLE = [[rotation]]  # In degrees
DOMAIN = 5*SCALE_FACTOR

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Cylinder_1 = geompy.MakeCylinderRH(MAGNET_DIAMETER/2, MAGNET_HEIGHT)
Cylinder_2 = geompy.MakeCylinderRH(ROD_DIAMETER/2, ROD_LENGTH)
geompy.TranslateDXDYDZ(Cylinder_2, 0, RADIUS, -ROD_LENGTH/2)
geompy.TranslateDXDYDZ(Cylinder_1, 0, 0, -MAGNET_HEIGHT/2)
geompy.Rotate(Cylinder_2, OX, 90*math.pi/180.0)
geompy.Rotate(Cylinder_2, OY, ROTATION_ANGLE*math.pi/180.0)
Sphere_1 = geompy.MakeSphereR(DOMAIN)

Partition_1 = geompy.MakePartition([Cylinder_1, Cylinder_2, Sphere_1], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
[Air, Magnet, Rod] = geompy.ExtractShapes(Partition_1, geompy.ShapeType["SOLID"], True)

BB1 = geompy.BasicProperties(Air)
BB2 = geompy.BasicProperties(Magnet)
BB3 = geompy.BasicProperties(Rod)

# Order parts by volume
order = {BB1[2]:Air, BB2[2]:Magnet, BB3[2]:Rod}
ordered = dict(sorted(order.items()))
Rod = list(ordered.items())[0][1]
Magnet = list(ordered.items())[1][1]
Air = list(ordered.items())[2][1]

farfield = geompy.CreateGroup(Partition_1, geompy.ShapeType["FACE"])
geompy.UnionIDs(farfield, [30])
#[Air, Magnet, Rod, farfield] = geompy.GetExistingSubObjects(Partition_1, False)

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
geompy.addToStudy( Sphere_1, 'Sphere_1' )
geompy.addToStudyInFather( Partition_1, Air, 'Air' )
geompy.addToStudy( Partition_1, 'Partition_1' )
geompy.addToStudyInFather( Partition_1, Magnet, 'Magnet' )
geompy.addToStudyInFather( Partition_1, Rod, 'Rod' )
geompy.addToStudyInFather( Partition_1, farfield, 'farfield' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(Partition_1,'Mesh_1')
NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 0.5 )
NETGEN_3D_Parameters_1.SetMinSize( 0.01 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 3 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(Magnet, 0.1)
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(Rod, 0.05)
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 3 )
Air_1 = Mesh_1.GroupOnGeom(Air,'Air',SMESH.VOLUME)
Magnet_1 = Mesh_1.GroupOnGeom(Magnet,'Magnet',SMESH.VOLUME)
Rod_1 = Mesh_1.GroupOnGeom(Rod,'Rod',SMESH.VOLUME)
farfield_1 = Mesh_1.GroupOnGeom(farfield,'farfield',SMESH.FACE)
isDone = Mesh_1.Compute()
[ Air_1, Magnet_1, Rod_1, farfield_1 ] = Mesh_1.GetGroups()
try:
  Mesh_1.ExportUNV( r'mesh.unv', 0 )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
