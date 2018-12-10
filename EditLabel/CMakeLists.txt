cmake_minimum_required(VERSION 3.0)
 
PROJECT(EditVtk)
 
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
 
add_executable(EditVtk MACOSX_BUNDLE EditVtk.cxx)
 
if(VTK_LIBRARIES)
  target_link_libraries(EditVtk ${VTK_LIBRARIES})
else()
  target_link_libraries(EditVtk vtkHybrid vtkWidgets)
endif()
