from conans import ConanFile, CMake, tools


class AngelscriptConan(ConanFile):
    name = "angelscript"
    license = "zlib"
    url = "https://github.com/AnotherFoxGuy/angelscript/issues"
    description = " AngelScript is an extremely flexible cross-platform scripting library designed to allow applications to extend their functionality through external scripts."
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "patches/**"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="angelscript/projects/cmake")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
