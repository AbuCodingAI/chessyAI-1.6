#include "trainer.h"
#include "../chess/moves.h"
#include <iostream>
#include <cmath>
#include <algorithm>
#include <random>
#include <fstream>
#include <filesystem>
#include <limits>

namespace fs = std::filesystem;

Trainer::Trainer(const TrainingConfig& config, const std::string& stockfishPath)
    : config(config), stockfish(stockfishPath), network({768, 512, 256, 128, 1}) {
    results = {0, 0, 0, 0, 0, 0, false, ""};
    trainingStartTime = std::chrono::steady_clock::now();
    
    // Create checkpoint directory
    if (config.enableCheckpointing) {
        fs::create_directories(config.checkpointDir);
    }
}

TrainingResult Trainer::train() {
    std::cout << "=== Chessy 1.6 Training Pipeline (Cloud-Ready) ===" << std::endl;
    std::cout << "Overfitting Prevention: ENABLED" << std::endl;
    std::cout << "Early Stopping: " << (config.overfitting.enableEarlyStopping ? "ON" : "OFF") << std::endl;
    std::cout << "Dropout Rate: " << (config.overfitting.dropoutRate * 100) << "%" << std::endl;
    std::cout << "L2 Regularization: " << config.overfitting.l2Regularization << std::endl;
    
    // Try to load checkpoint
    if (config.enableCheckpointing && loadCheckpoint()) {
        std::cout << "\n✓ Resumed from checkpoint (epoch " << results.epochsCompleted << ")" << std::endl;
    }
    
    std::cout << "\n[1/4] Generating training data..." << std::endl;
    generateTrainingData();
    
    if (!hasTimeRemaining()) {
        results.stopReason = "Time limit exceeded during data generation";
        return results;
    }
    
    std::cout << "\n[2/4] Training neural network..." << std::endl;
    trainNeuralNetwork();
    
    if (!hasTimeRemaining()) {
        results.stopReason = "Time limit exceeded during training";
        return results;
    }
    
    std::cout << "\n[3/4] Self-play improvement..." << std::endl;
    selfPlay();
    
    if (!hasTimeRemaining()) {
        results.stopReason = "Time limit exceeded during self-play";
        return results;
    }
    
    std::cout << "\n[4/4] Testing vs Stockfish..." << std::endl;
    testVsStockfish();
    
    std::cout << "\n=== Training Complete ===" << std::endl;
    std::cout << "Epochs Completed: " << results.epochsCompleted << std::endl;
    std::cout << "Validation Loss: " << results.validationLoss << std::endl;
    std::cout << "Estimated ELO: " << results.estimatedELO << std::endl;
    
    if (results.stoppedEarly) {
        std::cout << "⚠ Early Stopping: " << results.stopReason << std::endl;
    }
    
    // Save final model
    saveModel(config.modelOutputPath);
    
    return results;
}

void Trainer::generateTrainingData() {
    std::cout << "Generating " << config.numGamesGeneration << " games with Stockfish..." << std::endl;
    
    trainingData = stockfish.generateTrainingData(
        config.numGamesGeneration,
        config.stockfishDepth,
        config.blunderRate
    );
    
    std::cout << "Generated " << trainingData.size() << " positions" << std::endl;
    
    // Split into training and validation
    int splitPoint = trainingData.size() * (100 - config.overfitting.validationSplitRatio) / 100;
    validationData.assign(trainingData.begin() + splitPoint, trainingData.end());
    trainingData.erase(trainingData.begin() + splitPoint, trainingData.end());
    
    std::cout << "Training set: " << trainingData.size() << " positions" << std::endl;
    std::cout << "Validation set: " << validationData.size() << " positions" << std::endl;
    
    // Data augmentation
    if (config.overfitting.enableDataAugmentation) {
        augmentTrainingData();
    }
}

