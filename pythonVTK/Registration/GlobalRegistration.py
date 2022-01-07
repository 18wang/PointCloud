"""
全局配准函数

"""

import open3d as o3d
import numpy as np


from GlobalRegistrationUI import Ui_GlobalRegistration
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QDialog,
)

class GlobalRegistraionDialog(QDialog):
    setGR = pyqtSignal(list)
    def __init__(self):
        super(GlobalRegistraionDialog, self).__init__()
        self.ui = Ui_GlobalRegistration()
        self.ui.setupUi(self)

        self.ui.ok.clicked.connect(self.returnParams)
        self.ui.cancel.clicked.connect(self.close)

    def returnParams(self):
        voxelSize = self.ui.voxelSize.text()
        distanceThreshold = self.ui.distanceThreshold.text()
        self.close()
        self.setGR.emit([voxelSize, distanceThreshold])



def GlobalRegistration(source, target, voxel_size=1, distance_threshold=2):
    """
    ransac 全局配准
    :param source:
    :param target:
    :param voxel_size: 下采样大小
    :return: 配准结果
    """

    # 降采样 粗配准
    source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(source, target,
                                                                         voxel_size)

    # 粗配准, 及结果显示
    result_ransac = execute_fast_global_registration(source_down, target_down,
                            source_fpfh, target_fpfh, voxel_size, distance_threshold)
    trans_init = np.array(result_ransac.transformation)
    print("全局配准结果:", result_ransac)
    print("全局配准矩阵:", trans_init)
    print('\n')

    return result_ransac


def preprocess_point_cloud(pcd, voxel_size=1):
    """
    点云预处理 降采样, 计算法向量, 计算特征直方图
    :param pcd: 点云数据
    :param voxel_size: 体素采样大小
    :return: 降采样后点云, FPFH点快速特征直方图
    """
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def prepare_dataset(source, target, voxel_size=1):
    """
    点云文件预处理函数, 降采样, 计算法向量, 计算特征直方图
    :param voxel_size: 体素大小
    :return: source, target, source_down, target_down, source_fpfh, target_fpfh
    """
    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source_down, target_down, source_fpfh, target_fpfh


def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size, distance_threshold):
    """
    全局匹配函数
    :param source_down:
    :param target_down:
    :param source_fpfh:
    :param target_fpfh:
    :param voxel_size:
    :return:
    """

    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result


def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size, distance_threshold):
    if not distance_threshold:
        distance_threshold = voxel_size * 0.5
    print(":: Apply fast global registration with distance threshold %.3f" \
            % distance_threshold)
    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result


