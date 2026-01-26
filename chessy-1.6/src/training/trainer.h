#pragma once

#include "../chess/board.h"
#include "../neural/network.h"
#include "stockfish_interface.h"
#include "trainer_config.h"
#include <vector>
#include <string>
#include <chrono>

struct TrainingResult {
    float trainingLoss = 0.0f;
    float validationLoss = 0.0f;
    float selfPlayWinRate = 0.0f;
    float stockfishWinRate = 0.0f;
    float estimatedELO = 1200.0f;
    int epochsCompleted = 0;
    bool stoppedEarly = false;
    std::string stopReason = "";
};

class Trainer {
public:
    Trainer(const TrainingConfig& config, const std::string& stockfishPath);
    
    // Full training pipeline
    TrainingResult train();
    
    // Individual steps
    void generateTrainingData();
    void trainNeuralNetwork();
    void selfPlay();
    void testVsStockfish();
    
    // Save/Load
    void saveModel(const std::string& path);
    void loadModel(const std::string& path);
    void saveCheckpoint(int epoch);
    bool loadCheckpoint();
    
    // Get results
    const TrainingResult& getResults() const { return results; }
    
    // Overfitting prevention
    bool shouldStopEarly(float currentValidationLoss);
    void applyDropout(std::vector<float>& features);
    void augmentTrainingData();
    
private:
    TrainingConfig config;
    StockfishInterface stockfish;
    NeuralNetwork network;
    
    std::vector<Position> trainingData;
    std::vector<Position> validationData;
    TrainingResult results;
    
    // Early stopping tracking
    float bestValidationLoss = std::numeric_limits<float>::max();
    int epochsSinceImprovement = 0;
    std::chrono::steady_clock::time_point trainingStartTime;
    
    // Helper functions
    std::vector<float> positionToFeatures(const Board& board);
    float evaluatePosition(const Board& board);
    float playGame(bool useNeuralNetwork, int timePerMove);
    float calculateELO(float winRate);
    bool hasTimeRemaining();
};
