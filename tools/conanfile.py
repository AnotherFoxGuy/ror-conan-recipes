import os
from conans import ConanFile
from conans.errors import ConanInvalidConfiguration


class conantoolsConan(ConanFile):
    name = "afg-conan-tools"
    version = "1.0"
    description = "helper-tools"
    settings = "os", "arch"
    exports_sources = "bin/**"

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("Only Linux supported")

    def package(self):
        self.copy("*", src="bin", dst="bin", keep_path=True)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
