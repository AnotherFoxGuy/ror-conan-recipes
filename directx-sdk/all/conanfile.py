from conans import ConanFile, tools
from conans.tools import os_info


class GcConan(ConanFile):
    name = "directx-sdk"
    version = "9.0"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

    def package(self):
        self.copy("*.h", src="Include", dst="include")
        if self.settings.arch.__contains__("64"):
            self.copy("*.lib", src="Lib/x64", dst="lib", keep_path=False)
        else:
            self.copy("*.lib", src="lib/x86", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.name = "DirectX9"
        self.cpp_info.libs = ["d3d9", "d3dx9", "dxguid"]
