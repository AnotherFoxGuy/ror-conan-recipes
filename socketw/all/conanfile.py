from conans import ConanFile, CMake, tools


class SocketwConan(ConanFile):
    name = "socketw"
    license = "GNU Lesser General Public License v2.1"
    url = "https://github.com/RigsOfRods/socketw/issues"
    description = "SocketW is a library which provides cross-platform socket abstraction"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

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
        self.cpp_info.libs = tools.collect_libs(self)