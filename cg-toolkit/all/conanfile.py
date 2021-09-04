from conans import ConanFile, tools
from conans.tools import os_info


class GcConan(ConanFile):
    name = "cg-toolkit"
    version = "3.1"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        self.copy("*.h", src="include", dst="include")
        if os_info.is_linux:
            if self.settings.arch.__contains__('64'):
                self.copy("*.so", src="lib64", dst="lib", keep_path=False)
            else:
                self.copy("*.so", src="lib", dst="lib", keep_path=False)
        else:
            if self.settings.arch.__contains__('64'):
                self.copy("*.lib", src="lib64", dst="lib", keep_path=False)
                self.copy("*.dll", src="bin64", dst="bin", keep_path=False)
            else:
                self.copy("*.lib", src="lib", dst="lib", keep_path=False)
                self.copy("*.dll", src="bin", dst="bin", keep_path=False)

    def package_info(self): 
        self.cpp_info.name = "Cg"
        self.cpp_info.libs = tools.collect_libs(self)
