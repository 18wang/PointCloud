# vtkInteractionStyle vtkRenderingOpenGL2 交互与显示，虽不直接使用，但需要import
from PyQt5.QtWidgets import (
    QFileDialog,
)

import vtk
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkInteractionStyle import (
    vtkInteractorStyleTrackballCamera,
)
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOPLY import (
    vtkPLYReader,
    vtkPLYWriter,
)
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


class Mouse_Pointcloud_Selection(vtk.vtkInteractorStyleRubberBandPick):
    """
    鼠标点云选取类
    """
    def __init__(self, qWidget, render, data):
        self.qWidget = qWidget
        self.ren = render
        self.data = data

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

    def savePolydata(self):
        """
        qFileDialog文件读取
        :return: fileName
        """
        fileName = QFileDialog.getSaveFileName(self.qWidget,
            'Save file', './', '点云文件(*.txt *.ply *.obj *.stl);;彩色点云文件(*.txt)')
        return fileName

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
        actor.GetProperty().SetColor(colors.GetColor3d('light_salmon'))
        # actor.GetProperty().SetPointSize(5)               # 设置点云大小
        lastActor = self.ren.GetActors().GetLastActor()     # 获取最后添加的 Actor
        self.ren.RemoveActor(lastActor)                     # 移除最后的 Actor
        self.ren.AddActor(actor)            # 添加新截取的部分

        fileName = self.savePolydata()
        print(fileName)
        plyWriter = vtkPLYWriter()
        plyWriter.SetFileName(fileName[0])
        plyWriter.SetInputData(selected)
        plyWriter.Write()
