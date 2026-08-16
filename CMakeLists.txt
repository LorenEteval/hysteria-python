cmake_minimum_required(VERSION 3.15)
project(hysteria C CXX)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(
    CMAKE_LIBRARY_OUTPUT_DIRECTORY
    "${CMAKE_SOURCE_DIR}/build/lib/${PROJECT_NAME}"
    CACHE PATH "Directory for the Python extension"
)
set(
    HYSTERIA_GO_BUILD_DIR
    "${CMAKE_SOURCE_DIR}/gobuild"
    CACHE PATH "Directory containing the Go c-archive and generated header"
)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(${PROJECT_NAME} src/hysteria.cpp)

if (WIN32)
    if (MINGW)
        target_compile_options(${PROJECT_NAME} PRIVATE "-Wa,-mbig-obj")
        target_link_options(
            ${PROJECT_NAME} PRIVATE
            "-static-libgcc" "-static-libstdc++"
            "-Wl,-Bstatic,--whole-archive"
            "-lwinpthread"
            "-Wl,--no-whole-archive"
        )
    endif ()

    target_link_libraries(
        ${PROJECT_NAME} PRIVATE
        ${HYSTERIA_GO_BUILD_DIR}/hysteria.lib
    )
else ()
    target_link_libraries(
        ${PROJECT_NAME} PRIVATE
        ${HYSTERIA_GO_BUILD_DIR}/hysteria.a
        "-lresolv"
    )

    if (APPLE)
        target_link_libraries(
            ${PROJECT_NAME} PRIVATE
            "-framework CoreFoundation"
            "-framework Security"
        )
    endif ()
endif ()

target_include_directories(${PROJECT_NAME} PRIVATE ${HYSTERIA_GO_BUILD_DIR})
