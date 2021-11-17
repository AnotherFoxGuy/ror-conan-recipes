from conans import ConanFile, MSBuild, tools, AutoToolsBuildEnvironment
from conans.tools import os_info
import glob


class freeimageConan(ConanFile):
    name = "freeimage"
    license = "GNU"
    author = "Edgar (Edgar@AnotherFoxGuy.com)"
    url = "https://github.com/AnotherFoxGuy/conan-freeimage"
    description = "FreeImage is an Open Source library project for developers who would like to support popular graphics image formats like PNG, BMP, JPEG, TIFF and others as needed by today's multimedia applications."
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "patches/**"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        if os_info.is_windows:
            for file in glob.glob("./**/*2017.vcxproj", recursive=True):
                print(f"Patching winsdk in file {file}")
                tools.replace_in_file(file, "10.0.16299.0", "10.0", strict=False)
            msbuild = MSBuild(self)
            msbuild.build("FreeImage.2017.sln")
        else:
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make()

    def package(self):
        self.copy("*.h", dst="include", src="Dist", keep_path=False)
        self.copy("*.lib", dst="lib", src="Dist", keep_path=False)
        self.copy("*.dll", dst="bin", src="Dist", keep_path=False)
        self.copy("*.so", dst="lib", src="Dist", keep_path=False)
        self.copy("*.a", dst="lib", src="Dist", keep_path=False)
        self.copy("*.lib", dst="lib", src="Source", keep_path=False)
        self.copy("*.dll", dst="bin", src="Source", keep_path=False)
        self.copy("*.so", dst="lib", src="Source", keep_path=False)
        self.copy("*.a", dst="lib", src="Source", keep_path=False)

    def package_info(self):
        self.cpp_info.name = "FreeImage"
        self.cpp_info.libs = tools.collect_libs(self)
