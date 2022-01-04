"""
Open3D文件读写

"""

import open3d as o3d
import numpy as np
from pathlib import Path

def readOpen3D(filename):
    """
    Open3D 文件读取
    :param filename: 文件名
    :return: 相应类型的数据
    """

    valid_suffixes = ['.stl', '.pcd', '.ply', '.txt']
    path = Path(filename)
    if path.suffix:
        ext = path.suffix.lower()
    if ext not in valid_suffixes:
        print(f'No reader for this file suffix: {ext}')
        return None
    else:
        if ext == ".stl":
            source = o3d.io.read_triangle_mesh(filename)

        elif ext == ".pcd" or ext == ".ply":
            source = o3d.io.read_point_cloud(filename)

        elif ext == ".txt":
            temp_data = np.loadtxt(filename)

            # 点云数据点
            source = o3d.geometry.PointCloud()
            source.points = o3d.utility.Vector3dVector(temp_data[:, 0:3])

            isColorfulPoints = temp_data.shape[1] > 3
            if isColorfulPoints:
                # 彩色点云数据
                source_color = temp_data[:, 3:]
                # 0-1 归一化RGB彩色
                source.colors = o3d.utility.Vector3dVector(source_color)

    print(source)
    return source