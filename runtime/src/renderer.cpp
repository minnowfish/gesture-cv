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