#pragma once

#include "../chess/board.h"
#include "../neural/network.h"

class Evaluator {
public:
    Evaluator(NeuralNetwork* network);
    
    // Evaluate position
    float evaluate(const Board& board);
    
    // Static evaluation (without neural network)
    float staticEvaluate(const Board& board);
    
private:
    NeuralNetwork* network;
    
    // Evaluation components
    float evaluateMaterial(const Board& board);
    float evaluatePieceActivity(const Board& board);
    float evaluateKingSafety(const Board& board);
    float evaluatePawnStructure(const Board& board);
};
