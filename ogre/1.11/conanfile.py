from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class OGREConan(ConanFile):
    name = "ogre3d"
    license = "MIT"
    url = "https://github.com/AnotherFoxGuy/conan-OGRE"
    description = "scene-oriented, flexible 3D engine written in C++"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"
    exports_sources = "patches/**"
    options = {
        # Enable Ogre asserts and exceptions. Possible values:
        # 	0 - Standard asserts in debug builds, nothing in release builds.
        # 	1 - Standard asserts in debug builds, exceptions in release builds.
        # 	2 - Exceptions in debug builds, exceptions in release builds.
        "assert_mode": [0, 1, 2],

        # Build OgreBites component
        "component_bites": [True, False],

        # Build HLMS component
        "component_hlms": [True, False],

        # Build MeshLodGenerator component
        "component_meshlodgenerator": [True, False],

        # Build Overlay component
        "component_overlay": [True, False],

        # Build Paging component
        "component_paging": [True, False],

        # Build Property component
        "component_property": [True, False],

        # Build RTShader System component
        "component_rtshadersystem": [True, False],

        # Build Terrain component
        "component_terrain": [True, False],

        # Build Volume component
        "component_volume": [True, False],

        # Build BSP SceneManager plugin
        "plugin_bsp": [True, False],

        # Build Octree SceneManager plugin
        "plugin_octree": [True, False],

        # Build PCZ SceneManager plugin
        "plugin_pcz": [True, False],

        # Build ParticleFX plugin
        "plugin_pfx": [True, False],

        # Enable STBI image codec.
        "plugin_stbi": [True, False],

        # Build RTShader System FFP core shaders
        "rtshadersystem_core_shaders": [True, False],

        # Build RTShader System extensions shaders
        "rtshadersystem_ext_shaders": [True, False],

        # Use doubles instead of floats in Ogre
        "double": [True, False],

        # Build ASTC codec.
        "enable_astc": [True, False],

        # Build DDS codec.
        "enable_dds": [True, False],

        # Build ETC codec.
        "enable_etc": [True, False],

        # Enable Mesh Lod.
        "enable_meshlod": [True, False],

        # Build PVRTC codec.
        "enable_pvrtc": [True, False],

        # Enable stereoscopic 3D support
        "enable_quad_buffer_stereo": [True, False],

        # Enable TBB's scheduler initialisation/shutdown.
        "enable_tbb_scheduler": [True, False],

        # Include Viewport orientation mode support.
        "enable_viewport_orientationmode": [True, False],

        # Tells the node whether it should inherit full transform from
        #  it's parent node or derived position, orientation and scale
        "node_inherit_transform": [True, False],

        # Enable Ogre thread safety support for multithreading. Possible
        #  values:
        # 	0 - no thread safety. DefaultWorkQueue is not threaded.
        # 	1 - background resource preparation and loading is thread safe. Threaded DefaultWorkQueue. [DEPRECATED]
        # 	2 - only background resource preparation is thread safe. Threaded DefaultWorkQueue. [DEPRECATED]
        # 	3 - no thread safety. Threaded DefaultWorkQueue.
        "threads": [0, 1, 2, 3],

        # Make ResourceManager strict for faster operation. Possible values:
        #   0 - OFF search in all groups twice - for case sensitive and insensitive lookup [DEPRECATED]
        #   1 - PEDANTIC require an explicit resource group. Case sensitive lookup.
        #   2 - STRICT search in default group if not specified otherwise. Case sensitive lookup.
        #
        "resourcemanager_strict": [0, 1, 2],

        # Static build
        "shared": [True, False],
    }
    default_options  = {
        # Enable Ogre asserts and exceptions. Possible values:
        # 	0 - Standard asserts in debug builds, nothing in release builds.
        # 	1 - Standard asserts in debug builds, exceptions in release builds.
        # 	2 - Exceptions in debug builds, exceptions in release builds.
        "assert_mode": 1,

        # Build OgreBites component
        "component_bites": [True, False],

        # Build HLMS component
        "component_hlms": [True, False],

        # Build MeshLodGenerator component
        "component_meshlodgenerator": [True, False],

        # Build Overlay component
        "component_overlay": [True, False],

        # Build Paging component
        "component_paging": [True, False],

        # Build Property component
        "component_property": [True, False],

        # Build RTShader System component
        "component_rtshadersystem": [True, False],

        # Build Terrain component
        "component_terrain": [True, False],

        # Build Volume component
        "component_volume": [True, False],

        # Build BSP SceneManager plugin
        "plugin_bsp": [True, False],

        # Build Octree SceneManager plugin
        "plugin_octree": [True, False],

        # Build PCZ SceneManager plugin
        "plugin_pcz": [True, False],

        # Build ParticleFX plugin
        "plugin_pfx": [True, False],

        # Enable STBI image codec.
        "plugin_stbi": [True, False],

        # Build RTShader System FFP core shaders
        "rtshadersystem_core_shaders": [True, False],

        # Build RTShader System extensions shaders
        "rtshadersystem_ext_shaders": [True, False],

        # Use doubles instead of floats in Ogre
        "double": [True, False],

        # Build ASTC codec.
        "enable_astc": [True, False],

        # Build DDS codec.
        "enable_dds": [True, False],

        # Build ETC codec.
        "enable_etc": [True, False],

        # Enable Mesh Lod.
        "enable_meshlod": [True, False],

        # Build PVRTC codec.
        "enable_pvrtc": [True, False],

        # Enable stereoscopic 3D support
        "enable_quad_buffer_stereo": [True, False],

        # Enable TBB's scheduler initialisation/shutdown.
        "enable_tbb_scheduler": [True, False],

        # Include Viewport orientation mode support.
        "enable_viewport_orientationmode": [True, False],

        # Tells the node whether it should inherit full transform from
        #  it's parent node or derived position, orientation and scale
        "node_inherit_transform": [True, False],

        # Enable Ogre thread safety support for multithreading. Possible
        #  values:
        # 	0 - no thread safety. DefaultWorkQueue is not threaded.
        # 	1 - background resource preparation and loading is thread safe. Threaded DefaultWorkQueue. [DEPRECATED]
        # 	2 - only background resource preparation is thread safe. Threaded DefaultWorkQueue. [DEPRECATED]
        # 	3 - no thread safety. Threaded DefaultWorkQueue.
        "threads": [0, 1, 2, 3],

        # Make ResourceManager strict for faster operation. Possible values:
        #   0 - OFF search in all groups twice - for case sensitive and insensitive lookup [DEPRECATED]
        #   1 - PEDANTIC require an explicit resource group. Case sensitive lookup.
        #   2 - STRICT search in default group if not specified otherwise. Case sensitive lookup.
        #
        "resourcemanager_strict": [0, 1, 2],

        # Static build
        "shared": [True, False],
    }

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
        cmake.definitions["OGRE_BUILD_SAMPLES"] = "OFF"
        cmake.definitions["OGRE_BUILD_TESTS"] = "OFF"
        cmake.definitions["OGRE_INSTALL_DOCS"] = "OFF"
        cmake.definitions["OGRE_INSTALL_SAMPLES"] = "OFF"
        cmake.definitions["OGRE_INSTALL_SAMPLES_SOURCE"] = "OFF"
        cmake.definitions["OGRE_INSTALL_CMAKE"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_CSHARP"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_JAVA"] = "OFF"
        cmake.definitions["OGRE_BUILD_COMPONENT_PYTHON"] = "OFF"

        cmake.definitions["OGRE_STATIC"] = not self.options.shared
        cmake.definitions["OGRE_ASSERT_MODE"] = self.options.assert_mode
        cmake.definitions["OGRE_BUILD_COMPONENT_BITES"] = self.options.component_bites
        cmake.definitions["OGRE_BUILD_COMPONENT_HLMS"] = self.options.component_hlms
        cmake.definitions["OGRE_BUILD_COMPONENT_MESHLODGENERATOR"] = self.options.component_meshlodgenerator
        cmake.definitions["OGRE_BUILD_COMPONENT_OVERLAY"] = self.options.component_overlay
        cmake.definitions["OGRE_BUILD_COMPONENT_PAGING"] = self.options.component_paging
        cmake.definitions["OGRE_BUILD_COMPONENT_PROPERTY"] = self.options.component_property
        cmake.definitions["OGRE_BUILD_COMPONENT_RTSHADERSYSTEM"] = self.options.component_rtshadersystem
        cmake.definitions["OGRE_BUILD_COMPONENT_TERRAIN"] = self.options.component_terrain
        cmake.definitions["OGRE_BUILD_COMPONENT_VOLUME"] = self.options.component_volume

        cmake.definitions["OGRE_BUILD_PLUGIN_BSP"] = self.options.plugin_bsp
        cmake.definitions["OGRE_BUILD_PLUGIN_OCTREE"] = self.options.plugin_octree
        cmake.definitions["OGRE_BUILD_PLUGIN_PCZ"] = self.options.plugin_pcz
        cmake.definitions["OGRE_BUILD_PLUGIN_PFX"] = self.options.plugin_pfx
        cmake.definitions["OGRE_BUILD_PLUGIN_STBI"] = self.options.plugin_stbi

        cmake.definitions["OGRE_BUILD_RTSHADERSYSTEM_CORE_SHADERS"] = self.options.rtshadersystem_core_shaders
        cmake.definitions["OGRE_BUILD_RTSHADERSYSTEM_EXT_SHADERS"] = self.options.rtshadersystem_ext_shaders

        cmake.definitions["OGRE_CONFIG_DOUBLE"] = self.options.double

        cmake.definitions["OGRE_CONFIG_ENABLE_ASTC"] = self.options.enable_astc
        cmake.definitions["OGRE_CONFIG_ENABLE_DDS"] = self.options.enable_dds
        cmake.definitions["OGRE_CONFIG_ENABLE_ETC"] = self.options.enable_etc
        cmake.definitions["OGRE_CONFIG_ENABLE_MESHLOD"] = self.options.enable_meshlod
        cmake.definitions["OGRE_CONFIG_ENABLE_PVRTC"] = self.options.enable_pvrtc
        cmake.definitions["OGRE_CONFIG_ENABLE_SEM"] = self.options.enable_sem
        cmake.definitions["OGRE_CONFIG_ENABLE_QUAD_BUFFER_STEREO"] = self.options.enable_quad_buffer_stereo
        cmake.definitions["OGRE_CONFIG_ENABLE_TBB_SCHEDULER"] = self.options.enable_tbb_scheduler
        cmake.definitions["OGRE_CONFIG_ENABLE_VIEWPORT_ORIENTATIONMODE"] = self.options.enable_viewport_orientationmode
        cmake.definitions["OGRE_CONFIG_NODE_INHERIT_TRANSFORM"] = self.options.node_inherit_transform

        cmake.definitions["OGRE_CONFIG_THREADS"] = self.options.threads
        cmake.definitions["OGRE_RESOURCEMANAGER_STRICT"] = self.options.resourcemanager_strict

        if os_info.is_windows:
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-D_OGRE_FILESYSTEM_ARCHIVE_UNICODE"
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.name = "OGRE"
        self.cpp_info.components["OgreMain"].names["cmake"] = "OgreMain"
        self.cpp_info.components["OgreMain"].includedirs = [
            "include/OGRE/OGRE"]
        self.cpp_info.components["OgreMain"].libs = ["OgreMain"]

        #self.cpp_info.libs = tools.collect_libs(self)
