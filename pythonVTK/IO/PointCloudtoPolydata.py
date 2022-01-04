"""
open3d pointcloud 转vtk polydata
"""
import numpy as np
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
)
# vtk <==> numpy 格式转换
from vtk.util import numpy_support

def PointCloudtoPolydata(source):

    # 点云点 点云颜色数据
    pointsData = np.asarray(source.points)
    colorData = np.asarray(source.colors)
    normalData = np.asarray(source.normals)

    # array 转 vtk 点
    points = vtkPoints()
    points.SetData(numpy_support.numpy_to_vtk(pointsData))
    result = vtkPolyData()
    result.SetPoints(points)

    # 判断是否为RGB点云
    if len(colorData) == len(pointsData):
        pass


    # 判断是否有法向量
    if len(normalData) == len(pointsData):
        result.GetCellData().SetNormals(numpy_support.numpy_to_vtk(normalData,
                                                                array_type=VTK_FLOAT))

    return result
