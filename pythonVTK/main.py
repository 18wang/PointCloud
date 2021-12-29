

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import numpy as np
import MainForm
import vtk
from PyQt5 import QtWidgets
# vtkInteractionStyle vtkRenderingOpenGL2 交互与显示，虽不直接使用，但需要import
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray
)
from vtkmodules.util import (
    numpy_support
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
        super(QMainWindow, self).__init__(parent)
        self.ui = MainForm.Ui_MainWindow()
        self.ui.setupUi(self)
        # QtWidgets.QMainWindow.__init__(self, parent)
        #
        self.frame = QtWidgets.QFrame()

        # 添加vtkWidget
        self.vl = self.ui.verticalLayout
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        #
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()


        colors = vtkNamedColors()

        # colors.SetColor('bkg', [0.1, 0.2, 0.4, 1.0])

        # The source file
        file_name = "./data/彩色pz.txt"
        source_data = np.loadtxt(file_name)
        source_color = source_data[:, 3:]
        source_color_int = [[int(i[0]*255), int(i[1]*255), int(i[2]*255)] for i in source_color]
        source_data = source_data[:, 0:3]
        point_num = len(source_data)
        source = vtk.vtkPoints()
        source.SetData(numpy_support.numpy_to_vtk(source_data))


        points = vtk.vtkPoints()
        polydata = vtk.vtkPolyData()
        vtkCells = vtk.vtkCellArray()
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)

        for i, p in enumerate(source_data):

            pointId = points.InsertNextPoint(p[:])
            vtkCells.InsertNextCell(1)
            vtkCells.InsertCellPoint(pointId)
            colors.InsertNextTypedTuple(source_color_int[i])


        polydata.SetPoints(points)
        polydata.SetVerts(vtkCells)
        polydata.GetPointData().SetScalars(colors)


        mapper = vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        # mapper.SetLookupTable(lut)
        # mapper.SetColorModeToDefault()

        actor2 = vtkActor()
        actor2.SetMapper(mapper)

        self.ren.AddActor(actor2)


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

        # self.frame.setLayout(self.vl)
        # self.setCentralWidget(self.frame)
        #self.setCentralWidget(self.ui.verticalLayoutWidget)
        self.show()
        self.iren.Initialize()



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())



