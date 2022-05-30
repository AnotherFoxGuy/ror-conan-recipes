cmake_minimum_required(VERSION 3.1.2)
project(discord_game_sdk)

include(conanbuildinfo.cmake)
conan_basic_setup()

if(NOT "${CMAKE_CXX_STANDARD}")
    set(CMAKE_CXX_STANDARD 11)
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB_RECURSE src_files CONFIGURE_DEPENDS "src/cpp/*.cpp" "src/cpp/*.h")

add_library(${PROJECT_NAME} ${src_files})

target_include_directories(${PROJECT_NAME} PRIVATE "src/cpp/")

include(GNUInstallDirs)

install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(DIRECTORY src/cpp/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h"
)