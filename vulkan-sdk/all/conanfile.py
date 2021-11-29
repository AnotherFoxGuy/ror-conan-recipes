from conans import ConanFile, tools
from conans.tools import os_info


class VulkanConan(ConanFile):
    name = "vulkan-sdk"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"
    no_copy_source = True

    def requirements(self):
      if os_info.is_windows:
         self.requires("7zip/19.00")

    def source(self):
        if os_info.is_windows:
            tools.download(**self.conan_data["sources-windows"][self.version], filename="vulkan-sdk.exe")
            self.run("7z x vulkan-sdk.exe -ox86_64")
        elif os_info.is_linux:
            tools.get(**self.conan_data["sources-linux"][self.version], strip_root=True)
        else:
            raise Exception("Binary does not exist for these settings")

    def package(self):
        self.copy("*", src="x86_64", dst=".")

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
