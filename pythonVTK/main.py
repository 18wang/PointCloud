import copy
import sys
import numpy as np
import MainForm
import vtk

# 自定义程序类库
from Filtering.CropHull import Mouse_Pointcloud_Selection
from Filtering.PassThroughFilterUI import Ui_PTFDialog
from Registration.GlobalRegistration import GlobalRegistration
from Filtering.PassThroughFilter import (
    PassThroughFilter,
    PTFDialog,
)
from IO.VTKFileIO import readPolyData
from IO.Open3DFileIO import readOpen3D
from IO.PointCloudtoPolydata import PointCloudtoPolydata
from IO.MeshOperations import MeshPoissonSample


#
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QFileDialog,
)


# vtkInteractionStyle vtkRenderingOpenGL2 交互与显示，虽不直接使用，但需要import
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2

from vtkmodules.vtkIOPLY import (
    vtkPLYReader,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkCellArray,
)
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray,
    vtkPoints,
)
from vtkmodules.vtkIOGeometry import (
    vtkOBJReader,
    vtkSTLReader,
)
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
)
# vtk <==> numpy 格式转换
from vtk.util import numpy_support
# 嵌入qt 默认引用
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

#class Ui_MainWindow(QtWidgets.QMainWindow):
class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # 继承父类
        super(QMainWindow, self).__init__(parent)

        self.ui = MainForm.Ui_MainWindow()
        self.ui.setupUi(self)

        #------------------ 存放重要的系统参数 ---------------------------------
        self.polydata = []   # vtk 显示数据
        self.actor = []       # vtk actor
        self.pointcloud = []  # open3d 数据
        self.Mark = dict()              # 类型标记

        #-------------------------------------------------------------------


        #------------------ 手动添加的信号/槽 ------------------------------------
        self.ui.actionopen.triggered.connect(self.readFile)
        self.ui.actionopenStl.triggered.connect(self.readSTL)

        self.ui.actionCropHull.triggered.connect(self.cropHull)
        self.ui.actionzhitong.triggered.connect(self.passThrough)

        self.ui.actionGlobalRegist.triggered.connect(self.globalRegist)

        self.ui.actionClearDisplay.triggered.connect(self.clearDisplay)

        #---------------------------------------------------------------------

        self.frame = QFrame()

        # 向 verticalLayout 中添加 vtkWidget
        self.vl = self.ui.verticalLayout
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        # 新建 vtkRenderer
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()


    def readFile(self):
        """
        txt文件读取
        :return: bool
        """
        # The source file
        fileName, _ = QFileDialog.getOpenFileName(self,
                        'Open file', './', '点云文件(*.txt);;RGB点云文件(*.txt)')
        self.polydata.append(readPolyData(fileName))
        self.pointcloud.append(readOpen3D(fileName))
        self.Mark['.txt'] = len(self.pointcloud) - 1
        self.displayPolydata(self.polydata[-1])
        return True

    def readSTL(self):
        """
        stl文件读取
        :return: bool
        """
        # The source file
        fileName, _ = QFileDialog.getOpenFileName(self,
                        'Open file', './', 'STL文件(*.stl)')
        self.polydata.append(readPolyData(fileName))
        self.pointcloud.append(readOpen3D(fileName))
        self.Mark['.stl'] = len(self.pointcloud) - 1
        self.displayPolydata(self.polydata[-1])
        return True



    def displayPolydata(self, polydata):
        """
        polydata显示
        :param polydata:
        :return:
        """
        # 添加polydata
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(polydata)

        actor = vtkActor()
        actor.SetMapper(mapper)
        self.actor.append(actor)
        self.ren.AddActor(actor)

        if False:

            # 绘制scalar_bar

            # scalar_bar 的 lut
            bar_lut = vtkLookupTable()
            bar_lut.Build()
            # create the scalar_bar
            scalar_bar = vtkScalarBarActor()
            scalar_bar.SetOrientationToHorizontal()
            scalar_bar.SetLookupTable(bar_lut)

            # create the scalar_bar_widget
            self.scalar_bar_widget = vtkScalarBarWidget()
            self.scalar_bar_widget.SetInteractor(self.iren)
            self.scalar_bar_widget.SetScalarBarActor(scalar_bar)
            self.scalar_bar_widget.On()

        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

        return True


    def globalRegist(self):
        """
        点云和stl全局配准函数
        :return:
        """
        stlIndex = self.Mark[".stl"]
        txtIndex = self.Mark[".txt"]
        print(self.pointcloud[txtIndex])
        # voxel_size 可以设置为用户可调，另有其他几个超参数，可设置接口
        pointsNum = len(np.asarray(self.pointcloud[txtIndex].points))
        stlSample = MeshPoissonSample(self.pointcloud[stlIndex], pointsNum)
        result = GlobalRegistration(self.pointcloud[txtIndex], stlSample,
            voxel_size=1)
        transMatrix = np.array(result.transformation)
        GRsource = copy.deepcopy(self.pointcloud[txtIndex])
        GRsource.transform(transMatrix)

        # print(np.asarray(self.pointcloud[txtIndex].points), '\n\n', np.asarray(GRsource.points))

        # 类型变换 PointCloud => polydata
        temp = PointCloudtoPolydata(GRsource)
        self.polydata[txtIndex] = temp
        print(numpy_support.vtk_to_numpy(temp.GetPoints().GetData()))
        # self.polydata[txtIndex] = PointCloudtoPolydata(GRsource)


        mapper = vtkPolyDataMapper()
        mapper.SetInputData(self.polydata[txtIndex])

        actor = vtkActor()
        actor.SetMapper(mapper)
        # 替换旧显示
        self.ren.RemoveActor(self.actor[txtIndex])
        self.actor[txtIndex] = actor

        # 添加新显示
        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

    def cropHull(self):
        """
        区域选取函数
        :return: bool
        """

        # 定义 鼠标点云选取类
        style = Mouse_Pointcloud_Selection(self, self.ren, self.polydata)
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)
        # 添加 area_picker
        self.iren.SetPicker(style.area_picker)

        return True


    def passThrough(self):
        """
        直通滤波功能
        :return:
        """
        self.ptDialog = PTFDialog()
        self.ptDialog.SetPTF.connect(self.runPassThrough)

        self.ptDialog.show()

        # https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/
        # https://discourse.vtk.org/t/convert-vtk-array-to-numpy-array/3152


    def runPassThrough(self, params):
        pcd, fieldName, limits = params
        print('主窗口', params)


    def clearDisplay(self):
        """
        清除VTK显示窗口
        :return:
        """
        # 清空显示
        for act in self.actor:
            self.ren.RemoveActor(act)

        # 清空元素
        self.actor = []
        self.polydata = []
        self.pointcloud = []
        self.Mark = dict()

        return









if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

