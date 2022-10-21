from conan import ConanFile
from conan.tools.files import get, collect_libs
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class DiscordrpcConan(ConanFile):
    name = "discord-rpc"
    license = "MIT"
    author = "Edgar (Edgar@AnotherFoxGuy.com)"
    url = "https://github.com/AnotherFoxGuy/conan-discord-rpc"
    description = "This is a library for interfacing your game with a locally running Discord desktop client. It's known to work on Windows, macOS, and Linux."
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_EXAMPLES"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
