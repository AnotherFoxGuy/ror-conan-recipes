from conans import ConanFile, CMake, tools


class CrowdConan(ConanFile):
    name = "ogre3d-crowd"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/OGRECave/OgreCrowd/issues"
    description = "Pathfinding for Ogre using Recast/Detour"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_multi"

    def requirements(self):
        for req in self.conan_data["requirements"]:
            self.requires(req)

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.name = "OgreCrowd"
        self.cpp_info.libs = tools.collect_libs(self)

    def package_id(self):
        self.info.requires["ogre3d"].full_recipe_mode()
