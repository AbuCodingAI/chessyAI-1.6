#include "network.h"
#include <cmath>
#include <random>
#include <fstream>
#include <iostream>

NeuralNetwork::NeuralNetwork(const std::vector<int>& layerSizes) 
    : layerSizes(layerSizes) {
    initializeWeights();
}

void NeuralNetwork::initializeWeights() {
    std::random_device rd;
    std::mt19937 gen(rd());
    
    weights.clear();
    biases.clear();
    activations.clear();
    deltas.clear();
    
    for (size_t i = 0; i < layerSizes.size() - 1; i++) {
        int inputSize = layerSizes[i];
        int outputSize = layerSizes[i + 1];
        
        // Xavier initialization
        float limit = std::sqrt(6.0f / (inputSize + outputSize));
        std::uniform_real_distribution<float> dist(-limit, limit);
        
        MatrixXf w(outputSize, inputSize);
        for (int r = 0; r < outputSize; r++) {
            for (int c = 0; c < inputSize; c++) {
                w(r, c) = dist(gen);
            }
        }
        weights.push_back(w);
        
        VectorXf b = VectorXf::Zero(outputSize);
        biases.push_back(b);
    }
    
    // Initialize activation and delta vectors
    for (int size : layerSizes) {
        activations.push_back(VectorXf::Zero(size));
        deltas.push_back(VectorXf::Zero(size));
    }
}

float NeuralNetwork::relu(float x) const {
    return std::max(0.0f, x);
}

float NeuralNetwork::reluDerivative(float x) const {
    return x > 0 ? 1.0f : 0.0f;
}

float NeuralNetwork::sigmoid(float x) const {
    return 1.0f / (1.0f + std::exp(-x));
}

float NeuralNetwork::sigmoidDerivative(float x) const {
    float s = sigmoid(x);
    return s * (1.0f - s);
}

float NeuralNetwork::tanh(float x) const {
    return std::tanh(x);
}

float NeuralNetwork::tanhDerivative(float x) const {
    float t = tanh(x);
    return 1.0f - t * t;
}

void NeuralNetwork::forward(const std::vector<float>& input) {
    // Set input layer
    for (size_t i = 0; i < input.size(); i++) {
        activations[0](i) = input[i];
    }
    
    // Forward through hidden layers
    for (size_t layer = 0; layer < weights.size() - 1; layer++) {
        VectorXf z = weights[layer] * activations[layer] + biases[layer];
        
        // ReLU activation for hidden layers
        for (int i = 0; i < z.size(); i++) {
            activations[layer + 1](i) = relu(z(i));
        }
    }
    
    // Output layer with tanh activation (for evaluation -1 to 1)
    size_t lastLayer = weights.size() - 1;
    VectorXf z = weights[lastLayer] * activations[lastLayer] + biases[lastLayer];
    activations[lastLayer + 1](0) = tanh(z(0));
}

void NeuralNetwork::backward(float target, float learningRate) {
    // Output layer error
    float output = activations[activations.size() - 1](0);
    float error = output - target;
    deltas[deltas.size() - 1](0) = error * tanhDerivative(output);
    
    // Backpropagate through hidden layers
    for (int layer = weights.size() - 1; layer >= 0; layer--) {
        // Update weights and biases
        for (int i = 0; i < weights[layer].rows(); i++) {
            for (int j = 0; j < weights[layer].cols(); j++) {
                float gradient = deltas[layer + 1](i) * activations[layer](j);
                weights[layer](i, j) -= learningRate * gradient;
            }
            biases[layer](i) -= learningRate * deltas[layer + 1](i);
        }
        
        // Compute deltas for previous layer
        if (layer > 0) {
            VectorXf z = weights[layer - 1] * activations[layer - 1] + biases[layer - 1];
            for (int i = 0; i < activations[layer].size(); i++) {
                float delta = 0;
                for (int j = 0; j < deltas[layer + 1].size(); j++) {
                    delta += weights[layer](j, i) * deltas[layer + 1](j);
                }
                deltas[layer](i) = delta * reluDerivative(z(i));
            }
        }
    }
}

float NeuralNetwork::evaluate(const std::vector<float>& input) {
    forward(input);
    return activations[activations.size() - 1](0);
}

void NeuralNetwork::train(const std::vector<std::vector<float>>& inputs,
                          const std::vector<float>& targets,
                          int epochs, float learningRate) {
    for (int epoch = 0; epoch < epochs; epoch++) {
        float totalError = 0;
        
        for (size_t i = 0; i < inputs.size(); i++) {
            forward(inputs[i]);
            float output = activations[activations.size() - 1](0);
            float error = output - targets[i];
            totalError += error * error;
            
            backward(targets[i], learningRate);
        }
        
        float mse = totalError / inputs.size();
        if (epoch % 10 == 0) {
            std::cout << "Epoch " << epoch << " - MSE: " << mse << std::endl;
        }
    }
}

void NeuralNetwork::saveWeights(const std::string& path) {
    std::ofstream file(path, std::ios::binary);
    
    // Save layer sizes
    int numLayers = layerSizes.size();
    file.write(reinterpret_cast<char*>(&numLayers), sizeof(int));
    for (int size : layerSizes) {
        file.write(reinterpret_cast<char*>(&size), sizeof(int));
    }
    
    // Save weights and biases
    for (size_t i = 0; i < weights.size(); i++) {
        // Save weight matrix
        int rows = weights[i].rows();
        int cols = weights[i].cols();
        file.write(reinterpret_cast<char*>(&rows), sizeof(int));
        file.write(reinterpret_cast<char*>(&cols), sizeof(int));
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                float val = weights[i](r, c);
                file.write(reinterpret_cast<char*>(&val), sizeof(float));
            }
        }
        
        // Save bias vector
        int size = biases[i].size();
        file.write(reinterpret_cast<char*>(&size), sizeof(int));
        for (int j = 0; j < size; j++) {
            float val = biases[i](j);
            file.write(reinterpret_cast<char*>(&val), sizeof(float));
        }
    }
    
    file.close();
}

void NeuralNetwork::loadWeights(const std::string& path) {
    std::ifstream file(path, std::ios::binary);
    
    // Load layer sizes
    int numLayers;
    file.read(reinterpret_cast<char*>(&numLayers), sizeof(int));
    layerSizes.clear();
    for (int i = 0; i < numLayers; i++) {
        int size;
        file.read(reinterpret_cast<char*>(&size), sizeof(int));
        layerSizes.push_back(size);
    }
    
    // Load weights and biases
    weights.clear();
    biases.clear();
    
    for (int i = 0; i < numLayers - 1; i++) {
        // Load weight matrix
        int rows, cols;
        file.read(reinterpret_cast<char*>(&rows), sizeof(int));
        file.read(reinterpret_cast<char*>(&cols), sizeof(int));
        
        MatrixXf w(rows, cols);
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                float val;
                file.read(reinterpret_cast<char*>(&val), sizeof(float));
                w(r, c) = val;
            }
        }
        weights.push_back(w);
        
        // Load bias vector
        int size;
        file.read(reinterpret_cast<char*>(&size), sizeof(int));
        VectorXf b(size);
        for (int j = 0; j < size; j++) {
            float val;
            file.read(reinterpret_cast<char*>(&val), sizeof(float));
            b(j) = val;
        }
        biases.push_back(b);
    }
    
    file.close();
    
    // Reinitialize activation and delta vectors
    activations.clear();
    deltas.clear();
    for (int size : layerSizes) {
        activations.push_back(VectorXf::Zero(size));
        deltas.push_back(VectorXf::Zero(size));
    }
}
