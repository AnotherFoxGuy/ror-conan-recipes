from conan import ConanFile
from conan.tools.files import get, copy
import os

class DxConan(ConanFile):
    name = "directx-sdk"
    version = "9.0"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"
    exports_sources = "dummy-file-to-fix-cloudsmith"

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def package(self):
        copy(self, "*", os.path.join(self.source_folder, "Include"), os.path.join(self.package_folder, "include"))
        if '64' in self.settings.arch:
            copy(self, "*", os.path.join(self.source_folder, "Lib/x64"), os.path.join(self.package_folder, "lib"), keep_path=False)
        else:
            copy(self, "*", os.path.join(self.source_folder, "lib/x86"), os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "DirectX9")
        self.cpp_info.libs = ["d3d9", "d3dx9", "dxguid"]
