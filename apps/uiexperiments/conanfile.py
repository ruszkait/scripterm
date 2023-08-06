import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.scm import Git


class UiExperimentsPackage(ConanFile):
    name = "ui_experiments"
    package_type = "library"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    no_copy_source = True

    # use auto mode for versioning and git revision, on build server it will create automatically the
    # recipe version and both git url/revision
    revision_mode = 'scm'
    scm = {
        'type': 'git',
        'url': 'auto',
        'revision': 'auto'
    }

    def set_version(self):
        if self.version:
            return
        
        version = os.getenv('BUILD_NUMBER')
        if version:
            self.version = version.strip()
            return

        version = Git(self).run("describe --tags --abbrev=0")
        if version:
            self.version = version
            return

    def requirements(self):
        # transitive_headers = True -> dependency used in public header
        # transitive_headers = False -> independent public header
        self.requires("ftxui/4.1.1@", transitive_headers=True)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        toolchain = CMakeToolchain(self)
        toolchain.generate()

    def build(self):
        cmake = CMake(self)

        if self.should_configure:
            cmake.configure()

        if self.should_build:
            cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def layout(self):
        cmake_layout(self)
