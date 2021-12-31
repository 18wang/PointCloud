#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkMinimalStandardRandomSequence
)
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkSphereSource
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

"""
There are two alternative ways to apply the transform.
 1) Use vtkTransformPolyDataFilter to create a new transformed polydata.
    This method is useful if the transformed polydata is needed
      later in the pipeline
    To do this, set USER_MATRIX = True
 2) Apply the transform directly to the actor using vtkProp3D's SetUserMatrix.
    No new data is produced.
    To do this, set USER_MATRIX = False
"""
USER_MATRIX = True


def main():
    colors = vtkNamedColors()

    # Set the background color.
    colors.SetColor('BkgColor', [26, 51, 77, 255])

    # Create a cylinder.
    # Cylinder height vector is (0,1,0).
    # Cylinder center is in the middle of the cylinder
    cylinderSource = vtkCylinderSource()
    cylinderSource.SetResolution(15)

    # Generate a random start and end point
    startPoint = [0] * 3
    endPoint = [0] * 3
    rng = vtkMinimalStandardRandomSequence()
    rng.SetSeed(8775070)  # For testing.
    for i in range(0, 3):
        rng.Next()
        startPoint[i] = rng.GetRangeValue(-10, 10)
        rng.Next()
        endPoint[i] = rng.GetRangeValue(-10, 10)

    # Compute a basis
    normalizedX = [0] * 3
    normalizedY = [0] * 3
    normalizedZ = [0] * 3

    # The X axis is a vector from start to end
    vtkMath.Subtract(endPoint, startPoint, normalizedX)
    length = vtkMath.Norm(normalizedX)
    vtkMath.Normalize(normalizedX)

    # The Z axis is an arbitrary vector cross X
    arbitrary = [0] * 3
    for i in range(0, 3):
        rng.Next()
        arbitrary[i] = rng.GetRangeValue(-10, 10)
    vtkMath.Cross(normalizedX, arbitrary, normalizedZ)
    vtkMath.Normalize(normalizedZ)

    # The Y axis is Z cross X
    vtkMath.Cross(normalizedZ, normalizedX, normalizedY)
    matrix = vtkMatrix4x4()

    # Create the direction cosine matrix
    matrix.Identity()
    for i in range(0, 3):
        matrix.SetElement(i, 0, normalizedX[i])
        matrix.SetElement(i, 1, normalizedY[i])
        matrix.SetElement(i, 2, normalizedZ[i])

    # Apply the transforms
    transform = vtkTransform()
    transform.Translate(startPoint)  # translate to starting point
    transform.Concatenate(matrix)  # apply direction cosines
    transform.RotateZ(-90.0)  # align cylinder to x axis
    transform.Scale(1.0, length, 1.0)  # scale along the height vector
    transform.Translate(0, .5, 0)  # translate to start of cylinder

    # Transform the polydata
    transformPD = vtkTransformPolyDataFilter()
    transformPD.SetTransform(transform)
    transformPD.SetInputConnection(cylinderSource.GetOutputPort())

    # Create a mapper and actor for the arrow
    mapper = vtkPolyDataMapper()
    actor = vtkActor()
    if USER_MATRIX:
        mapper.SetInputConnection(cylinderSource.GetOutputPort())
        actor.SetUserMatrix(transform.GetMatrix())
    else:
        mapper.SetInputConnection(transformPD.GetOutputPort())
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Cyan'))

    # Create spheres for start and end point
    sphereStartSource = vtkSphereSource()
    sphereStartSource.SetCenter(startPoint)
    sphereStartSource.SetRadius(0.8)
    sphereStartMapper = vtkPolyDataMapper()
    sphereStartMapper.SetInputConnection(sphereStartSource.GetOutputPort())
    sphereStart = vtkActor()
    sphereStart.SetMapper(sphereStartMapper)
    sphereStart.GetProperty().SetColor(colors.GetColor3d('Yellow'))

    sphereEndSource = vtkSphereSource()
    sphereEndSource.SetCenter(endPoint)
    sphereEndSource.SetRadius(0.8)
    sphereEndMapper = vtkPolyDataMapper()
    sphereEndMapper.SetInputConnection(sphereEndSource.GetOutputPort())
    sphereEnd = vtkActor()
    sphereEnd.SetMapper(sphereEndMapper)
    sphereEnd.GetProperty().SetColor(colors.GetColor3d('Magenta'))

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName('Oriented Cylinder')
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(actor)
    renderer.AddActor(sphereStart)
    renderer.AddActor(sphereEnd)
    renderer.SetBackground(colors.GetColor3d('BkgColor'))

    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
