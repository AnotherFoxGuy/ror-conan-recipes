from conan import ConanFile
from conan.tools.files import get, collect_libs, replace_in_file
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
import os


class DiscordrpcConan(ConanFile):
    name = "discord-rpc"
    license = "MIT"
    author = "Edgar (Edgar@AnotherFoxGuy.com)"
    url = "https://github.com/AnotherFoxGuy/conan-discord-rpc"
    description = "This is a library for interfacing your game with a locally running Discord desktop client. It's known to work on Windows, macOS, and Linux."
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.requires("rapidjson/cci.20230929")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_EXAMPLES"] = "OFF"
        tc.generate()

    def _patch_sources(self):
        replace_in_file(
            self,
            os.path.join(self.source_folder, "CMakeLists.txt"),
            "find_file(RAPIDJSON NAMES rapidjson rapidjson-1.1.0 PATHS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty CMAKE_FIND_ROOT_PATH_BOTH)",
            "find_path(RapidJSON_INCLUDE_DIRS NAMES rapidjson/rapidjson.h PATHS ${RAPIDJSON_INCLUDEDIR})",
        )
        replace_in_file(
            self,
            os.path.join(self.source_folder, "src", "CMakeLists.txt"),
            "${RAPIDJSON}/include",
            "${RapidJSON_INCLUDE_DIRS}",
        )
        replace_in_file(
            self,
            os.path.join(self.source_folder, "CMakeLists.txt"),
            "add_library(rapidjson STATIC IMPORTED ${RAPIDJSON})",
            'message("Found rapidjson at ${RapidJSON_INCLUDE_DIRS}")',
        )
        replace_in_file(
            self,
            os.path.join(self.source_folder, "CMakeLists.txt"),
            "find_program(CLANG_FORMAT_CMD",
            "# find_program(CLANG_FORMAT_CMD",
        )

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)

    def package_id(self):
        self.info.requires["rapidjson"].full_recipe_mode()
