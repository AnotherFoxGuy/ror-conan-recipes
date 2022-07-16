include(Findfreeimage)

set(FreeImage_FOUND "${freeimage_FOUND}" CACHE BOOL "Conan patch for freeimage" FORCE)
set(FreeImage_LIBRARIES "${freeimage_LIBRARIES}" CACHE STRING "Conan patch for freeimage" FORCE)
set(FreeImage_INCLUDE_DIR "${freeimage_INCLUDE_DIR}" CACHE STRING "Conan patch for freeimage" FORCE)