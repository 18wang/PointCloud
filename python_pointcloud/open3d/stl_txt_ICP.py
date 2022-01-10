import open3d as o3d
import numpy as np
import time
import copy

def draw_registration_result(source, target, transformation):
    """
    点云配准可视化函数
    :param source: 待配准点云 黄色
    :param target: 目标点云 青绿色
    :param transformation: 变换矩阵
    :return: None
    """
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4459,
                                      front=[0.9288, -0.2951, -0.2242],
                                      lookat=[1.6784, 2.0612, 1.4451],
                                      up=[-0.3402, -0.9189, -0.1996])


def preprocess_point_cloud(pcd, voxel_size):
    """
    点云预处理 降采样
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


def prepare_dataset(source, target, voxel_size):
    """
    点云文件读取和整理函数
    :param voxel_size: 体素大小
    :return: source, target, source_down, target_down, source_fpfh, target_fpfh
    """
    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source_down, target_down, source_fpfh, target_fpfh


def txt2PointCloud(path):
    """
    txt 到 点云
    :param path: 文件路径
    :return: pcd 点云文件
    """
    with open(path) as temp:
        points = temp.read()
        points = points.strip().split('\n')

        PointXYZ = []
        for i in points:
            PointXYZ.append([float(x) for x in i.split(' ')])

    temp = np.asarray(PointXYZ)
    source = o3d.geometry.PointCloud()
    source.points = o3d.utility.Vector3dVector(temp)
    return source

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    """
    全局匹配函数
    :param source_down:
    :param target_down:
    :param source_fpfh:
    :param target_fpfh:
    :param voxel_size:
    :return:
    """
    distance_threshold = voxel_size * 1.5
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


def ICPP2P(source, target, threshold, trans_init, maxIteration=30):
    # 开始时间
    startTime = time.time()

    # ICP 配准 默认30次迭代
    print("Apply point-to-point ICP")
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=maxIteration))
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    endTime = time.time()
    print('运算时间: {} s'.format(endTime - startTime), '\n')
    return reg_p2p


def ICPP2l(source, target, threshold, trans_init, maxIteration=30):
    # 开始时间
    startTime = time.time()

    print("Apply point-to-plane ICP")
    reg_p2l = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=maxIteration))
    print(reg_p2l)
    print("Transformation is:")
    print(reg_p2l.transformation)
    endTime = time.time()
    print('运算时间: {} s'.format(endTime - startTime), '\n')
    return reg_p2l



if __name__ == "__main__":

    # 读取txt扫描数据文件 返回 pcd
    sourcePath = "../../../data/曲面6-2.txt"
    source = txt2PointCloud(sourcePath)


    # 读取 mesh
    targetPath = "../../../data/壳体.stl"
    mesh = o3d.io.read_triangle_mesh(targetPath)

    # mesh 采样生成 pcd
    numbers_of_points = len(source.points)
    target = mesh.sample_points_poisson_disk(number_of_points=numbers_of_points, init_factor=5)

    # 原始数据显示
    o3d.visualization.draw_geometries([source, target])


    # # 读取点云, 降采样待粗配准
    voxel_size = 1  #
    source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(source, target, voxel_size)
    # draw_registration_result(source_down, target_down, np.identity(4))

    # 粗配准, 及结果显示
    result_ransac = execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)
    trans_init = np.array(result_ransac.transformation)
    print("全局配准结果:", result_ransac)
    print("全局配准矩阵:", trans_init)
    print('\n')
    draw_registration_result(source_down, target_down, trans_init)


    # 点对点ICP
    threshold = 0.5    # 阈值匹配
    reg_p2p = ICPP2P(source, target, threshold, trans_init, 1000)
    draw_registration_result(source, target, reg_p2p.transformation)

    # # 点对面ICP
    # reg_p2l = ICPP2l(source, target, threshold, trans_init, 1000)
    # draw_registration_result(source, target, reg_p2l.transformation)


    """
    threshold的选取比较重要，和物体尺寸高度相关，一般物体尺寸越大，阈值越小，反之则越大。
    和点云的密度也有一定的关系，但尚不明确。
    由于threshold选取不当，可能造成粗、精配准不收敛，增加迭代次数不能使其收敛。
    """

    # # 距离计算
    # dists = source.compute_point_cloud_distance(target)
    #
    # dists = np.asarray(dists)
    # ind = np.where(dists > 0.01)[0]
    # pcd_without_chair = source.select_by_index(ind)
    # o3d.visualization.draw_geometries([pcd_without_chair],
    #                                   zoom=0.3412,
    #                                   front=[0.4257, -0.2125, -0.8795],
    #                                   lookat=[2.6172, 2.0475, 1.532],
    #                                   up=[-0.0694, -0.9768, 0.2024])



