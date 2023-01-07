from conan import ConanFile
from conan.tools.files import get, collect_libs, rmdir, replace_in_file, apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from conan.tools.system.package_manager import Apt
import os

class OGRENextConan(ConanFile):
    name = "ogre3d-next"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("zlib/[1.x]")
        self.requires("zziplib/[0.13.x]")
        self.requires("freetype/[2.x]")
        self.requires("freeimage/[3.x]")
        self.requires("rapidjson/cci.20220822")
        self.requires("libpng/1.6.38")
        self.requires("sdl/[2.x]")
        self.requires("tinyxml/[2.x]")

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
        tc.variables["OGRE_BUILD_COMPONENT_ATMOSPHERE"] = "ON"
        tc.variables["OGRE_BUILD_COMPONENT_BITES"] = "ON"
        tc.variables["OGRE_BUILD_COMPONENT_CSHARP"] = "OFF"
        tc.variables["OGRE_BUILD_COMPONENT_JAVA"] = "OFF"
        tc.variables["OGRE_BUILD_COMPONENT_OVERLAY_IMGUI"] = "ON"
        tc.variables["OGRE_BUILD_COMPONENT_PYTHON"] = "OFF"
        tc.variables["OGRE_BUILD_COMPONENT_TERRAIN"] = "ON"
        #tc.variables["OGRE_BUILD_COMPONENT_PAGING"] = "ON" # Completly broken
        tc.variables["OGRE_BUILD_DEPENDENCIES"] = "OFF"
        tc.variables["OGRE_BUILD_PLUGIN_DOT_SCENE"] = "OFF"
        tc.variables["OGRE_BUILD_PLUGIN_EXRCODEC"] = "OFF"
        tc.variables["OGRE_BUILD_RENDERSYSTEM_D3D11"] = "ON"
        tc.variables["OGRE_BUILD_RENDERSYSTEM_GL3PLUS"] = "OFF"
        tc.variables["OGRE_BUILD_SAMPLES"] = "OFF"
        tc.variables["OGRE_BUILD_SAMPLES2"] = "OFF"
        tc.variables["OGRE_CONFIG_ENABLE_JSON"] = "ON"
        tc.variables["OGRE_COPY_DEPENDENCIES"] = "OFF"
        tc.variables["OGRE_INSTALL_DEPENDENCIES"] = "OFF"
        tc.variables["OGRE_INSTALL_SAMPLES"] = "OFF"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):  
        apply_conandata_patches(self)
        replace_in_file(self,
            os.path.join(self.source_folder, "CMake/Dependencies.cmake"),
            "find_package(Rapidjson)", 
            """
            find_package(RapidJSON)
            set(Rapidjson_FOUND TRUE)
            """,
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "Components/Overlay/CMakeLists.txt"),
            "${FREETYPE_LIBRARIES}",
            "freetype",
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "CMake/InstallDependencies.cmake"),
            "# Install dependencies",
            "return()",
        )
        replace_in_file(self,
            os.path.join(self.source_folder, "OgreMain/CMakeLists.txt"),
            "target_link_libraries(${OGRE_NEXT}Main ${LIBRARIES})",
            "target_link_libraries(${OGRE_NEXT}Main ${LIBRARIES} rapidjson freeimage::FreeImage)",
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
            "include/OGRE/Animation",
            "include/OGRE/Atmosphere",
            "include/OGRE/CommandBuffer",
            "include/OGRE/Compositor",
            "include/OGRE/Compute",
            "include/OGRE/Hash",
            "include/OGRE/Hlms",
            "include/OGRE/Hlms/Common",
            "include/OGRE/Hlms/Pbs",
            "include/OGRE/Hlms/Unlit",
            "include/OGRE/Math",
            "include/OGRE/MeshLodGenerator",
            "include/OGRE/ogrestd",
            "include/OGRE/Overlay",
            "include/OGRE/Plugins",
            "include/OGRE/RenderSystems",
            "include/OGRE/SceneFormat",
            "include/OGRE/Threading",
            "include/OGRE/Vao",
        ]
        # Directories where libraries can be found
        self.cpp_info.libdirs = ['lib', f'lib/{self.settings.build_type}']
        self.cpp_info.libs = collect_libs(self)
