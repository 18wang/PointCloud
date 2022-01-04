#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


# def get_program_parameters():
#     import argparse
#     description = 'Read a .stl file.'
#     epilogue = ''''''
#     parser = argparse.ArgumentParser(description=description, epilog=epilogue,
#                                      formatter_class=argparse.RawDescriptionHelpFormatter)
#     parser.add_argument('filename', help='42400-IDGH.stl')
#     args = parser.parse_args()
#     return args.filename
#
#
# def main():
#     colors = vtkNamedColors()
#
#     filename = get_program_parameters()
#
#     reader = vtkSTLReader()
#     reader.SetFileName(filename)
#
#     mapper = vtkPolyDataMapper()
#     mapper.SetInputConnection(reader.GetOutputPort())
#
#     actor = vtkActor()
#     actor.SetMapper(mapper)
#     actor.GetProperty().SetDiffuse(0.8)
#     actor.GetProperty().SetDiffuseColor(colors.GetColor3d('LightSteelBlue'))
#     actor.GetProperty().SetSpecular(0.3)
#     actor.GetProperty().SetSpecularPower(60.0)
#
#     # Create a rendering window and renderer
#     ren = vtkRenderer()
#     renWin = vtkRenderWindow()
#     renWin.AddRenderer(ren)
#     renWin.SetWindowName('ReadSTL')
#
#     # Create a renderwindowinteractor
#     iren = vtkRenderWindowInteractor()
#     iren.SetRenderWindow(renWin)
#
#     # Assign actor to the renderer
#     ren.AddActor(actor)
#     ren.SetBackground(colors.GetColor3d('DarkOliveGreen'))
#
#     # Enable user interface interactor
#     iren.Initialize()
#     renWin.Render()
#     iren.Start()


# if __name__ == '__main__':
    # main()
colors = vtkNamedColors()

# filename = get_program_parameters()
filename = "../../pythonVTK/ProjectSrc/Meetal_nut.ply"

reader = vtkPLYReader()
reader.SetFileName(filename)
reader.Update()



# vtk <==> numpy 格式转换
from vtk.util import numpy_support

polydata = reader.GetOutput()
points = polydata.GetPoints()
cells = polydata.GetPolys()
cellsOffSet = cells.GetOffsetsArray()
array = points.GetData()
cellArray = cells.GetData()
cell_nodes = numpy_support.vtk_to_numpy(cellArray)
cell_OffSetarray = numpy_support.vtk_to_numpy(cellsOffSet)
numpy_nodes = numpy_support.vtk_to_numpy(array)


array2 = numpy_support.numpy_to_vtk(numpy_nodes)
points2 = vtkPoints()
points2.SetData(array2)
polydata2 = vtkPolyData()
polydata2.SetPoints(points2)

cellArray2 = numpy_support.numpy_to_vtkIdTypeArray(cell_nodes)
cells2 = vtkCellArray()
cells2.SetData(numpy_support.numpy_to_vtkIdTypeArray(cell_OffSetarray), cellArray2)
polydata2.SetPolys(cells2)


from vtk.numpy_interface import dataset_adapter as dsa

polydata3 = reader.GetOutput()
numpy_array_of_points = dsa.WrapDataObject(polydata3).Points
numpy_nodes2 = numpy_support.vtk_to_numpy(numpy_array_of_points)


mapper = vtkPolyDataMapper()
# mapper.SetInputData(polydata2)


# mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuse(0.8)
actor.GetProperty().SetDiffuseColor(colors.GetColor3d('LightSteelBlue'))
actor.GetProperty().SetSpecular(0.3)
actor.GetProperty().SetSpecularPower(60.0)

# Create a rendering window and renderer
ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('ReadSTL')

# Create a renderwindowinteractor
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Assign actor to the renderer
ren.AddActor(actor)
ren.SetBackground(colors.GetColor3d('DarkOliveGreen'))

# Enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()





