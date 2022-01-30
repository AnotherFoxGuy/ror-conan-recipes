from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class PthreadWinConan(ConanFile):
    name = "pthread-win"
    license = "zlib"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    url = "https://github.com/GerHobbelt/pthread-win32"
    description = "clone / cvs-import of pthread-win32 + local tweaks (including MSVC2008 - MSVC2019 project files)"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_BUILD_TYPE'] = self.settings.build_type
        cmake.definitions['ENABLE_TESTS'] = 'OFF'
        cmake.definitions['DLLDEST'] = 'bin'
        cmake.definitions['LIBDEST'] = 'lib'
        cmake.definitions['HDRDEST'] = 'include'
        cmake.definitions['TESTDEST'] = 'test'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
