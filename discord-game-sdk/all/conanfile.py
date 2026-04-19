from conan import ConanFile
from conan.tools.files import get, collect_libs, replace_in_file
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
import os


class DiscordGameSDKConan(ConanFile):
    name = "discord-game-sdk"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _cmake = None

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def source(self):
        get(**self.conan_data["sources"][self.version], destination="src")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        if self.settings.os == "Windows":
            if self.settings.arch.__contains__('64'):
                copy("*.lib", src="src/lib/x86_64", dst="lib", keep_path=False)
                copy("*.dll", src="src/lib/x86_64", dst="bin", keep_path=False)
            else:
                copy("*.lib", src="src/lib/x86", dst="lib", keep_path=False)
                copy("*.dll", src="src/lib/x86", dst="bin", keep_path=False)
        elif self.settings.os == "MacOS":
            copy("*.bundle", src="src/lib/x86_64", dst="lib", keep_path=False)
            copy("*.dylib", src="src/lib/x86_64", dst="bin", keep_path=False)
            copy("*.so", src="src/lib/x86_64", dst="lib", keep_path=False)
        else:
            copy("*.so", src="src/lib/x86_64", dst="lib", keep_path=False)

    def package_info(self): 
        self.cpp_info.name = "DiscordGameSDK"
        self.cpp_info.libs = collect_libs(self)
