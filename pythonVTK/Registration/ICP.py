"""
ICP功能函数
"""

import open3d as o3d

def ICPP2P(source, target, trans_init, threshold=0.5, maxIteration=30):

    # ICP 配准 默认30次迭代
    print("Apply point-to-point ICP")
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=maxIteration))
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    return reg_p2p


def ICPP2l(source, target, trans_init, threshold=0.5, maxIteration=30):

    print("Apply point-to-plane ICP")
    reg_p2l = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=maxIteration))
    print(reg_p2l)
    print("Transformation is:")
    print(reg_p2l.transformation)

    return reg_p2l



