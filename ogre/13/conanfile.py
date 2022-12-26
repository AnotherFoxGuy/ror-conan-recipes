from conan import ConanFile
from conan.tools.files import get, collect_libs, rmdir, replace_in_file, apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.system.package_manager import Apt
import os

class OGREConan(ConanFile):
    name = "ogre3d"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "resourcemanager_strict": ["off", "pedantic", "strict"],
        "nodeless_positioning": [True, False],
    }

    default_options = {
        "resourcemanager_strict": "strict",
        "nodeless_positioning": False,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("zlib/[1.x]")
        self.requires("zziplib/[0.13.x]")
        self.requires("freetype/[2.x]")
        self.requires("freeimage/[3.x]")
        self.requires("cg-toolkit/3.1@anotherfoxguy/stable")
        self.requires("pugixml/[1.x]")
        self.requires("libpng/1.6.38")
        self.requires("sdl/[2.x]")
        if self.settings.os == "Windows":
            self.requires("directx-sdk/9.0@anotherfoxguy/stable")

    def system_requirements(self):
        Apt(self).install([
                "libx11-dev",
                "libxaw7-dev",
                "libxrandr-dev",
                "libgles2-mesa-dev",
                "libvulkan-dev",
                "glslang-dev"
        ], check=True)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["OGRE_BUILD_COMPONENT_BITES"] = "ON"
        tc.variables["OGRE_BUILD_COMPONENT_CSHARP"] = "OFF"
        tc.variables["OGRE_BUILD_COMPONENT_JAVA"] = "OFF"
        tc.variables["OGRE_BUILD_COMPONENT_OVERLAY_IMGUI"] = "ON"
        tc.variables["OGRE_BUILD_COMPONENT_PYTHON"] = "OFF"
        tc.variables["OGRE_BUILD_COMPONENT_BULLET"] = "OFF"
        tc.variables["OGRE_BUILD_DEPENDENCIES"] = "OFF"
        tc.variables["OGRE_BUILD_PLUGIN_DOT_SCENE"] = "OFF"
        tc.variables["OGRE_BUILD_PLUGIN_STBI"] = "ON"
        tc.variables["OGRE_BUILD_PLUGIN_EXRCODEC"] = "OFF"
        tc.variables["OGRE_BUILD_RENDERSYSTEM_D3D11"] = "ON"
        tc.variables["OGRE_BUILD_RENDERSYSTEM_D3D9"] = "ON"
        tc.variables["OGRE_BUILD_RENDERSYSTEM_GL3PLUS"] = "OFF"
        tc.variables["OGRE_BUILD_SAMPLES"] = "OFF"
        tc.variables["OGRE_COPY_DEPENDENCIES"] = "OFF"
        tc.variables["OGRE_INSTALL_DEPENDENCIES"] = "OFF"
        tc.variables["OGRE_INSTALL_SAMPLES"] = "OFF"
        tc.variables["OGRE_NODELESS_POSITIONING"] = self.options.nodeless_positioning

        if self.options.resourcemanager_strict == "off":
            tc.variables["OGRE_RESOURCEMANAGER_STRICT"] = 0
        elif self.options.resourcemanager_strict == "pedantic":
            tc.variables["OGRE_RESOURCEMANAGER_STRICT"] = 1
        else:
            tc.variables["OGRE_RESOURCEMANAGER_STRICT"] = 2

        if self.settings.os == "Windows":
            tc.variables["CMAKE_CXX_FLAGS"] = "-D_OGRE_FILESYSTEM_ARCHIVE_UNICODE"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)
        replace_in_file(self,
            os.path.join(self.source_folder, "CMake/Dependencies.cmake"),
            "find_package(DirectX)",
            "find_package(DirectX9)",
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "PlugIns/FreeImageCodec/CMakeLists.txt"),
            "${FreeImage_LIBRARIES}",
            "freeimage::FreeImage",
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "Components/Overlay/CMakeLists.txt"),
            "${FREETYPE_LIBRARIES}",
            "freetype",
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "CMake/Packages/FindDirectX11.cmake"),
            'find_path(DirectX11_INCLUDE_DIR NAMES d3d11.h HINTS "',
            'find_path(DirectX11_INCLUDE_DIR NO_CMAKE_PATH NO_CMAKE_ENVIRONMENT_PATH NAMES d3d11.h HINTS "',
        )

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "CMake"))
        rmdir(self, os.path.join(self.package_folder, "Docs"))

    def package_info(self):
        self.cpp_info.set_property("cmake_module_file_name", "OGRE")
        self.cpp_info.set_property("cmake_module_target_name", "OGRE::OGRE")
        self.cpp_info.set_property("cmake_file_name", "OGRE")
        self.cpp_info.set_property("cmake_target_name", "OGRE::OGRE")
        self.cpp_info.includedirs = [
            "include",
            "include/OGRE",
            "include/OGRE/Bites",
            "include/OGRE/MeshLodGenerator",
            "include/OGRE/Overlay",
            "include/OGRE/Paging",
            "include/OGRE/Plugins",
            "include/OGRE/Property",
            "include/OGRE/RenderSystems",
            "include/OGRE/RTShaderSystem",
            "include/OGRE/Terrain",
            "include/OGRE/Threading",
            "include/OGRE/Volume",
        ]
        self.cpp_info.libs = collect_libs(self)