void Trainer::trainNeuralNetwork() {
    std::cout << "Training neural network for max " << config.epochs << " epochs..." << std::endl;
    std::cout << "Early stopping patience: " << config.overfitting.patienceEpochs << " epochs" << std::endl;
    
    // Pre-compute all features and targets (cache for speed)
    std::vector<std::vector<float>> inputs;
    std::vector<float> targets;
    inputs.reserve(trainingData.size());
    targets.reserve(trainingData.size());
    
    for (const Position& pos : trainingData) {
        Board board;
        board.fromFEN(pos.fen);
        
        std::vector<float> features = positionToFeatures(board);
        inputs.push_back(std::move(features));  // Move semantics for speed
        
        // Normalize evaluation to -1 to 1
        float target = std::tanh(pos.evaluation / 100.0f);
        targets.push_back(target);
    }
    
    // Pre-compute validation features too
    std::vector<std::vector<float>> validationInputs;
    std::vector<float> validationTargets;
    validationInputs.reserve(validationData.size());
    validationTargets.reserve(validationData.size());
    
    for (const Position& pos : validationData) {
        Board board;
        board.fromFEN(pos.fen);
        
        std::vector<float> features = positionToFeatures(board);
        validationInputs.push_back(std::move(features));
        
        float target = std::tanh(pos.evaluation / 100.0f);
        validationTargets.push_back(target);
    }
    
    // Training loop with early stopping
    for (int epoch = results.epochsCompleted; epoch < config.epochs; epoch++) {
        if (!hasTimeRemaining()) {
            results.stoppedEarly = true;
            results.stopReason = "Time limit exceeded";
            break;
        }
        
        // Train on batch
        network.train(inputs, targets, 1, config.learningRate);  // 1 epoch per iteration
        
        // Validate (optimized - no FEN parsing)
        float validationError = 0;
        for (size_t i = 0; i < validationInputs.size(); i++) {
            std::vector<float> features = validationInputs[i];  // Copy for dropout
            applyDropout(features);  // Apply dropout during validation
            
            float prediction = network.evaluate(features);
            float error = prediction - validationTargets[i];
            validationError += error * error;
        }
        
        results.validationLoss = validationError / validationInputs.size();
        results.epochsCompleted = epoch + 1;
        
        // Early stopping check
        if (config.overfitting.enableEarlyStopping) {
            if (shouldStopEarly(results.validationLoss)) {
                results.stoppedEarly = true;
                results.stopReason = "Validation loss plateaued";
                std::cout << "\n✓ Early stopping triggered at epoch " << epoch + 1 << std::endl;
                break;
            }
        }
        
        // Checkpoint
        if (config.enableCheckpointing && (epoch + 1) % config.checkpointInterval == 0) {
            saveCheckpoint(epoch + 1);
        }
        
        if ((epoch + 1) % 10 == 0) {
            std::cout << "Epoch " << (epoch + 1) << " - Validation MSE: " << results.validationLoss << std::endl;
        }
    }
    
    std::cout << "Training complete. Final Validation MSE: " << results.validationLoss << std::endl;
}

void Trainer::selfPlay() {
    std::cout << "Playing " << config.numSelfPlayGames << " self-play games..." << std::endl;
    
    float wins = 0;
    MoveGenerator moveGen;  // Reuse instead of creating each game
    
    for (int i = 0; i < config.numSelfPlayGames; i++) {
        float result = playGame(true, 5);  // 5 seconds per move
        if (result > 0.5f) wins++;
        
        if ((i + 1) % 10 == 0) {
            std::cout << "Completed " << (i + 1) << " games" << std::endl;
        }
    }
    
    results.selfPlayWinRate = wins / config.numSelfPlayGames;
    std::cout << "Self-play win rate: " << (results.selfPlayWinRate * 100) << "%" << std::endl;
}

void Trainer::testVsStockfish() {
    std::cout << "Testing against Stockfish (depth 10)..." << std::endl;
    
    float wins = 0;
    MoveGenerator moveGen;  // Reuse instead of creating each game
    
    for (int i = 0; i < config.numTestGames; i++) {
        Board board;
        board.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
        
        bool chessy1_6_white = (i % 2 == 0);
        int moveCount = 0;
        
        while (moveCount < 200) {  // Max 200 moves
            std::vector<Move> moves = moveGen.generateLegalMoves(board);
            if (moves.empty()) break;
            
            Move move;
            if ((board.getTurn() == Color::WHITE && chessy1_6_white) ||
                (board.getTurn() == Color::BLACK && !chessy1_6_white)) {
                // Chessy 1.6 move (optimized - cache features)
                std::vector<float> features = positionToFeatures(board);
                float bestEval = -2;
                Move bestMove = moves[0];
                
                for (const Move& m : moves) {
                    board.makeMove(m);
                    std::vector<float> nextFeatures = positionToFeatures(board);
                    float eval = network.evaluate(nextFeatures);
                    if (eval > bestEval) {
                        bestEval = eval;
                        bestMove = m;
                    }
                    board.unmakeMove(m);
                }
                move = bestMove;
            } else {
                // Stockfish move (use cached FEN)
                move = stockfish.getBestMove(board.toFEN(), 10);
            }
            
            board.makeMove(move);
            moveCount++;
        }
        
        // Determine winner (simplified)
        // TODO: Implement proper game result evaluation
        
        if ((i + 1) % 20 == 0) {
            std::cout << "Completed " << (i + 1) << " test games" << std::endl;
        }
    }
    
    results.stockfishWinRate = wins / config.numTestGames;
    results.estimatedELO = calculateELO(results.stockfishWinRate);
    
    std::cout << "vs Stockfish win rate: " << (results.stockfishWinRate * 100) << "%" << std::endl;
    std::cout << "Estimated ELO: " << results.estimatedELO << std::endl;
}

