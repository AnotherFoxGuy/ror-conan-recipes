from conan import ConanFile
from conan.tools.microsoft import (
    MSBuildToolchain,
    MSBuild,
    VCVars,
)
from conan.tools.files import (
    collect_libs,
    get,
    copy,
    chdir,
)
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.52.0"


class BounceConan(ConanFile):
    name = "bounce"
    description = "short description"
    license = ""
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/project/package"
    settings = "os", "arch", "compiler", "build_type"

    def build_requirements(self):
        self.tool_requires("premake/5.0.0-alpha15")

    def layout(self):
        basic_layout(self)

    def _generator(self):
        if self.settings.compiler == "Visual Studio":
            generator = (
                "vs"
                + {
                    "17": "2022",
                    "16": "2019",
                    "15": "2017",
                    "14": "2015",
                }.get(str(self.settings.compiler.version))
            )
        else:
            generator = "gmake2"
        return generator

    def _winarch(self):
        return "Win32" if self.settings.arch == "x86" else "x86_x64"

    def source(self):
        get(
            self,
            **self.conan_data["sources"][self.version],
            destination=self.source_folder,
            strip_root=True,
        )

    def generate(self):
        if self.settings.compiler == "Visual Studio":
            tc = MSBuildToolchain(self)
            tc.generate()
            tc = VCVars(self)
            tc.generate()

        else:
            config = "debug" if self.settings.build_type == "Debug" else "release"
            config += "_x86_64"
            tc = AutotoolsToolchain(self)
            tc.make_args = [f"config={config}" ]
            tc.generate()

    def build(self):
        # Build using premake
        gen = self._generator()

        with chdir(self, self.source_folder):
            self.run(f"premake5 {gen}")

            if self.settings.compiler == "Visual Studio":
                msbuild = MSBuild(self)
                msbuild.build_type = str(self.settings.build_type).lower()
                msbuild.platform = self._winarch()
                msbuild.build(f"build/{gen}/bounce.sln", targets=["bounce"])
            else:
                with chdir(self, os.path.join(self.source_folder, "build/gmake2")):
                    autotools = Autotools(self)
                    autotools.make(target="bounce")

    def package(self):
        bt = str(self.settings.build_type).lower()
        copy(
            self,
            pattern="*.h",
            dst=os.path.join(self.package_folder, "include"),
            src=os.path.join(self.source_folder, "include"),
        )
        if self.settings.compiler == "Visual Studio":
            copy(
                self,
                pattern="*.lib",
                dst=os.path.join(self.package_folder, "lib"),
                src=os.path.join(  # build\vs2019\bin\x86\release\bounce\bounce.lib
                    self.source_folder, "build", self._generator(), "bin", self._winarch(), bt, "bounce",
                ),
            )
        else:
            copy(
                self,
                pattern="*.a",
                dst=os.path.join(self.package_folder, "lib"),
                src=os.path.join(  # build/gmake2/bin/x86_64/release/bounce/libbounce.a
                    self.source_folder, "build/gmake2/bin/x86_64", bt, "bounce",
                ),
            )

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
