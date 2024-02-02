from conan import ConanFile
from conan.tools.files import get, collect_libs, download, copy
import os


class VulkanConan(ConanFile):
    name = "vulkan-sdk-bin"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "arch"

    def requirements(self):
        if self.settings.os == "Windows":
            self.requires("7zip/23.01")

    def build(self):
        if self.settings.os == "Windows":
            download(
                self,
                **self.conan_data["sources-windows"][self.version],
                filename="vulkan-sdk.7z"
            )
            self.run("7z x vulkan-sdk.7z -ox86_64")
        elif self.settings.os == "Linux":
            get(self, **self.conan_data["sources-linux"][self.version], strip_root=True)
        else:
            raise Exception("Binary does not exist for these settings")

    def package(self):
        copy(self, "*", os.path.join(self.source_folder, "x86_64"), self.package_folder)

    def package_info(self):
        self.cpp_info.set_property("cmake_module_file_name", "Vulkan")
        self.cpp_info.set_property("cmake_module_target_name", "Vulkan::Vulkan")
        self.cpp_info.set_property("cmake_file_name", "Vulkan")
        self.cpp_info.set_property("cmake_target_name", "Vulkan::Vulkan")
        self.cpp_info.libs = collect_libs(self)
