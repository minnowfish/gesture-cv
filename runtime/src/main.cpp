#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include "renderer.h"
#include <opencv2/opencv.hpp>

int main() {
    if (!glfwInit()) {
        std::cerr << "Failed to create window" << std::endl;
        return -1;
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "Gesture 3D", nullptr, nullptr);
    if (!window) {
        std::cerr << "Failed to create window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Failed to init GLAD" << std::endl;
        return -1;
    }

    cv::VideoCapture cam(0);
    Renderer renderer;

    while (!glfwWindowShouldClose(window)) {
        
        cv::Mat frame;
        cam.read(frame);

        glClear(GL_COLOR_BUFFER_BIT);
        renderer.draw(frame);
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    cam.release();

    glfwTerminate();
    return 0;

}