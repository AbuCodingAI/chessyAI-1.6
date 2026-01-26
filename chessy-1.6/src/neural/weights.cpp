#include "weights.h"
#include <fstream>
#include <random>

void WeightManager::saveWeights(const std::string& path, const std::vector<std::vector<float>>& weights) {
    std::ofstream file(path, std::ios::binary);
    
    int numLayers = weights.size();
    file.write(reinterpret_cast<char*>(&numLayers), sizeof(int));
    
    for (const auto& layer : weights) {
        int size = layer.size();
        file.write(reinterpret_cast<char*>(&size), sizeof(int));
        
        for (float w : layer) {
            file.write(reinterpret_cast<char*>(&w), sizeof(float));
        }
    }
    
    file.close();
}

std::vector<std::vector<float>> WeightManager::loadWeights(const std::string& path) {
    std::vector<std::vector<float>> weights;
    std::ifstream file(path, std::ios::binary);
    
    int numLayers;
    file.read(reinterpret_cast<char*>(&numLayers), sizeof(int));
    
    for (int i = 0; i < numLayers; i++) {
        int size;
        file.read(reinterpret_cast<char*>(&size), sizeof(int));
        
        std::vector<float> layer(size);
        for (int j = 0; j < size; j++) {
            file.read(reinterpret_cast<char*>(&layer[j]), sizeof(float));
        }
        
        weights.push_back(layer);
    }
    
    file.close();
    return weights;
}

std::vector<std::vector<float>> WeightManager::initializeWeights(const std::vector<int>& layerSizes) {
    std::vector<std::vector<float>> weights;
    std::random_device rd;
    std::mt19937 gen(rd());
    
    for (size_t i = 0; i < layerSizes.size() - 1; i++) {
        int inputSize = layerSizes[i];
        int outputSize = layerSizes[i + 1];
        
        float limit = std::sqrt(6.0f / (inputSize + outputSize));
        std::uniform_real_distribution<> dis(-limit, limit);
        
        std::vector<float> layer(inputSize * outputSize);
        for (float& w : layer) {
            w = dis(gen);
        }
        
        weights.push_back(layer);
    }
    
    return weights;
}
