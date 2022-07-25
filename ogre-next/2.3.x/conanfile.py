import shutil
from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class OGREConan(ConanFile):
    name = "ogre3d-next"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_find_package"
    exports_sources = "patches/**"

    options = {
        "resourcemanager_strict": ["off", "pedantic", "strict"],
        "nodeless_positioning": [True, False],
    }

    default_options = {
        "resourcemanager_strict": "strict",
        "nodeless_positioning": False,
    }

    _cmake = None

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)

        self._cmake.definitions["OGRE_BUILD_COMPONENT_BITES"] = "ON"
        self._cmake.definitions["OGRE_BUILD_COMPONENT_CSHARP"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_COMPONENT_JAVA"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_COMPONENT_OVERLAY_IMGUI"] = "ON"
        self._cmake.definitions["OGRE_BUILD_COMPONENT_PYTHON"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_DEPENDENCIES"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_PLUGIN_DOT_SCENE"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_PLUGIN_STBI"] = "ON"
        self._cmake.definitions["OGRE_BUILD_PLUGIN_EXRCODEC"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_RENDERSYSTEM_D3D11"] = "ON"
        self._cmake.definitions["OGRE_BUILD_RENDERSYSTEM_D3D9"] = "ON"
        self._cmake.definitions["OGRE_BUILD_RENDERSYSTEM_GL3PLUS"] = "OFF"
        self._cmake.definitions["OGRE_BUILD_SAMPLES"] = "OFF"
        self._cmake.definitions["OGRE_COPY_DEPENDENCIES"] = "OFF"
        self._cmake.definitions["OGRE_INSTALL_DEPENDENCIES"] = "OFF"
        self._cmake.definitions["OGRE_INSTALL_SAMPLES"] = "OFF"
        self._cmake.definitions[
            "OGRE_NODELESS_POSITIONING"
        ] = self.options.nodeless_positioning

        if self.options.resourcemanager_strict == "off":
            self._cmake.definitions["OGRE_RESOURCEMANAGER_STRICT"] = 0
        elif self.options.resourcemanager_strict == "pedantic":
            self._cmake.definitions["OGRE_RESOURCEMANAGER_STRICT"] = 1
        else:
            self._cmake.definitions["OGRE_RESOURCEMANAGER_STRICT"] = 2

        if os_info.is_windows:
            self._cmake.definitions[
                "CMAKE_CXX_FLAGS"
            ] = "-D_OGRE_FILESYSTEM_ARCHIVE_UNICODE"

        self._cmake.configure()
        return self._cmake

    def requirements(self):
        for req in self.conan_data["requirements"]:
            self.requires(req)

        if os_info.is_windows:
            self.requires("directx-sdk/9.0@anotherfoxguy/stable")

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                installer.install("libx11-dev")
                installer.install("libxaw7-dev")
                installer.install("libxrandr-dev")
                installer.install("libgles2-mesa-dev")
                installer.install("libvulkan-dev")
                installer.install("glslang-dev")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)
        tools.replace_in_file(
            "CMake/Dependencies.cmake",
            "find_package(DirectX)",
            "find_package(DirectX9)",
        )
        tools.replace_in_file(
            "CMake/Dependencies.cmake",
            "find_package(FreeImage)",
            "find_package(ConanFreeImage)",
        )
        tools.replace_in_file(
            "CMake/Dependencies.cmake",
            "find_package(Rapidjson)",
            "find_package(ConanRapidJSON)",
        )
        tools.replace_in_file(
            "CMake/Dependencies.cmake",
            "find_package(ZZip)",
            "find_package(ConanZZip)",
        )
        tools.replace_in_file(
            "CMake/Packages/FindDirectX11.cmake",
            'find_path(DirectX11_INCLUDE_DIR NAMES d3d11.h HINTS "',
            'find_path(DirectX11_INCLUDE_DIR NO_CMAKE_PATH NO_CMAKE_ENVIRONMENT_PATH NAMES d3d11.h HINTS "',
        )
        shutil.copyfile(
            "patches/FindFreeImage.cmake", "CMake/Packages/FindConanFreeImage.cmake"
        )
        shutil.copyfile(
            "patches/FindRapidJSON.cmake", "CMake/Packages/FindConanRapidJSON.cmake"
        )
        shutil.copyfile(
            "patches/FindZZip.cmake", "CMake/Packages/FindConanZZip.cmake"
        )
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
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
