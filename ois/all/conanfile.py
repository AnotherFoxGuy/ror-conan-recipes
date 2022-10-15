from conan import ConanFile
from conan.tools.files import get, collect_libs
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.system import package_manager


class OisConan(ConanFile):
    name = "ois"
    license = "zlib"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    url = "https://github.com/AnotherFoxGuy/conan-OIS/"
    description = "Object oriented Input System"
    topics = ("Input", "System")
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def system_requirements(self):
        package_manager.Apt(self).install(["libx11-dev"])

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["OIS_BUILD_DEMOS"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include', 'include/ois']
        self.cpp_info.libs = collect_libs(self)
