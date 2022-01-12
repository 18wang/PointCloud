
import vtk
from vtkmodules.vtkCommonDataModel import vtkPointLocator

reverse.Update()
my_cell_locator = vtkPointLocator()
my_cell_locator.SetDataSet(reverse.GetOutput())  # reverse.GetOutput() --> vtkPolyData
my_cell_locator.BuildLocator()

cellId = vtk.reference(0)
c = [0.0, 0.0, 0.0]
subId = vtk.reference(0)
d = vtk.reference(0.0)
my_cell_locator.FindClosestPoint([-23.7, -48.4, -906.4], c, cellId, subId, d)


def ExtractPatchesIds(parentCl,clipPts):
   clipIds = []
   numberOfPoints = 0

   if (clipPts.GetNumberOfPoints() == 2):
      upstreamPoint = clipPts.GetPoint(0)
      downstreamPoint = clipPts.GetPoint(1)

      for j in range(parentCl.GetNumberOfCells()):
         cellLine = ExtractSingleLine(parentCl,j)

         locator = vtkPointLocator()
         locator.SetDataSet(cellLine)
         locator.BuildLocator()

         upstreamId = locator.FindClosestPoint(upstreamPoint)
         downstreamId = locator.FindClosestPoint(downstreamPoint)

         if j==0:
            clipIds.append(upstreamId)
            clipIds.append(downstreamId)
            numberOfPoints += upstreamId+1
            numberOfPoints += cellLine.GetNumberOfPoints()-downstreamId
         else:
            clipIds.append(downstreamId)
            numberOfPoints += cellLine.GetNumberOfPoints()-downstreamId

   if (clipPts.GetNumberOfPoints() == 3):
      commonPoint = clipPts.GetPoint(0)
      dau1Point = clipPts.GetPoint(1)
      dau2Point = clipPts.GetPoint(2)
      for j in range(parentCl.GetNumberOfCells()):
         cellLine = ExtractSingleLine(parentCl,j)

         locator = vtk.vtkPointLocator()
         locator.SetDataSet(cellLine)
         locator.BuildLocator()

         if j==0:
            upstreamId = locator.FindClosestPoint(commonPoint)
            downstreamId = locator.FindClosestPoint(dau1Point)
            clipIds.append(upstreamId)
            clipIds.append(downstreamId)
            numberOfPoints += upstreamId+1
            numberOfPoints += cellLine.GetNumberOfPoints()-downstreamId
         else:
            downstreamId = locator.FindClosestPoint(dau2Point)
            clipIds.append(downstreamId)
            numberOfPoints += cellLine.GetNumberOfPoints()-downstreamId

   return clipIds, numberOfPoints