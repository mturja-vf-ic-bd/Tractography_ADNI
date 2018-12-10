cmake_minimum_required(VERSION 3.0)
 
PROJECT(EditParcellationTable)
 
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
 
add_executable(EditParcellationTable MACOSX_BUNDLE updateParcellationTable.cxx)
 
if(VTK_LIBRARIES)
  target_link_libraries(EditParcellationTable ${VTK_LIBRARIES})
else()
  target_link_libraries(EditParcellationTable vtkHybrid vtkWidgets)
endif()
