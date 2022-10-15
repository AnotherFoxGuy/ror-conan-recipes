from conans import ConanFile, CMake, tools


class RemoteryConan(ConanFile):
    name = "remotery"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/Celtoys/Remotery"
    description = "Single C file, Realtime CPU/GPU Profiler with Remote Web Viewer"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

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
        self.cpp_info.libs = tools.collect_libs(self)
