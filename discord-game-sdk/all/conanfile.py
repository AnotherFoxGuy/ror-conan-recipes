from conans import CMake, ConanFile, tools
from conans.tools import os_info


class DiscordGameSDKConan(ConanFile):
    name = "discord-game-sdk"
    author = "Edgar Edgar@AnotherFoxGuy.com"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _cmake = None

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination="src")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        if os_info.is_windows:
            if self.settings.arch.__contains__('64'):
                self.copy("*.lib", src="src/lib/x86_64", dst="lib", keep_path=False)
                self.copy("*.dll", src="src/lib/x86_64", dst="bin", keep_path=False)
            else:
                self.copy("*.lib", src="src/lib/x86", dst="lib", keep_path=False)
                self.copy("*.dll", src="src/lib/x86", dst="bin", keep_path=False)
        elif os_info.is_macos:
            self.copy("*.bundle", src="src/lib/x86_64", dst="lib", keep_path=False)
            self.copy("*.dylib", src="src/lib/x86_64", dst="bin", keep_path=False)
            self.copy("*.so", src="src/lib/x86_64", dst="lib", keep_path=False)
        else:
            self.copy("*.so", src="src/lib/x86_64", dst="lib", keep_path=False)

    def package_info(self): 
        self.cpp_info.name = "DiscordGameSDK"
        self.cpp_info.libs = tools.collect_libs(self)
