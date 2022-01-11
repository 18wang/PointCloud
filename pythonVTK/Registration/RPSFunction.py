from vtkmodules.vtkCommonDataModel import vtkPointLocator
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkPointPicker


class MouseInteractorICP(vtkInteractorStyleTrackballCamera):

    def __init__(self, render=None, actor=None):
        self.AddObserver("LeftButtonPressEvent", self.onLeftButtonDown)
        self.LastPickedPoints = None
        self.Render = render
        self.Actor = actor

    def onLeftButtonDown(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        #  Pick from this location.
        picker = vtkPointLocator()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        self.LastPickedPoints = picker.GetActor()

        # If we picked something before, remove the silhouette actor and
        # generate a new one.
        if self.LastPickedPoints:
            self.GetDefaultRenderer().RemoveActor(self.Actor)

            # Highlight the picked actor by generating a silhouette
            self.Render.SetInputData(self.LastPickedPoints.GetMapper().GetInput())
            self.GetDefaultRenderer().AddActor(self.Actor)

        #  Forward events
        self.OnLeftButtonDown()
        return
