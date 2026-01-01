cmake_minimum_required(VERSION 3.21)
project(${SKBUILD_PROJECT_NAME})
# Set Python module name (should match the .pyx filename)
string(REPLACE "-" "_" MODULE_NAME ${SKBUILD_PROJECT_NAME})

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optimize for performance
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -DNDEBUG")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2")
endif()

# Additional optimization flags for GCC/Clang
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native -mtune=native -fomit-frame-pointer -fno-stack-protector")
endif()

# Set build type to Release for better performance
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()


list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Find Python and Cython
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(Cython MODULE REQUIRED VERSION 3.0)
include(UseCython)




# Configure Cython module
cython_transpile(src/${MODULE_NAME}/${MODULE_NAME}.pyx LANGUAGE CXX OUTPUT_VARIABLE curl_file)

# Create Python module
python_add_library(${MODULE_NAME} MODULE "${curl_file}" WITH_SOABI)

set_target_properties(${MODULE_NAME} PROPERTIES
    INSTALL_RPATH "$ORIGIN/curl/lib"
    BUILD_RPATH "$ORIGIN/curl/lib"
    SKIP_RPATH FALSE
    INSTALL_RPATH_USE_LINK_PATH TRUE
)


include(ExternalProject)
# Set curl install directory
set(CURL_INSTALL_DIR ${CMAKE_BINARY_DIR}/curl/install)

# Define external project for zlib
ExternalProject_Add(install_zlib
    SOURCE_DIR ${CMAKE_SOURCE_DIR}/src/third_party/zlib
    BINARY_DIR ${CMAKE_BINARY_DIR}/zlib/build
    INSTALL_DIR ${CMAKE_BINARY_DIR}/zlib/install

    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
        -DCMAKE_INSTALL_LIBDIR=lib

    BUILD_ALWAYS OFF
    UPDATE_DISCONNECTED TRUE
    STEP_TARGETS build install
    LOG_CONFIGURE OFF
    LOG_BUILD OFF
    LOG_INSTALL OFF
    COMMENT "Building and installing zlib"
)

# Define external project for nghttp2
ExternalProject_Add(install_nghttp2
    SOURCE_DIR ${CMAKE_SOURCE_DIR}/src/third_party/nghttp2
    BINARY_DIR ${CMAKE_BINARY_DIR}/nghttp2/build
    INSTALL_DIR ${CMAKE_BINARY_DIR}/nghttp2/install

    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
        -DCMAKE_INSTALL_LIBDIR=lib
        -DENABLE_LIB_ONLY=ON

    BUILD_ALWAYS OFF
    UPDATE_DISCONNECTED TRUE
    STEP_TARGETS build install
    LOG_CONFIGURE OFF
    LOG_BUILD OFF
    LOG_INSTALL OFF
    COMMENT "Building and installing nghttp2"
)

# Define external project for brotli using CMake
ExternalProject_Add(install_brotli
    SOURCE_DIR ${CMAKE_SOURCE_DIR}/src/third_party/brotli
    BINARY_DIR ${CMAKE_BINARY_DIR}/brotli/build
    INSTALL_DIR ${CMAKE_BINARY_DIR}/brotli/install

    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
        -DCMAKE_INSTALL_LIBDIR=lib
        -DBROTLI_DISABLE_TESTS=ON

    BUILD_ALWAYS OFF
    UPDATE_DISCONNECTED TRUE
    STEP_TARGETS build install
    LOG_CONFIGURE OFF
    LOG_BUILD OFF
    LOG_INSTALL OFF
    COMMENT "Building and installing brotli"
)




# Define external project for zstd using Makefile
ExternalProject_Add(install_zstd
    SOURCE_DIR ${CMAKE_SOURCE_DIR}/src/third_party/zstd
    BINARY_DIR ${CMAKE_BINARY_DIR}/zstd/build
    INSTALL_DIR ${CMAKE_BINARY_DIR}/zstd/install

    CONFIGURE_COMMAND ""
    BUILD_COMMAND make -C ${CMAKE_SOURCE_DIR}/src/third_party/zstd lib-release
    INSTALL_COMMAND make -C ${CMAKE_SOURCE_DIR}/src/third_party/zstd PREFIX=<INSTALL_DIR> install

    BUILD_ALWAYS OFF
    UPDATE_DISCONNECTED TRUE
    STEP_TARGETS build install
    LOG_CONFIGURE OFF
    LOG_BUILD OFF
    LOG_INSTALL OFF
    COMMENT "Building and installing zstd"
)

