from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class OGREConan(ConanFile):
    name = "ogre3d"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"
    exports_sources = "patches/**"

    def requirements(self):
        for req in self.conan_data["requirements"]:
            self.requires(req)

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                installer.install("libx11-dev")
                installer.install("libxaw7-dev")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["OGRE_BUILD_DEPENDENCIES"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_OVERLAY_IMGUI"] = "ON"
        cmake.definitions["OGRE_BUILD_COMPONENT_CSHARP"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_JAVA"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_PYTHON"] = "OFF"
        cmake.definitions["OGRE_BUILD_PLUGIN_STBI"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_BITES"] = "ON"
        cmake.definitions["OGRE_BUILD_SAMPLES"] = "OFF"
        cmake.definitions["OGRE_BUILD_RENDERSYSTEM_D3D9"] = "ON"
        cmake.definitions["OGRE_BUILD_RENDERSYSTEM_D3D11"] = "ON"
        cmake.definitions["OGRE_BUILD_RENDERSYSTEM_GL3PLUS"] = "OFF"
        cmake.definitions["OGRE_RESOURCEMANAGER_STRICT"] = 0
        cmake.definitions["OGRE_INSTALL_SAMPLES"] = "OFF"
        cmake.definitions["OGRE_BUILD_PLUGIN_DOT_SCENE"] = "OFF"
        if os_info.is_windows:
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-D_OGRE_FILESYSTEM_ARCHIVE_UNICODE"
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.name = "OGRE"
        self.cpp_info.includedirs = [
            "include",
            "include/OGRE",
            "include/OGRE/Bites",
            "include/OGRE/HLMS",
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
        self.cpp_info.libs = tools.collect_libs(self)