std::vector<float> Trainer::positionToFeatures(const Board& board) {
    std::vector<float> features(768, 0.0f);  // 8x8x12 = 768
    
    // Piece placement encoding
    for (int sq = 0; sq < 64; sq++) {
        PieceType piece = board.getPieceAt(sq);
        Color color = board.getColorAt(sq);
        
        if (piece == PieceType::NONE) continue;
        
        int pieceIndex = static_cast<int>(piece) - 1;  // 0-5
        int colorOffset = (color == Color::WHITE) ? 0 : 6;
        int featureIndex = sq * 12 + colorOffset + pieceIndex;
        
        features[featureIndex] = 1.0f;
    }
    
    return features;
}

float Trainer::evaluatePosition(const Board& board) {
    std::vector<float> features = positionToFeatures(board);
    return network.evaluate(features);
}

float Trainer::playGame(bool useNeuralNetwork, int timePerMove) {
    Board board;
    board.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    
    MoveGenerator moveGen;
    int moveCount = 0;
    
    while (moveCount < 200) {  // Max 200 moves
        std::vector<Move> moves = moveGen.generateLegalMoves(board);
        if (moves.empty()) break;
        
        Move move;
        if (useNeuralNetwork) {
            // Use neural network to select move
            float bestEval = -2;
            Move bestMove = moves[0];
            
            for (const Move& m : moves) {
                board.makeMove(m);
                std::vector<float> features = positionToFeatures(board);
                float eval = network.evaluate(features);
                if (eval > bestEval) {
                    bestEval = eval;
                    bestMove = m;
                }
                board.unmakeMove(m);
            }
            move = bestMove;
        } else {
            // Random move
            move = moves[rand() % moves.size()];
        }
        
        board.makeMove(move);
        moveCount++;
    }
    
    // Return 1.0 for win, 0.5 for draw, 0.0 for loss
    // TODO: Implement proper game result evaluation
    return 0.5f;
}

float Trainer::calculateELO(float winRate) {
    // ELO calculation: ELO = 2400 + 400 * log10(winRate / (1 - winRate))
    if (winRate <= 0 || winRate >= 1) return 2400;
    return 2400 + 400 * std::log10(winRate / (1 - winRate));
}

bool Trainer::shouldStopEarly(float currentValidationLoss) {
    if (currentValidationLoss < bestValidationLoss - config.overfitting.minValidationImprovement) {
        bestValidationLoss = currentValidationLoss;
        epochsSinceImprovement = 0;
        return false;
    }
    
    epochsSinceImprovement++;
    return epochsSinceImprovement >= config.overfitting.patienceEpochs;
}

void Trainer::applyDropout(std::vector<float>& features) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    
    float dropoutRate = config.overfitting.dropoutRate;
    for (auto& feature : features) {
        if (dis(gen) < dropoutRate) {
            feature = 0.0f;  // Drop this feature
        } else {
            feature /= (1.0f - dropoutRate);  // Scale remaining features
        }
    }
}

void Trainer::augmentTrainingData() {
    std::cout << "Augmenting training data..." << std::endl;
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    
    int originalSize = trainingData.size();
    int augmentCount = originalSize * config.overfitting.augmentationRate;
    
    for (int i = 0; i < augmentCount; i++) {
        int idx = i % originalSize;
        Position augmented = trainingData[idx];
        
        // Add small noise to evaluation
        float noise = (dis(gen) - 0.5f) * 10.0f;  // ±5 centipawn noise
        augmented.evaluation += noise;
        
        trainingData.push_back(augmented);
    }
    
    std::cout << "Augmented " << augmentCount << " positions" << std::endl;
}

void Trainer::saveCheckpoint(int epoch) {
    std::string checkpointPath = config.checkpointDir + "/checkpoint_epoch_" + std::to_string(epoch) + ".bin";
    saveModel(checkpointPath);
    std::cout << "✓ Checkpoint saved: epoch " << epoch << std::endl;
}

bool Trainer::loadCheckpoint() {
    // Find latest checkpoint
    int latestEpoch = 0;
    std::string latestCheckpoint;
    
    for (const auto& entry : fs::directory_iterator(config.checkpointDir)) {
        if (entry.path().extension() == ".bin") {
            std::string filename = entry.path().filename().string();
            if (filename.find("checkpoint_epoch_") == 0) {
                int epoch = std::stoi(filename.substr(17));  // Extract epoch number
                if (epoch > latestEpoch) {
                    latestEpoch = epoch;
                    latestCheckpoint = entry.path().string();
                }
            }
        }
    }
    
    if (latestEpoch > 0) {
        loadModel(latestCheckpoint);
        results.epochsCompleted = latestEpoch;
        return true;
    }
    
    return false;
}

bool Trainer::hasTimeRemaining() {
    if (!config.isCloudDeployment) return true;
    
    auto now = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::hours>(now - trainingStartTime);
    
    return elapsed.count() < config.maxTrainingHours;
}


void Trainer::saveModel(const std::string& path) {
    network.saveWeights(path);
    std::cout << "✓ Model saved to " << path << std::endl;
}

void Trainer::loadModel(const std::string& path) {
    network.loadWeights(path);
    std::cout << "✓ Model loaded from " << path << std::endl;
}
