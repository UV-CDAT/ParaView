vtk_module(vtkSciberQuest
  DEPENDS
    vtkFiltersFlowPaths
    vtkIOLegacy
    vtkPVCommon
    vtkParallelCore
    vtkPVVTKExtensionsCore
    vtksys
  COMPILE_DEPENDS
    vtkFiltersFlowPaths
    vtkFiltersParallel
    vtkIOLegacy
    vtkPVCommon
    vtkPVServerManagerApplication
    vtkParallelCore
    vtkRenderingOpenGL
    vtksys
  TEST_LABELS
    PARAVIEW
)
