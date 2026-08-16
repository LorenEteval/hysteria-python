# hysteria-python

[![Deploy PyPI](https://github.com/LorenEteval/hysteria-python/actions/workflows/deploy-pypi.yml/badge.svg?branch=main)](https://github.com/LorenEteval/hysteria-python/actions/workflows/deploy-pypi.yml)

Python bindings for [hysteria](https://github.com/apernet/hysteria), a feature-packed proxy & relay tool.

## Install

Install the package from PyPI:

```
pip install hysteria
```

Binary wheels include the native Hysteria binding, so installing a supported Python and platform combination does not
require Go, CMake, or a C/C++ compiler.

### Building from Source

If pip cannot find a compatible wheel, it may fall back to the source distribution. Building from source requires:

* [Go](https://go.dev/doc/install) 1.20 or newer in your PATH.
* [CMake](https://cmake.org/download/) in your PATH.
* A compatible C/C++ compiler toolchain: GCC or Clang on Linux, Apple Clang on macOS, MinGW-w64 on Windows x86_64,
  or LLVM-MinGW on Windows ARM64.

If Google services are blocked in your region, configure `GOPROXY` before building. Chinese users can refer
to [goproxy.cn](https://goproxy.cn/) for more information.

## API

```pycon
>>> import hysteria
>>> help(hysteria)  
Help on package hysteria:

NAME
    hysteria

PACKAGE CONTENTS
    hysteria

FUNCTIONS
    startFromJSON(...) method of builtins.PyCapsule instance
        startFromJSON(json: str, rule: str = '', mmdb: str = '') -> None

        Start Hysteria client with JSON, ACL rule and MMDB

VERSION
    1.3.5
```

## Source Code Modification

This repository, including the package that distributes to pypi,
contains [hysteria](https://github.com/apernet/hysteria) source code that's been
modified to build the binding and specific API. If without explicitly remark, the version of this package corresponds to
the version of the origin source code tag, so the binding will have full features as the original go distribution will
have. And due to its backward compatibility, there's no plan to generate bindings for older release of hysteria.

To make installation of this package easier, I didn't add the original [hysteria](https://github.com/apernet/hysteria)
source code as a submodule. To track what modifications have been made to the source code, you can compare it with the
same version under Python binding and corresponding go repository.

## Tested Platform

hysteria-python provides binary wheels for CPython 3.8 through 3.14, including the free-threaded CPython 3.13 and 3.14
variants. Windows ARM64 starts at CPython 3.9 because CPython 3.8 ARM64 wheels are not available through cibuildwheel.
The free-threaded interpreters are supported for installation, but importing the native extension currently enables
the GIL.

Every wheel is built and tested in [GitHub Actions](https://github.com/LorenEteval/hysteria-python/actions) on its native
platform before release.

| Platform | Architecture | Supported CPython |
|----------|:------------:|:-----------------:|
| Linux    | x86_64       | 3.8-3.14, 3.13t, 3.14t |
| Linux    | ARM64        | 3.8-3.14, 3.13t, 3.14t |
| Windows  | x86_64       | 3.8-3.14, 3.13t, 3.14t |
| Windows  | ARM64        | 3.9-3.14, 3.13t, 3.14t |
| macOS    | Intel        | 3.8-3.14, 3.13t, 3.14t |
| macOS    | Apple Silicon | 3.8-3.14, 3.13t, 3.14t |

## License

The license for this project follows its original go repository [hysteria](https://github.com/apernet/hysteria) and is
under [MIT License](https://github.com/LorenEteval/hysteria-python/blob/main/LICENSE).
