#pragma once

#include <string>

struct OverfittingPrevention {
    // Early stopping (OPTIMIZED FOR FREE TIER)
    bool enableEarlyStopping = true;
    int patienceEpochs = 5;            // Reduced from 10 for faster stopping
    float minValidationImprovement = 0.001f;  // Minimum improvement threshold
    
    // Regularization
    float l2Regularization = 0.0001f;  // L2 weight decay
    float dropoutRate = 0.3f;          // Dropout rate (0.2-0.4 typical)
    
    // Data augmentation
    bool enableDataAugmentation = true;
    float augmentationRate = 0.2f;     // Augment 20% of training data
    
    // Validation strategy (OPTIMIZED FOR FREE TIER)
    int validationSplitRatio = 20;     // 80/20 train/validation split
    bool enableCrossValidation = false; // Disabled for speed
    int kFolds = 5;                    // K-fold cross-validation
};

struct TrainingConfig {
    // Data generation (OPTIMIZED FOR FREE TIER)
    int numGamesGeneration = 500;      // Reduced from 1000 for speed
    int stockfishDepth = 12;           // Reduced from 15 for speed
    float blunderRate = 0.05f;         // 5% blunder injection
    
    // Neural network training (OPTIMIZED FOR FREE TIER)
    int epochs = 50;                   // Reduced from 100 for speed
    float learningRate = 0.001f;       // Adam learning rate
    int batchSize = 32;                // Batch size
    
    // Self-play and testing (OPTIMIZED FOR FREE TIER)
    int numSelfPlayGames = 250;        // Reduced from 500 for speed
    int numTestGames = 50;             // Reduced from 100 for speed
    
    // Overfitting prevention
    OverfittingPrevention overfitting;
    
    // Checkpointing
    bool enableCheckpointing = true;
    std::string checkpointDir = "./checkpoints";
    int checkpointInterval = 3;        // Save every 3 epochs (was 5)
    
    // Cloud deployment
    bool isCloudDeployment = true;     // Enable for cloud
    int maxTrainingHours = 5;          // Reduced from 24 for free tier (safe limit)
    std::string modelOutputPath = "./models/chessy-1.6-trained.bin";
};
