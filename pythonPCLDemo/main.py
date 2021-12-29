import pcl
import pcl.pcl_visualization
import numpy as np
import time

def transformPC(points, Mat):
    """
    点云变换
    :param points: 点云格式数据
    :param Mat: 变换矩阵
    :return: 变换后点云数据
    """
    cloud_out = np.array(points)
    cloud_out = np.concatenate((cloud_out, np.ones(len(cloud_out)).reshape(-1,1)), axis=1)

    c = np.dot(Mat, cloud_out.T).T[:, 0:3]
    c = np.array(c, dtype=np.float32)

    cloud_out = pcl.PointCloud(c)
    return cloud_out


def visualizationPC(points1, points2, points3):
    """
    点云可视化
    :param points:
    :return:
    """
    # visual = pcl.pcl_visualization.CloudViewing()
    # visual.ShowMonochromeCloud(points)


    # 新建视窗
    visual = pcl.pcl_visualization.PCLVisualizering()

    # 原始点云
    visual.AddPointCloud(points1, b'cloud_in', 0)

    # 变换点云
    cloudOutColor = pcl.pcl_visualization.PointCloudColorHandleringCustom(points2, 0, 255, 0)
    visual.AddPointCloud_ColorHandler(points2, cloudOutColor, b'cloud_out')
    # visual.AddPointCloud(points2, cloudOutColor, 0)

    # 配准点云
    cloudICPColor = pcl.pcl_visualization.PointCloudColorHandleringCustom(points3, 0, 0, 255)
    visual.AddPointCloud_ColorHandler(points3, cloudICPColor, b'cloud_ICP')

    # cloudICPColor = pcl.pcl_visualization.PointCloudColorHandleringCustom(0, 0, 255)
    # visual.AddPointCloud(points3, cloudICPColor, 0)

    visual.Spin()
    # visual.RemovePointCloud(b'scene_cloud', 0)
    return visual

"""
    range_image_color_handler = pcl.pcl_visualization.PointCloudColorHandleringCustom(point_cloud, 0, 0, 0)

    viewer.AddPointCloud_ColorHandler(point_cloud, range_image_color_handler, b'range image')

    keypoints_color_handler = pcl.visualization.PointCloudColorHandlerCustom[pcl.PointXYZ](keypoints_ptr, 0, 255, 0)
    viewer.addPointCloud(keypoints_ptr, keypoints_color_handler, keypoints)
    viewer.setPointCloudRenderingProperties(pcl.pcl_visualization.PCL_VISUALIZER_POINT_SIZE, 7, keypoints)
    keypoints_color_handler = pcl.PointCloudColorHandlerCustom(0, 255, 0)
    viewer.AddPointCloud(keypoints_ptr, keypoints_color_handler, keypoints)
    viewer.SetPointCloudRenderingProperties(pcl.pcl_visualization.PCL_VISUALIZER_POINT_SIZE, 7, keypoints)
"""
    # flag = True
    # while flag:
    #     flag != visual.WasStopped()

    # time.sleep(10)


def ICP(points1, points2, MI=1):
    """
    点云ICP
    :param points1: 待移动点云
    :param points2: 目标点云
    :param MI: 最大迭代次数
    :return:
    """
    icp = pcl.IterativeClosestPoint()
    # icp.setMaximumIterations(1)
    converged, transf, estimate, fitness = icp.icp(points1, points2)

    # std::cout << "has converged:" << icp.hasConverged() << " score: " << icp.getFitnessScore() << std::endl;
    # std::cout << icp.getFinalTransformation() << std::endl;
    # print('has converged:' + str(icp.hasConverged()) + ' score: ' + str(icp.getFitnessScore()) )
    # print(str(icp.getFinalTransformation()))
    print('has converged:' + str(converged) + ' score: ' + str(fitness))
    print(str(transf))

    # final = icp.align()
    return transf


