from conans import ConanFile, CMake, tools


class PagedGeometryConan(ConanFile):
    name = "ogre3d-pagedgeometry"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/RigsOfRods/Caelum/issues"
    description = "PagedGeometry is a plugin for OGRE for rendering of dense vegetation "
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"
    exports_sources = "patches/**"

    def requirements(self):
        for req in self.conan_data["requirements"][self.version]:
            self.requires(req)

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.name = "PagedGeometry"
        self.cpp_info.includedirs = [
            'include',
            'include/PagedGeometry'
        ]
        self.cpp_info.libs = tools.collect_libs(self)

    def package_id(self):
        self.info.requires["ogre3d"].full_recipe_mode()
