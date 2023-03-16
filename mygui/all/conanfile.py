from conan import ConanFile
from conan.tools.files import get, collect_libs, replace_in_file
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
import os


class MyGUIConan(ConanFile):
    name = "mygui"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-MyGUI"
    description = "Fast, flexible and simple GUI."
    settings = "os", "compiler", "build_type", "arch"
    options = {"system_ogre": [True, False]}
    default_options = {"system_ogre": False}

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        if not self.options.system_ogre:
            self.requires("ogre3d/[>=1 <14]@anotherfoxguy/stable")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["MYGUI_BUILD_DEMOS"] = "OFF"
        tc.variables["MYGUI_BUILD_DOCS"] = "OFF"
        tc.variables["MYGUI_BUILD_TEST_APP"] = "OFF"
        tc.variables["MYGUI_BUILD_PLUGINS"] = "OFF"
        tc.variables["MYGUI_BUILD_TOOLS"] = "OFF"
        tc.variables["MYGUI_RENDERSYSTEM"] = "3"
        tc.variables["OIS_BUILD_DEMOS"] = "OFF"
        tc.variables["OIS_BUILD_DEMOS"] = "OFF"
        tc.variables["OIS_BUILD_DEMOS"] = "OFF"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        replace_in_file(self,
            os.path.join(self.source_folder, "MyGUIEngine/CMakeLists.txt"),
            "${FREETYPE_LIBRARIES}",
            "freetype",
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "Platforms/Ogre/OgrePlatform/CMakeLists.txt"),
            "${OGRE_LIBRARIES}",
            "OGRE::OGRE",
        )

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_module_file_name", "MyGUI")
        self.cpp_info.set_property("cmake_module_target_name", "MyGUI::MyGUI")
        self.cpp_info.set_property("cmake_file_name", "MyGUI")
        self.cpp_info.set_property("cmake_target_name", "MyGUI::MyGUI")
        self.cpp_info.includedirs = ['include/MYGUI']
        # Directories where libraries can be found
        self.cpp_info.libdirs = ['lib', f'lib/{self.settings.build_type}']
        self.cpp_info.libs = collect_libs(self)

    def package_id(self):
        if not self.options.system_ogre:
            self.info.requires["ogre3d"].full_recipe_mode()
