#pragma once

#include <vector>
#include <Eigen/Dense>

using MatrixXf = Eigen::MatrixXf;
using VectorXf = Eigen::VectorXf;

class NeuralNetwork {
public:
    NeuralNetwork(const std::vector<int>& layerSizes);
    
    // Forward pass
    float evaluate(const std::vector<float>& input);
    
    // Training
    void train(const std::vector<std::vector<float>>& inputs,
               const std::vector<float>& targets,
               int epochs, float learningRate);
    
    // Save/Load weights
    void saveWeights(const std::string& path);
    void loadWeights(const std::string& path);
    
    // Get/Set weights
    const std::vector<MatrixXf>& getWeights() const { return weights; }
    const std::vector<VectorXf>& getBiases() const { return biases; }
    
private:
    std::vector<int> layerSizes;
    std::vector<MatrixXf> weights;
    std::vector<VectorXf> biases;
    std::vector<VectorXf> activations;
    std::vector<VectorXf> deltas;
    
    // Activation functions
    float relu(float x) const;
    float reluDerivative(float x) const;
    float sigmoid(float x) const;
    float sigmoidDerivative(float x) const;
    float tanh(float x) const;
    float tanhDerivative(float x) const;
    
    // Forward pass with caching
    void forward(const std::vector<float>& input);
    
    // Backward pass
    void backward(float target, float learningRate);
    
    // Initialize weights
    void initializeWeights();
};
