from conan import ConanFile
from conan.tools.files import (
    get,
    collect_libs,
    apply_conandata_patches,
    export_conandata_patches,
)
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
import os


class CaelumConan(ConanFile):
    name = "ogre3d-caelum"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/RigsOfRods/Caelum/issues"
    description = "Library for rendering of dynamic and realistic skies"
    settings = "os", "compiler", "build_type", "arch"

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("ogre3d/[~14]@anotherfoxguy/stable")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_DEBUG_POSTFIX"] = "d"
        tc.cache_variables["CMAKE_POLICY_VERSION_MINIMUM"] = "3.5"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_module_file_name", "Caelum")
        self.cpp_info.set_property("cmake_module_target_name", "Caelum::Caelum")
        self.cpp_info.set_property("cmake_file_name", "Caelum")
        self.cpp_info.set_property("cmake_target_name", "Caelum::Caelum")
        self.cpp_info.includedirs = ["include", "include/Caelum"]
        self.cpp_info.libs = collect_libs(self)

    def package_id(self):
        self.info.requires["ogre3d"].full_recipe_mode()
