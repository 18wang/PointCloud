"""
VTK文件读取功能模块
可读取'.obj', '.stl', '.ply', '.txt' 文件

"""

from pathlib import Path
import numpy as np
import pandas as pd

from vtkmodules.vtkIOGeometry import (
    vtkOBJReader,
    vtkSTLReader,
)
from vtkmodules.vtkIOPLY import (
    vtkPLYReader,
)
from vtkmodules.vtkCommonCore import (
    vtkUnsignedCharArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkCellArray,
)

def readPolyData(file_name):
    """
    文件名分析并读取
    :param file_name:
    :return: polydata
    """
    valid_suffixes = ['.obj', '.stl', '.ply', '.txt']
    path = Path(file_name)
    if path.suffix:
        ext = path.suffix.lower()
    if ext not in valid_suffixes:
        print(f'No reader for this file suffix: {ext}')
        return None
    else:
        if ext == ".ply":
            reader = vtkPLYReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif ext == ".obj":
            reader = vtkOBJReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif ext == ".stl":
            reader = vtkSTLReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif ext == ".txt":

            read_csv_data = pd.read_csv(file_name, header=None, na_filter=False,
                                        delim_whitespace=True)
            temp_data = read_csv_data.to_numpy()
            # temp_data = np.loadtxt(file_name)

            isColorfulPoints = temp_data.shape[1] > 3
            if isColorfulPoints:
                # 彩色点云数据
                source_color = temp_data[:, 3:]
                # 0-255 RGB彩色
                source_color_int = [[int(i[0] * 255), int(i[1] * 255),
                                     int(i[2] * 255)] for i in source_color]
                colors = vtkUnsignedCharArray()
                colors.SetNumberOfComponents(3)

            # 点云数据点
            source_data = temp_data[:, 0:3]

            # points cell color 类型
            points = vtkPoints()
            poly_data = vtkPolyData()
            vtkCells = vtkCellArray()

            # 插入cell
            for i, p in enumerate(source_data):
                pointId = points.InsertNextPoint(p[:])  # 插入点
                vtkCells.InsertNextCell(1)
                vtkCells.InsertCellPoint(pointId)
                if isColorfulPoints:
                    colors.InsertNextTypedTuple(source_color_int[i])

            poly_data.SetPoints(points)
            poly_data.SetVerts(vtkCells)
            if isColorfulPoints:
                poly_data.GetPointData().SetScalars(colors)

        return poly_data