# Define external project for curl
ExternalProject_Add(install_curl
    SOURCE_DIR ${CMAKE_SOURCE_DIR}/src/third_party/curl
    BINARY_DIR ${CMAKE_BINARY_DIR}/curl/build
    INSTALL_DIR ${CURL_INSTALL_DIR}

    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
        -DCMAKE_INSTALL_LIBDIR=lib
        -DBUILD_SHARED_LIBS=ON
        -DBUILD_CURL_EXE=ON
        -DBUILD_TESTING=OFF
        -DUSE_MANUAL=OFF
        -DUSE_OPENSSL=ON
        -DENABLE_MANUAL=OFF
        -DCURL_ZLIB=ON
        -DZLIB_ROOT=${CMAKE_BINARY_DIR}/zlib/install
        -DZLIB_INCLUDE_DIR=${CMAKE_BINARY_DIR}/zlib/install/include
        -DZLIB_LIBRARY=${CMAKE_BINARY_DIR}/zlib/install/lib/libz.so
        -DUSE_NGHTTP2=ON
        -DNGHTTP2_ROOT=${CMAKE_BINARY_DIR}/nghttp2/install
        -DNGHTTP2_INCLUDE_DIR=${CMAKE_BINARY_DIR}/nghttp2/install/include
        -DNGHTTP2_LIBRARY=${CMAKE_BINARY_DIR}/nghttp2/install/lib/libnghttp2.so
        -DCURL_BROTLI=ON
        -DBROTLI_ROOT=${CMAKE_BINARY_DIR}/brotli/install
        -DBROTLI_INCLUDE_DIR=${CMAKE_BINARY_DIR}/brotli/install/include
        -DBROTLIDEC_LIBRARY=${CMAKE_BINARY_DIR}/brotli/install/lib/libbrotlidec.so
        -DBROTLIENC_LIBRARY=${CMAKE_BINARY_DIR}/brotli/install/lib/libbrotlienc.so
        -DBROTLICOMMON_LIBRARY=${CMAKE_BINARY_DIR}/brotli/install/lib/libbrotlicommon.so
        -DCURL_ZSTD=ON
        -DZSTD_ROOT=${CMAKE_BINARY_DIR}/zstd/install
        -DZSTD_INCLUDE_DIR=${CMAKE_BINARY_DIR}/zstd/install/include
        -DZSTD_LIBRARY=${CMAKE_BINARY_DIR}/zstd/install/lib/libzstd.so
        -DCURL_USE_LIBPSL=OFF
        -DCURL_USE_LIBIDN2=OFF

    DEPENDS install_zlib install_nghttp2 install_brotli install_zstd

    BUILD_ALWAYS OFF
    UPDATE_DISCONNECTED TRUE
    STEP_TARGETS build install
    LOG_CONFIGURE OFF
    LOG_BUILD OFF
    LOG_INSTALL OFF
    COMMENT "Building and installing curl"
)

# Add dependency so curl installation happens during build
add_dependencies(${MODULE_NAME} install_curl)





# Create interface library for curl
add_library(curl_interface INTERFACE)

target_include_directories(curl_interface INTERFACE
    ${CURL_INSTALL_DIR}/include
)

target_link_directories(curl_interface INTERFACE
    ${CURL_INSTALL_DIR}/lib
)

target_link_libraries(curl_interface INTERFACE
    curl
)

# Link curl interface to the main module
target_link_libraries(${MODULE_NAME} PRIVATE curl_interface)

# Install the Python module
install(TARGETS ${MODULE_NAME}
    DESTINATION ${SKBUILD_PROJECT_NAME}
)

# Copy curl installation to Python module directory
install(DIRECTORY ${CURL_INSTALL_DIR}/
    DESTINATION ${SKBUILD_PROJECT_NAME}/curl
)