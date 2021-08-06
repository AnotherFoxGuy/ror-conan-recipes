from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class OisConan(ConanFile):
    name = "ois"
    license = "zlib"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    url = "https://github.com/AnotherFoxGuy/conan-OIS/"
    description = "Object oriented Input System"
    topics = ("Input", "System")
    settings = "os", "compiler", "build_type", "arch"

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                installer.install("libx11-dev")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['OIS_BUILD_DEMOS'] = 'OFF'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include', 'include/ois']
        self.cpp_info.libs = tools.collect_libs(self)
