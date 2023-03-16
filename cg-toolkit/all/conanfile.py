from conan import ConanFile
from conan.tools.files import get, collect_libs, copy
import os

class GcConan(ConanFile):
    name = "cg-toolkit"
    version = "3.1"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder,"include"))
        if self.settings.os == "Windows":
            if '64' in self.settings.arch:
                #copy(self, "*.h", self.source_folder, os.path.join(self.package_folder, "include"))
                copy(self, "*.lib", os.path.join(self.source_folder, "lib64"), os.path.join(self.package_folder,"lib"))
                copy(self, "*.dll", os.path.join(self.source_folder, "bin64"), os.path.join(self.package_folder,"bin"))
            else:
                copy(self, "*.lib", os.path.join(self.source_folder, "lib"), os.path.join(self.package_folder,"lib"))
                copy(self, "*.dll", os.path.join(self.source_folder, "bin"), os.path.join(self.package_folder,"bin"))
        else:
            if '64' in self.settings.arch:
                copy(self, "*.so", os.path.join(self.source_folder, "lib64"), os.path.join(self.package_folder,"lib"))
            else:
                copy(self, "*.so", os.path.join(self.source_folder, "lib"), os.path.join(self.package_folder,"lib"))
    def package_info(self):
        self.cpp_info.set_property("cmake_module_file_name", "Cg")
        self.cpp_info.set_property("cmake_module_target_name", "Cg::Cg")
        self.cpp_info.set_property("cmake_file_name", "Cg")
        self.cpp_info.set_property("cmake_target_name", "Cg::Cg")
        self.cpp_info.libs = collect_libs(self)
