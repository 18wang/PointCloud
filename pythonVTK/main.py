import copy
import sys
import numpy as np


import MainForm
import vtk
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QFileDialog,
)

# vtkInteractionStyle vtkRenderingOpenGL2 交互与显示，虽不直接使用，但需要import
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkInteractionStyle import (
    vtkInteractorStyleTrackballCamera,
)
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkCellArray,
)
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray,
    vtkPoints,
    vtkCallbackCommand,
)
from vtkmodules.util import (
    numpy_support
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
    vtkAreaPicker,
    vtkRenderedAreaPicker,
)
# 嵌入qt 默认引用
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

#class Ui_MainWindow(QtWidgets.QMainWindow):
class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # 继承父类
        super(QMainWindow, self).__init__(parent)

        self.ui = MainForm.Ui_MainWindow()
        self.ui.setupUi(self)

#------------------ 自行添加的信号/槽 ------------------------------------
        self.ui.actionopen.triggered.connect(self.readFile)
        self.ui.actionCropHull.triggered.connect(self.cropHull)

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


    def getFile(self):
        """
        qFileDialog文件读取
        :return: fileName
        """
        fileName, _ = QFileDialog.getOpenFileName(self,
            'Open file', './', '点云文件(*.txt *.ply *.obj *.stl);;彩色点云文件(*.txt)')
        return fileName

    def ReadPolyData(self, file_name):
        """
        文件名分析并读取
        :param file_name:
        :return: polydata
        """
        valid_suffixes = ['.obj', '.stl', '.ply', '.txt']
        path = Path(file_name)
        if path.suffix:
            ext = path.suffix.lower()
        if path.suffix not in valid_suffixes:
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

                temp_data = np.loadtxt(file_name)

                isColorfulPoints = temp_data.shape[1] > 3
                if isColorfulPoints:
                    # 彩色点云数据
                    source_color = temp_data[:, 3:]
                    # 0-255 RGB彩色
                    source_color_int = [[int(i[0]*255), int(i[1]*255),
                                         int(i[2]*255)] for i in source_color]
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


    def readFile(self):
        """
        文件读取
        :return: bool
        """
        # The source file
        file_name = self.getFile()
        self.polydata = self.ReadPolyData(file_name)
        self.displayPolydata(self.polydata)
        return True


    def cropHull(self):
        """
        区域选取函数
        :return: bool
        """

        # 定义 鼠标点云选取类
        style = Mouse_Pointcloud_Selection(self.ren, self.polydata)
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)
        # 添加 area_picker
        self.iren.SetPicker(style.area_picker)

        return True



class Mouse_Pointcloud_Selection(vtk.vtkInteractorStyleRubberBandPick):
    """
    鼠标点云选取类
    """
    def __init__(self, render, data):
        self.data = data
        self.ren = render
        self.AddObserver(vtk.vtkCommand.PickEvent, self.PickEvent)
        self.AddObserver(vtk.vtkCommand.KeyPressEvent, self.KeypressCallbackFunction)

        self.area_picker = vtkRenderedAreaPicker()
        self.area_picker.AddObserver(vtk.vtkCommand.EndPickEvent, self.EndPickEventfunc)
        self.area_picker.AddObserver(vtk.vtkCommand.PickEvent, self.PickEvent)
        print(r'按 r 键锁定画面，鼠标左键框选，再按 r 释放画面。')
        return

    def KeypressCallbackFunction(self, obj, event):
        print('画面锁定，开始框选。')

    def PickEvent(self, obj, event):
        # clickPos = self.GetInteractor().GetEventPosition()
        # print(clickPos)
        print('区域已选中。')

    def EndPickEventfunc(self, obj, event):

        # 获取选中的 vtkPlanes
        frustum = self.area_picker.GetFrustum()
        # print(frustum)

        # 几何形状构建
        extractGeometry = vtkExtractGeometry()
        extractGeometry.SetImplicitFunction(frustum)
        extractGeometry.SetInputData(self.data)
        extractGeometry.Update()

        # Make a vtkPolyData with a vertex on each point.
        glyphFilter = vtkVertexGlyphFilter()
        glyphFilter.SetInputConnection(extractGeometry.GetOutputPort())
        glyphFilter.Update()

        selected = glyphFilter.GetOutput()

        colors = vtkNamedColors()


        # selected.GetPointData().SetScalars((0.1, 1, 0.))

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(selected)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d('Tomato'))
        # actor.GetProperty().SetPointSize(5)
        actors = self.ren.GetActors()
        print(actors, type(actors))
        self.ren.RemoveActor(actors)
        self.ren.AddActor(actor)






"""

        clickPos = self.GetInteractor().GetEventPosition()
        print(clickPos)

"""

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

