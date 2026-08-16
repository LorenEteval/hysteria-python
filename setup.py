import os
import pathlib
import platform
import shlex
import subprocess
import sys
from importlib import metadata

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


ROOT_DIR = pathlib.Path(__file__).resolve().parent
PACKAGE_NAME = 'hysteria'
BINDING_NAME = 'hysteria'


def getHysteriaVersion():
    # Hysteria version is specified by environment variables.
    # Specify a fixed version corresponding to the git tag.
    return '1.3.5.3'


def runCommand(command, *, env=None):
    subprocess.run(command, check=True, env=env)


def getMacOSArchitecture():
    arch_flags = shlex.split(os.environ.get('ARCHFLAGS', ''))
    architectures = []

    for index, flag in enumerate(arch_flags):
        if flag == '-arch' and index + 1 < len(arch_flags):
            architecture = arch_flags[index + 1]
            if architecture not in architectures:
                architectures.append(architecture)

    if len(architectures) > 1 or architectures == ['universal2']:
        raise RuntimeError(
            'Universal2 wheels are not supported because the Go c-archive '
            'contains a single architecture'
        )

    if not architectures:
        return None

    architecture = architectures[0]
    go_architectures = {
        'arm64': 'arm64',
        'x86_64': 'amd64',
    }

    if architecture not in go_architectures:
        raise RuntimeError(f'Unsupported macOS architecture: {architecture}')

    return architecture, go_architectures[architecture]


class CMakeExtension(Extension):
    '''A setuptools extension whose compilation is delegated to CMake.'''

    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = str(pathlib.Path(sourcedir).resolve())


class BuildHysteriaExtension(build_ext):
    '''Build the Go archive and the pybind11 module for a wheel/install.'''

    def build_extension(self, ext):
        extension_path = pathlib.Path(self.get_ext_fullpath(ext.name)).resolve()
        extension_dir = extension_path.parent
        build_root = pathlib.Path(self.build_temp).resolve() / ext.name.replace('.', '_')
        go_build_dir = build_root / 'gobuild'
        cmake_build_dir = build_root / 'cmake'

        extension_dir.mkdir(parents=True, exist_ok=True)
        go_build_dir.mkdir(parents=True, exist_ok=True)
        cmake_build_dir.mkdir(parents=True, exist_ok=True)

        system = platform.system()
        macos_architecture = getMacOSArchitecture() if system == 'Darwin' else None
        archive_name = f'{BINDING_NAME}.lib' if system == 'Windows' else f'{BINDING_NAME}.a'
        archive_path = go_build_dir / archive_name
        pybind11_cmake_dir = metadata.distribution('pybind11').locate_file(
            'pybind11/share/cmake/pybind11'
        )

        go_env = os.environ.copy()
        go_env['CGO_ENABLED'] = '1'

        if macos_architecture:
            go_env['GOARCH'] = macos_architecture[1]

        runCommand(
            [
                'go',
                'build',
                '-C',
                str(ROOT_DIR / 'hysteria-go'),
                '-o',
                str(archive_path),
                '-buildmode=c-archive',
                '-trimpath',
                '-ldflags',
                '-s -w -buildid=',
                './app/cmd',
            ],
            env=go_env,
        )

        build_type = 'Debug' if self.debug else 'Release'
        configure = [
            'cmake',
            '-S',
            ext.sourcedir,
            '-B',
            str(cmake_build_dir),
            f'-DCMAKE_BUILD_TYPE={build_type}',
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extension_dir}',
            f'-DHYSTERIA_GO_BUILD_DIR={go_build_dir}',
            f'-DPython_EXECUTABLE={sys.executable}',
            f'-Dpybind11_DIR={pybind11_cmake_dir}',
            '-DPYBIND11_FINDPYTHON=ON',
        ]

        if system == 'Windows':
            configure += ['-G', 'MinGW Makefiles']
        elif macos_architecture:
            configure += [f'-DCMAKE_OSX_ARCHITECTURES={macos_architecture[0]}']

        runCommand(configure)
        runCommand(
            [
                'cmake',
                '--build',
                str(cmake_build_dir),
                '--config',
                build_type,
                '--target',
                BINDING_NAME,
                '--parallel',
            ]
        )

        if not extension_path.is_file():
            produced = sorted(extension_dir.glob(f'{BINDING_NAME}.*'))
            raise RuntimeError(
                f'CMake did not produce the expected extension {extension_path}; '
                f'found: {produced}'
            )


with open(ROOT_DIR / 'README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


setup(
    name=PACKAGE_NAME,
    version=getHysteriaVersion(),
    license='MIT',
    description='Python bindings for hysteria, a feature-packed proxy & relay tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Loren Eteval',
    author_email='loren.eteval@proton.me',
    url='https://github.com/LorenEteval/hysteria-python',
    cmdclass={'build_ext': BuildHysteriaExtension},
    ext_modules=[CMakeExtension('hysteria.hysteria', sourcedir=ROOT_DIR)],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
    ],
    zip_safe=False,
)
