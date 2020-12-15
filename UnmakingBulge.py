# Unmaking Bulge - generates 2 meshes: 1 for the "main material" and 1 for the thermally expanding microspheres
# Inputs: model mesh, mesh that defines start of bulging plane, and height of bulge.
# Author: Katherine Song
# Last modified: Dec 2020

import Rhino
import scriptcontext
import rhinoscriptsyntax as rs

import System
from System.Threading import Tasks as tasks
from System.Collections.Generic import List

def Bulge():

    input_mesh_id = rs.GetObjects("Select model mesh", 32, True, False)
    if not input_mesh_id: return

    cutter_mesh_id = rs.GetObjects("Select mesh defining bottom of bulge", 32, True, False, False)
    if not cutter_mesh_id: return

    bulge_height = rs.GetReal("Enter bulge chamber height", 5.0, 1.0)
    if not bulge_height: return

    input_mesh = rs.coercemesh(input_mesh_id, True)
    offset_mesh = input_mesh.Offset(0.5)
    input_brep = Rhino.Geometry.Brep.CreateFromMesh(offset_mesh, False)

    cutter_mesh = rs.coercemesh(cutter_mesh_id, True)
    cutter_brep = Rhino.Geometry.Brep.CreateFromMesh(cutter_mesh, False)
    offset_cutter_meshes = Rhino.Geometry.Mesh.Offset(cutter_mesh, bulge_height, True)
    cutter_brep = Rhino.Geometry.Brep.CreateFromMesh(offset_cutter_meshes, False)

    brep_pieces = Rhino.Geometry.Brep.Split(input_brep, cutter_brep, 0.01)
    inner_chamber_brep = brep_pieces[2] # may need to manually change this index for some models/cuts
    scriptcontext.doc.Objects.AddBrep(inner_chamber_brep)

    inner_chamber_mesh = Rhino.Geometry.Mesh()
    mesh_array = Rhino.Geometry.Mesh.CreateFromBrep(inner_chamber_brep)
    for mesh in mesh_array:
        inner_chamber_mesh.Append(mesh)
    inner_chamber_mesh.FillHoles()
    scriptcontext.doc.Objects.AddMesh(inner_chamber_mesh) # TEM mesh
    inner_chamber_mesh.Flip(True, True, True)
    inner_chamber_mesh.Append(input_mesh)
    scriptcontext.doc.Objects.AddMesh(inner_chamber_mesh) # main material mesh

    #for brep_piece in inner_chamber[0]:
    #    scriptcontext.doc.Objects.AddBrep(brep_piece)
      #doc.Objects.Delete(obj_ref, False)
    scriptcontext.doc.Views.Redraw()
    return Rhino.Commands.Result.Success
Bulge()
