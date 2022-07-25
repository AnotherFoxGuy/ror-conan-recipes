include(FindRapidJSON)

set(Rapidjson_FOUND "${RapidJSON_FOUND}" CACHE BOOL "Conan patch for Rapidjson" FORCE)
set(Rapidjson_LIBRARIES "${RapidJSON_LIBRARIES}" CACHE STRING "Conan patch for Rapidjson" FORCE)
set(Rapidjson_INCLUDE_DIR "${RapidJSON_INCLUDE_DIR}" CACHE STRING "Conan patch for Rapidjson" FORCE)