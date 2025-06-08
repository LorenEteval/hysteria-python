#include <string>
#if defined _WIN64
    #define _hypot hypot
    #include <cmath>
#endif
#include <pybind11/pybind11.h>

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

    PYBIND11_MODULE(hysteria, m) {
        m.def("startFromJSON",
            &startFromJSON,
            "Start Hysteria client with JSON, ACL rule and MMDB",
            py::arg("json"), py::arg("rule") = "", py::arg("mmdb") = "");

        m.attr("__version__") = "1.3.5.2";
    }
}
