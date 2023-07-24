# hysteria-python

Python bindings for [hysteria](https://github.com/apernet/hysteria), a feature-packed proxy & relay tool. This package
provides a bridge to start hysteria client directly from Python on any platform.

Looking for [Xray-core](https://github.com/XTLS/Xray-core) bindings?
Check [Xray-core-python](https://github.com/LorenEteval/Xray-core-python).

## Start

To use this binding, please first make sure that:

* You are a Python developer, or your application is associated with this package.
* You are building a client application. There is no point to use binding on the server side.
* You want to provide additional abstraction for your client. The core(i.e. hysteria) will be shipped with your
  application as dynamic link library, not an executable.
* This bridge provides functionality to start hysteria directly from Python string(see the API below). What that means
  is that the client config stays in memory all the time, and cannot(or very hard to) be inspected. So you can, for
  example, get a configuration template from a remote server and edit it for a group of specific client and start the
  service.

## Install

### Core Building Tools

You have to install the following tools to be able to install this package successfully.

* [go](https://go.dev/doc/install) in your PATH. go 1.20.0 and above is recommended. To check go is ready,
  type `go version`. Also, if google service is blocked in your region(such as Mainland China), you have to configure
  your GOPROXY to be able to pull go packages. For Chinese users, refer to [goproxy.cn](https://goproxy.cn/) for more
  information.
* [cmake](https://cmake.org/download/) in your PATH. To check cmake is ready, type `cmake --version`.
* A working GNU C++ compiler(i.e. GNU C++ toolchains). To check GNU C++ compiler is ready, type `g++ --version`. These
  tools should have been installed in Linux or macOS by default. If you don't have GNU C++ toolchains(especially for
  Windows users) anyway:

    * For Linux users: type `sudo apt update && sudo apt install g++` and that should work out fine.
    * For Windows users: install [MinGW-w64](https://sourceforge.net/projects/mingw-w64/files/mingw-w64/)
      or [Cygwin](https://www.cygwin.com/) and make sure you have add them to PATH.

### Install Package

```
pip install hysteria
```

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
source code as a submodule. To track what modifications have been to the source code, you can compare it with the same
version under Python binding and corresponding go repository.

## Tested Platform

This package should behave well in all platform that go and Python target on. I built and ran the binding successfully
on:

* macOS 12.5.1 Apple Silicon
* Ubuntu 20.04, Ubuntu 22.04
* Windows 11 22H2

## License

The license for this project follows its original go repository [hysteria](https://github.com/apernet/hysteria) and is
under [MIT License](https://github.com/LorenEteval/hysteria-python/blob/main/LICENSE).
