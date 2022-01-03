import numpy as np
import open3d as o3d

# 直通滤波 PassThrough Filter
def PassThroughFilter(pcd, fieldName, limits, limitsNegative=False):
    """
    点云直通滤波
    :param pcd: 点云数据
    :param fieldName: 坐标轴 'x', 'y', 'z'
    :param limits: 过滤区间
    :param limitsNegative: 是否反选, 默认limits区间
    :return: 过滤后pcd, 过滤后剩余的点云坐标index
    """
    dictXYZ = {'x':0, 'y':1, 'z':2}
    source = np.asarray(pcd.points)

    # 判断滤波坐标轴
    try:
        xyz = dictXYZ[fieldName]
    except KeyError:
        print('滤波轴选择错误, 请选坐标轴 \'x\', \'y\', \'z\'')

    # 计算左右区间
    if limitsNegative:
        indexLeft = limits[0] >= source[:, xyz]
        indexRight = limits[1] <= source[:, xyz]
    else:
        indexLeft = limits[0] <= source[:, xyz]
        indexRight = limits[1] >= source[:, xyz]

    # 合并区间, 滤波
    index = np.logical_and(indexLeft, indexRight)
    PCD = source[index, :]

    # ndarray到pcd
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(PCD)
    return pcd, index

