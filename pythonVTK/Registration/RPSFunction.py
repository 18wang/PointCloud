import numpy as np
import open3d as o3d
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkCommand, vtkMinimalStandardRandomSequence
from vtkmodules.vtkCommonDataModel import vtkPointLocator
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkPointPicker,
    vtkRenderWindowInteractor, vtkPolyDataMapper, vtkActor, vtkPropPicker,
)


class MouseInteractorICP(vtkInteractorStyleTrackballCamera):

    def __init__(self, actor=None):
        self.AddObserver(vtkCommand.RightButtonPressEvent, self.onRightButtonDown)
        self.AddObserver(vtkCommand.KeyPressEvent, self.action)
        self.Actor = actor              # actor
        self.StlSelected = []           # 模型被选中的点
        self.PointsSelected = []        # 点云被选中的点
        self.StlSphere = []
        self.PointsSphere = []
        self.Flag = 0

        print("::请按 n 键开始选点，再次按 n 键进入下一个对象，第3"
              "次按 n 键完成选择。\n  按C键清空本对象的点选。")

    def onRightButtonDown(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        # #  Pick from this location.
        # picker = vtkPointLocator()
        print(clickPos[0], clickPos[1])
        # # 设置点云数值
        # picker.SetDataSet(self.Data[self.Flag-1])
        # picker.BuildLocator()
        # # 最近点ID
        # pointId = picker.FindClosestPoint((clickPos[0], clickPos[1], 0))

        #------------------------------------------
        picker = vtkPointPicker()
        # picker = vtkPropPicker()
        picker.SetTolerance(0.01)


        result = picker.Pick(float(clickPos[0]), float(clickPos[1]), 0,
                             self.GetDefaultRenderer())

        if not result:
            # 未选中点云，则程序退出
            return
        pointId = picker.GetPointId()

        xyz = picker.GetPickPosition()

        if self.Flag == 1:

            # xyz = self.Data[self.Flag - 1].GetPoint(pointId)
            self.StlSelected.append(xyz)

            sphere = self.markSphere(xyz, len(self.StlSelected))
            self.StlSphere.append(sphere)
        else:

            # xyz = self.Data[self.Flag - 1].GetPoint(pointId)
            self.PointsSelected.append(xyz)

            sphere = self.markSphere(xyz, len(self.PointsSelected))
            self.PointsSphere.append(sphere)

        print(xyz)

        self.GetDefaultRenderer().AddActor(sphere)

        self.OnRightButtonDown()
        return


    def markSphere(self, xyz, id):
        """
        选点位置标记球体
        :param xyz:
        :param id:
        :return: actor
        """
        source = vtkSphereSource()
        randomSequence = vtkMinimalStandardRandomSequence()
        randomSequence.SetSeed(id)
        colors = vtkNamedColors()

        radius = 2.5

        source.SetRadius(radius)
        source.SetCenter(*xyz)
        source.SetPhiResolution(11)
        source.SetThetaResolution(21)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(mapper)

        r = randomSequence.GetRangeValue(0, 1.0)
        randomSequence.Next()
        g = randomSequence.GetRangeValue(0, 1.0)
        randomSequence.Next()
        b = randomSequence.GetRangeValue(0, 1.0)
        randomSequence.Next()

        actor.GetProperty().SetDiffuseColor(r, g, b)
        actor.GetProperty().SetDiffuse(0.8)
        actor.GetProperty().SetSpecular(0.5)
        actor.GetProperty().SetSpecularColor(colors.GetColor3d('White'))
        actor.GetProperty().SetSpecularPower(30.0)

        return actor


    def action(self, obj, event):
        # 判断按键事件
        keyPressed = self.GetInteractor().GetKeySym()
        if keyPressed == 'n':
            self.pointPicker()
        elif keyPressed == 'c':
            self.clearPoints()

        return

    def pointPicker(self):
        """
        鼠标点选函数
        :return:
        """
        if self.Flag == 0:
            print("模型选点")
            self.GetDefaultRenderer().RemoveActor(self.Actor[1])
            self.GetDefaultRenderer().ResetCamera()
            self.GetInteractor().Initialize()


        if self.Flag == 1:
            if len(self.StlSelected) < 3:
                print('未选满3个点，继续选择')
                return
            print("点云选点")
            self.GetDefaultRenderer().RemoveAllViewProps()
            self.GetDefaultRenderer().AddActor(self.Actor[1])
            self.GetDefaultRenderer().ResetCamera()
            self.GetInteractor().Initialize()

        if self.Flag == 2:
            if len(self.StlSelected) < 3 or \
                    len(self.StlSelected) != len(self.PointsSelected):
                print('点选数量有误！')

            print("完成点选")
            # 清除所有 可视对象
            self.GetDefaultRenderer().RemoveAllViewProps()
            self.GetDefaultRenderer().ResetCamera()
            self.GetInteractor().Initialize()



        self.Flag += 1
        return

    def getActor(self):

        return self.Actor


    def getSelected(self):
        return [self.StlSelected, self.PointsSelected]


    def clearPoints(self):
        if self.Flag == 1:
            for actor in self.StlSphere:
                self.GetDefaultRenderer().RemoveActor(actor)
            self.StlSelected = []

        if self.Flag == 2:
            for actor in self.PointsSphere:
                self.GetDefaultRenderer().RemoveActor(actor)
            self.PointsSelected = []

        self.GetDefaultRenderer().ResetCamera()
        self.GetInteractor().Initialize()

        return





def RPS(stlSample, pointData, stlSelected, pointSelected):
    """
    根据选定点坐标返回变换矩阵
    :param stlSample:
    :param pointData:
    :param stlSelected:
    :param pointSelected:
    :return:
    """
    pointSelected = np.asarray(pointSelected).T
    stlSelected = np.asarray(stlSelected).T

    trans = umeyama(pointSelected, stlSelected)

    print("手动选点粗配准矩阵：",trans, '\n')

    threshold = 0.03  # 3cm distance threshold
    reg_p2p = o3d.pipelines.registration.registration_icp(
        pointData, stlSample, threshold, trans,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())

    return reg_p2p.transformation


def umeyama(A, B):
    """
    根据一组对应点对变换，求取粗变换矩阵
    :param A:
    :param B:
    :return:
    """

    assert A.shape == B.shape

    num_rows, num_cols = A.shape
    if num_rows != 3:
        raise Exception(f"matrix A is not 3xN, it is {num_rows}x{num_cols}")

    num_rows, num_cols = B.shape
    if num_rows != 3:
        raise Exception(f"matrix B is not 3xN, it is {num_rows}x{num_cols}")

    # find mean column wise
    centroid_A = np.mean(A, axis=1)
    centroid_B = np.mean(B, axis=1)

    # ensure centroids are 3x1
    centroid_A = centroid_A.reshape(-1, 1)
    centroid_B = centroid_B.reshape(-1, 1)

    # subtract mean
    Am = A - centroid_A
    Bm = B - centroid_B

    H = Am @ np.transpose(Bm)

    # sanity check
    # if linalg.matrix_rank(H) < 3:
    #    raise ValueError("rank of H = {}, expecting 3".format(linalg.matrix_rank(H)))

    # find rotation
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # special reflection case
    if np.linalg.det(R) < 0:
        print("det(R) < R, reflection detected!, correcting for it ...")
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    t = -R @ centroid_A + centroid_B

    trans = np.concatenate((R, t.reshape(-1, 1)), axis=1)
    trans = np.concatenate((trans, np.reshape([0, 0, 0, 1], (1, -1))), axis=0)
    return trans