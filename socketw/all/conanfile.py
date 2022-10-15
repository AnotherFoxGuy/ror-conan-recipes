from conan import ConanFile
from conan.tools.files import get, collect_libs
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout

class SocketwConan(ConanFile):
    name = "socketw"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/RigsOfRods/socketw/issues"
    description = "SocketW is a library which provides cross-platform socket abstraction"
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        for req in self.conan_data["requirements"]:
            self.requires(req)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
