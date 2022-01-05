"""
Renderer 显示函数
"""

from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor


def UpdateActor(ren, index, actors, polydata):
    """
    更新 Actor
    :param ren: vtk.render 窗口
    :param index: actor 下标
    :param polydata: 显示数据
    :return:
    """
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtkActor()
    actor.SetMapper(mapper)
    # 替换旧显示
    ren.RemoveActor(actors[index])

    # 添加新显示
    ren.AddActor(actor)
    ren.ResetCamera()

    return actor