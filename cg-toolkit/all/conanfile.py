from conan import ConanFile
from conan.tools.files import get, collect_libs
from conans.client.tools.oss import OSInfo

class GcConan(ConanFile):
    name = "cg-toolkit"
    version = "3.1"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"
    exports_sources = "dummy-file-to-fix-cloudsmith"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        self.copy("*.h", src="include", dst="include")
        os_info = OSInfo()
        if os_info.is_linux:
            if '64' in self.settings.arch:
                self.copy("*.so", src="lib64", dst="lib", keep_path=False)
            else:
                self.copy("*.so", src="lib", dst="lib", keep_path=False)
        else:
            if '64' in self.settings.arch:
                self.copy("*.lib", src="lib64", dst="lib", keep_path=False)
                self.copy("*.dll", src="bin64", dst="bin", keep_path=False)
            else:
                self.copy("*.lib", src="lib", dst="lib", keep_path=False)
                self.copy("*.dll", src="bin", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.name = "Cg"
        self.cpp_info.libs = collect_libs(self)
