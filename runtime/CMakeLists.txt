cmake_minimum_required(VERSION 3.15)
project(gesture_runtime)

set(CMAKE_CXX_STANDARD 17)

# GLAD
add_library(glad third_party/glad/src/glad.c)
target_include_directories(glad PUBLIC third_party/glad/include)

# OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# GLFW
find_package(glfw3 REQUIRED)

# Main Executable
add_executable(gesture_runtime
    src/main.cpp
    src/renderer.cpp
)

target_link_libraries(gesture_runtime
    glad
    glfw
    ${OpenCV_LIBS}
)

add_custom_target(run
    COMMAND ${CMAKE_BINARY_DIR}/gesture_runtime
    DEPENDS gesture_runtime
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}    
)
