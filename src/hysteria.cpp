#include <string>
#if defined(__MINGW32__) && defined(_M_ARM64)
    // CPython 3.14t uses MSVC's __getReg(18) intrinsic to read the Windows
    // ARM64 thread environment block, but LLVM-MinGW does not provide it.
    // Windows reserves x18 for that pointer, so provide the equivalent here.
    #include <cstdint>
    static inline std::uintptr_t getArm64ThreadPointer()
    {
        std::uintptr_t value;
        __asm__ __volatile__("mov %0, x18" : "=r"(value));
        return value;
    }
    #define __getReg(registerNumber) getArm64ThreadPointer()
#endif
#if defined _WIN64
    #define _hypot hypot
    #include <cmath>
#endif
#include <pybind11/pybind11.h>
#if defined(__MINGW32__) && defined(_M_ARM64)
    #undef __getReg
#endif

#include "hysteria.h"

namespace py = pybind11;

namespace {
    void startFromJSON(const std::string& json, const std::string& rule="", const std::string& mmdb="")
    {
        GoString jsonString{json.data(), static_cast<ptrdiff_t>(json.size())};
        GoString ruleString{rule.data(), static_cast<ptrdiff_t>(rule.size())};

        GoSlice mmdbBytes{const_cast<void*>(static_cast<const void*>(mmdb.data())),
            static_cast<GoInt>(mmdb.size()), static_cast<GoInt>(mmdb.size())};

        {
            py::gil_scoped_release release;

            startClientFromJSON(jsonString, ruleString, mmdbBytes);

            py::gil_scoped_acquire acquire;
        }
    }

    // TODO: After auditing and testing the C++ and Go paths for free-threaded
    // safety, use PYBIND11_MODULE(hysteria, m, py::mod_gil_not_used()) so
    // importing this extension does not cause free-threaded CPython to enable
    // the GIL.
    PYBIND11_MODULE(hysteria, m) {
        m.def("startFromJSON",
            &startFromJSON,
            "Start Hysteria client with JSON, ACL rule and MMDB",
            py::arg("json"), py::arg("rule") = "", py::arg("mmdb") = "");

        m.attr("__version__") = "1.3.5.3";
    }
}
