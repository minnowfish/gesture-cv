#include "renderer.h"
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <GLFW/glfw3.h>


const std::string vertexFilePath = "shaders/background.vert";
const std::string fragmentFilePath = "shaders/background.frag";

Renderer::Renderer() {
    float quad_vertices[] = {
        -1.0f, 1.0f, 0.0f, 0.0f, 1.0f, // top left
        1.0f, 1.0f, 0.0f, 1.0f, 1.0f, // top right
        1.0f, -1.0f, 0.0f, 1.0f, 0.0f, // bottom right
        -1.0f, -1.0f, 0.0f, 0.0f, 0.0f, // bottom left
    };

    // EBO (Element Buffer Object)
    unsigned int indices[] = {
        0, 1, 2, // first triangle
        0, 2, 3, // second triangle
    };

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(quad_vertices), quad_vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5*sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glBindVertexArray(0);

    std::ifstream vertexFile(vertexFilePath, std::ios::in);
    std::ifstream fragmentFile(fragmentFilePath, std::ios::in);
    std::string vertexString;
    std::string fragmentString;

    if (vertexFile.is_open()) {
        std::stringstream buffer;
        buffer << vertexFile.rdbuf();
        vertexString = buffer.str();
    } else {
        std::cerr << "Failed to open vertex shader: " << vertexFilePath << std::endl;
    }

    if (fragmentFile.is_open()) {
        std::stringstream buffer;
        buffer << fragmentFile.rdbuf();
        fragmentString = buffer.str();
    } else {
        std::cerr << "Failed to open fragment shader: " << fragmentFilePath << std::endl;
    }

    const char* vertexCode = vertexString.c_str();
    const char* fragmentCode = fragmentString.c_str();

    unsigned int vertexShader;
    unsigned int fragShader;
    int success;
    char infoLog[512];

    vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexCode, NULL);
    glCompileShader(vertexShader);

    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);

    if (!success) {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    } 

    fragShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragShader, 1, &fragmentCode, NULL);
    glCompileShader(fragShader);

    glGetShaderiv(fragShader, GL_COMPILE_STATUS, &success);

    if (!success) {
        glGetShaderInfoLog(fragShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    } 

    shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragShader);
    glLinkProgram(shaderProgram);
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);

    if (!success) {
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
    }

    glDeleteShader(vertexShader);
    glDeleteShader(fragShader);

    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0);
}

void Renderer::draw(cv::Mat frame) {
    if (frame.empty()) {
        return;
    }

    cv::Mat rgb_frame;
    cv::cvtColor(frame, rgb_frame, cv::COLOR_BGR2RGB);

    glBindTexture(GL_TEXTURE_2D, texture);

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, rgb_frame.cols, rgb_frame.rows, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_frame.data);

    glUseProgram(shaderProgram);
    GLint samplerLocation = glGetUniformLocation(shaderProgram, "webcamTexture");

    glUniform1i(samplerLocation, 0);

    glBindVertexArray(VAO);
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
    glBindVertexArray(0);
    glBindTexture(GL_TEXTURE_2D, 0);
}
