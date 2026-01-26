#pragma once

#include <string>

struct OverfittingPrevention {
    // Early stopping
    bool enableEarlyStopping = true;
    int patienceEpochs = 10;           // Stop if validation loss doesn't improve for N epochs
    float minValidationImprovement = 0.001f;  // Minimum improvement threshold
    
    // Regularization
    float l2Regularization = 0.0001f;  // L2 weight decay
    float dropoutRate = 0.3f;          // Dropout rate (0.2-0.4 typical)
    
    // Data augmentation
    bool enableDataAugmentation = true;
    float augmentationRate = 0.2f;     // Augment 20% of training data
    
    // Validation strategy
    int validationSplitRatio = 20;     // 80/20 train/validation split
    bool enableCrossValidation = true;
    int kFolds = 5;                    // K-fold cross-validation
};

struct TrainingConfig {
    // Data generation
    int numGamesGeneration = 1000;     // Games for data generation
    int stockfishDepth = 15;           // Depth for Stockfish analysis
    float blunderRate = 0.05f;         // 5% blunder injection
    
    // Neural network training
    int epochs = 100;                  // Max epochs (early stopping may stop earlier)
    float learningRate = 0.001f;       // Adam learning rate
    int batchSize = 32;                // Batch size
    
    // Self-play and testing
    int numSelfPlayGames = 500;        // Self-play games
    int numTestGames = 100;            // Test games vs Stockfish
    
    // Overfitting prevention
    OverfittingPrevention overfitting;
    
    // Checkpointing
    bool enableCheckpointing = true;
    std::string checkpointDir = "./checkpoints";
    int checkpointInterval = 5;        // Save every N epochs
    
    // Cloud deployment
    bool isCloudDeployment = false;
    int maxTrainingHours = 24;         // Max training time per session
    std::string modelOutputPath = "./models/chessy-1.6-trained.bin";
};
