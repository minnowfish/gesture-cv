#ifndef RENDERER_H
#define RENDERER_H
#include <opencv2/opencv.hpp>

#include <glad/glad.h>

class Renderer {
    private:
        unsigned int VAO, VBO, EBO, shaderProgram, texture;
    
    public:
        Renderer();

        void draw(cv::Mat frame);
};

#endif