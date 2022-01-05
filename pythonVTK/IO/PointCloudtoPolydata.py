"""
open3d pointcloud 转vtk polydata
"""
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData, vtkCellArray,
)
# vtk <==> numpy 格式转换
from vtk.util import numpy_support

def PointCloudtoPolydata(source):

    # 点云点 点云颜色数据
    pointsData = np.asarray(source.points)
    colorData = np.asarray(source.colors)
    normalData = np.asarray(source.normals)

    # 判断是否为RGB点云
    isColorfulPoints = len(colorData) == len(pointsData)
    haveNormal = len(normalData) == len(pointsData)

    # array 转 vtk 点
    points = vtkPoints()
    vtkCells = vtkCellArray()
    result = vtkPolyData()
    colors = vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)

    # 插入cell
    for i, p in enumerate(pointsData):
        pointId = points.InsertNextPoint(p[:])  # 插入点
        vtkCells.InsertNextCell(1)
        vtkCells.InsertCellPoint(pointId)
        if isColorfulPoints:
            source_color_int = [[int(i[0] * 255), int(i[1] * 255),
                                 int(i[2] * 255)] for i in colorData]
            colors.InsertNextTypedTuple(source_color_int[i])

    result.SetPoints(points)
    result.SetVerts(vtkCells)

    # 判断是否有法向量
    if haveNormal:
        result.GetCellData().SetNormals(numpy_support.numpy_to_vtk(
            normalData, array_type=VTK_FLOAT))

    return result
