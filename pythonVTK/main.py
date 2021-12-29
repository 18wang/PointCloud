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
#--------------------------------------------------------------------
        self.ui.actionopen.triggered.connect(self.readTxt)


#---------------------------------------------------------------------
        self.frame = QFrame()

        # 添加vtkWidget
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
            'Open file', './', '点云文件(*.txt *.ply *.obj *.stl)')
        return fileName

    def ReadPolyData(self, file_name):
        valid_suffixes = ['.obj', '.stl', '.ply']
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

            return poly_data

    def readTxt(self):

        # The source file
        file_name = self.getFile()
        # source_data = np.loadtxt(file_name)
        # source_color = source_data[:, 3:]
        # # 0-255 RGB彩色
        # source_color_int = [[int(i[0]*255), int(i[1]*255),
        #                      int(i[2]*255)] for i in source_color]
        # # 点云数据点
        # source_data = source_data[:, 0:3]
        #
        # # points cell color 类型
        # points = vtkPoints()
        # polydata = vtkPolyData()
        # vtkCells = vtkCellArray()
        # colors = vtkNamedColors()
        # colors = vtkUnsignedCharArray()
        # colors.SetNumberOfComponents(3)
        #
        # # 插入cell
        # for i, p in enumerate(source_data):
        #
        #     pointId = points.InsertNextPoint(p[:])  # 插入点
        #     vtkCells.InsertNextCell(1)
        #     vtkCells.InsertCellPoint(pointId)
        #     colors.InsertNextTypedTuple(source_color_int[i])
        #
        #
        # polydata.SetPoints(points)
        # polydata.SetVerts(vtkCells)
        # polydata.GetPointData().SetScalars(colors)


        polydata = self.ReadPolyData(file_name)
        self.displayPolydata(polydata)

        return True

    def displayPolydata(self, polydata):

        # 添加polydata
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(polydata)

        actor = vtkActor()
        actor.SetMapper(mapper)
        self.ren.AddActor(actor)

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



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

