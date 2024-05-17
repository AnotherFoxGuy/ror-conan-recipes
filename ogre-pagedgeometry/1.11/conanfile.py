from conan import ConanFile
from conan.tools.files import get, collect_libs
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout


class PagedGeometryConan(ConanFile):
    name = "ogre3d-pagedgeometry"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/RigsOfRods/Caelum/issues"
    description = "PagedGeometry is a plugin for OGRE for rendering of dense vegetation "
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("ogre3d/[~1.11]@anotherfoxguy/stable")

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
        self.cpp_info.set_property("cmake_module_file_name", "PagedGeometry")
        self.cpp_info.set_property("cmake_module_target_name", "PagedGeometry::PagedGeometry")
        self.cpp_info.set_property("cmake_file_name", "PagedGeometry")
        self.cpp_info.set_property("cmake_target_name", "PagedGeometry::PagedGeometry")
        self.cpp_info.includedirs = [
            'include',
            'include/PagedGeometry'
        ]
        self.cpp_info.libs = collect_libs(self)

    def package_id(self):
        self.info.requires["ogre3d"].full_recipe_mode()