if __name__ == "__main__":

    # lidar_path = "~/Documents/tutorials数据/correspondence_grouping/milk.pcd"
    lidar_path = "monkey.ply"

    # 读取点云
    cloud_in = pcl.load(lidar_path, format='ply')

    # 变换矩阵和点云变换
    theta = np.pi/20
    ZMove = 0
    Mat = np.mat([[np.cos(theta), -1*np.sin(theta), 0, 0],
                  [np.sin(theta), np.cos(theta), 0, 0],
                  [0, 0, 1, ZMove],
                  [0, 0, 0, 1]], dtype=np.float32)

    cloud_out = transformPC(cloud_in, Mat)
    print('transMatrix:\n', Mat, '\n\n')

    # 循环ICP
    Tmatrix = np.identity(4)
    cloud_ICP = cloud_out

    print(np.array(cloud_ICP)[0:5, :])

    # 新建视窗
    visual = pcl.pcl_visualization.PCLVisualizering()

    # 显示原始点云
    visual.AddPointCloud(cloud_in, b'cloud_in', 0)

    # 显示变换点云
    cloudOutColor = pcl.pcl_visualization.PointCloudColorHandleringCustom(cloud_out, 0, 255, 0)
    visual.AddPointCloud_ColorHandler(cloud_out, cloudOutColor, b'cloud_out')
    # visual.AddPointCloud(points2, cloudOutColor, 0)

    flag = True
    while flag:

        # visual.SpinOnce()
        visual.Spin()
        # visual.RemovePointCloud(b'scene_cloud', 0)

        for i in range(3):
            # 点云配准
            transf = ICP(cloud_ICP, cloud_in)
            Tmatrix = np.dot(transf, Tmatrix)
            print('Tmatrix:\n', Tmatrix, '\n')
            cloud_ICP = transformPC(cloud_ICP, transf)

            if i == 0:
                print(np.array(cloud_ICP)[0:5, :])

            # 显示配准点云
            cloudICPColor = pcl.pcl_visualization.PointCloudColorHandleringCustom(cloud_ICP, 0, 0, 255)
            visual.AddPointCloud_ColorHandler(cloud_ICP, cloudICPColor, bytes("cloud_ICP{}".format(str(i)), 'utf-8'), 0)
            visual.Spin()
            visual.RemovePointCloud(bytes("cloud_ICP{}".format(str(i)), 'utf-8'), 0)

        visual.Spin()
        # flag = not(visual.WasStopped())

        print('sleep 2s')
        time.sleep(2)

        quit()



        # 点云显示
        # combine = np.vstack((np.array(cloud_in), np.array(cloud_out)))
        # visualizationPC(pcl.PointCloud(combine))
        # visual = visualizationPC(cloud_in, cloud_out, cloud_ICP, visual)






# # 点云滤波
# fil = p.make_statistical_outlier_filter()
# fil.set_mean_k(50)
# fil.set_std_dev_mul_thresh(1.0)
# # fil.filter().to_file("inliers.pcd")
# points = fil.filter()
#
# icp = pcl.IterativeClosestPoint()

# points = pcl.load(lidar_path).to_array()[:, :3]
# points_num = points.shape[0]



# import pcl.pcl_visualization
# import numpy as np
#
# lidar_path = "./Meetal_nut.ply"
#
# # lidar_path 指定一个kitti 数据的点云bin文件就行了
# points = np.fromfile(lidar_path, dtype=np.float32)  # .astype(np.float16)
# points = points[0 : len(points)//4 * 4].reshape(-1, 4)
#
# # 这段代码省略，要在这里对第四列进行赋值，它代表颜色值，根据你自己的需要赋值即可；
# # points[:,3] =
#
#
# # PointCloud_PointXYZRGB 需要点云数据是N*4，分别表示x,y,z,RGB ,其中RGB 用一个整数表示颜色；
# color_cloud = pcl.PointCloud_PointXYZRGB(points)
# visual = pcl.pcl_visualization.CloudViewing()
# visual.ShowColorCloud(color_cloud, b'cloud')
# flag = True
# while flag:
#     flag != visual.WasStopped()


# # 这是一个示例 Python 脚本。
#
# # 按 Shift+F10 执行或将其替换为您的代码。
# # 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
#
# import pcl
#
# import numpy as np
#
#
#
# def generate_points():  # 产生1000个随机点
#     points = np.zeros((1000, 3))  # 建立一个1000*3的矩阵
#     for i in range(len(points)):  # 给矩阵赋随机值
#         points[i][0] = np.random.rand(1)
#         points[i][1] = np.random.rand(1)
#         points[i][2] = np.random.rand(1)
#     return points
#
#
# if __name__ == '__main__':
#     # points = generate_points()
#     points = pcl.load('Meetal_nut.ply')
#     print(points)
#     cloud = pcl.PointCloud()  # 定义点云为 pointcloud形式
#     cloud.from_array(np.array(points, dtype=np.float32))  # 把生成的随机点加入点云
#     pcl.save(cloud, "test_point_cloud.pcd")  # 存储点云为 test_point_cloud.pcd
#     visual = pcl.pcl_visualization.CloudViewing()
#     visual.ShowMonochromeCloud(cloud, b'cloud')  # 可视化点云
#     view = True
#     while view:
#         view = not (visual.WasStopped())
#
