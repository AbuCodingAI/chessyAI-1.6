#pragma once

#include <vector>
#include <string>

class WeightManager {
public:
    // Save weights to file
    static void saveWeights(const std::string& path, const std::vector<std::vector<float>>& weights);
    
    // Load weights from file
    static std::vector<std::vector<float>> loadWeights(const std::string& path);
    
    // Initialize weights randomly
    static std::vector<std::vector<float>> initializeWeights(const std::vector<int>& layerSizes);
};
