include(Findzziplib)

set(ZZip_FOUND "${zziplib_FOUND}" CACHE BOOL "Conan patch for zziplib" FORCE)
set(ZZip_LIBRARIES "${zziplib_LIBRARIES}" CACHE STRING "Conan patch for zziplib" FORCE)
set(ZZip_INCLUDE_DIRS "${zziplib_INCLUDE_DIRS}" CACHE STRING "Conan patch for zziplib" FORCE)