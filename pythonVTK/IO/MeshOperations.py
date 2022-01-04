"""
mesh处理函数
"""

def MeshPoissonSample(source, nums):
    """
    mesh泊松采样
    :param source:
    :param nums:
    :return:
    """
    # mesh 采样生成 pcd
    result = source.sample_points_poisson_disk(number_of_points=nums, init_factor=5)
    return result

