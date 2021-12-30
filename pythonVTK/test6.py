import vtk

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleRubberBandPick):

    def __init__(self, parent=None):
        self.AddObserver(vtk.vtkCommand.PickEvent, self.PickEvent)
        self.AddObserver(vtk.vtkCommand.KeyPressEvent, self.KeypressCallbackFunction)

        self.area_picker = vtk.vtkRenderedAreaPicker()
        self.area_picker.AddObserver(vtk.vtkCommand.EndPickEvent, self.EndPickEventfunc)
        self.area_picker.AddObserver(vtk.vtkCommand.PickEvent, self.PickEvent)
        return

    def KeypressCallbackFunction(self, obj, event):
        print('Key pressed!')

    def PickEvent(self, obj, event):
        print('PickEvent!')

    def EndPickEventfunc(self, obj, event):
        print('I was here!')
        clickPos = self.GetInteractor().GetEventPosition()


# A renderer and render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(.3, .4, .5)

renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)

# An interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renwin)

# add the custom style
style = MouseInteractorHighLightActor()
style.SetDefaultRenderer(renderer)
interactor.SetInteractorStyle(style)
interactor.SetPicker(style.area_picker)


# Add spheres to play with
for i in range(10):
    source = vtk.vtkSphereSource()

    source.SetRadius(vtk.vtkMath.Random(.5, 1.0))
    source.SetCenter(vtk.vtkMath.Random(-5, 5), vtk.vtkMath.Random(-5, 5), vtk.vtkMath.Random(-5, 5))
    source.SetPhiResolution(11)
    source.SetThetaResolution(21)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetDiffuseColor(vtk.vtkMath.Random(.4, 1.0), vtk.vtkMath.Random(.4, 1.0), vtk.vtkMath.Random(.4, 1.0))

    renderer.AddActor(actor)

# Start
interactor.Initialize()
interactor.Start()