from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class MyGUIConan(ConanFile):
    name = "mygui"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-MyGUI"
    description = "Fast, flexible and simple GUI."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths", "cmake_find_package"
    exports_sources = "patches/**"
    options = {"system_ogre": [True, False]}
    default_options = {"system_ogre": False}

    def requirements(self):
        if not self.options.system_ogre:
            for req in self.conan_data["requirements"]:
                self.requires(req)

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)
        if not self.options.system_ogre:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['MYGUI_BUILD_DEMOS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_DOCS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TEST_APP'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_PLUGINS'] = 'OFF'
        cmake.definitions['MYGUI_BUILD_TOOLS'] = 'OFF'
        cmake.definitions['MYGUI_RENDERSYSTEM'] = '3'
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include/MYGUI']
        # Directories where libraries can be found
        self.cpp_info.libdirs = ['lib', f'lib/{self.settings.build_type}']
        self.cpp_info.libs = tools.collect_libs(self)

    def package_id(self):
        if not self.options.system_ogre:
            self.info.requires["ogre3d"].full_recipe_mode()
