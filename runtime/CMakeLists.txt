cmake_minimum_required(VERSION 3.15)
project(gesture_runtime)

set(CMAKE_CXX_STANDARD 17)

# GLAD
add_library(glad third_party/glad/src/glad.c)
target_include_directories(glad PUBLIC third_party/glad/include)

# GLFW
find_package(glfw3 REQUIRED)

# Main Executable
add_executable(gesture_runtime
    src/main.cpp
)

target_link_libraries(gesture_runtime
    glad
    glfw
)
