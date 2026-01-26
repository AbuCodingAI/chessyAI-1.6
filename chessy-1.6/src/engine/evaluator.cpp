#include "evaluator.h"
#include <vector>

Evaluator::Evaluator(NeuralNetwork* network) : network(network) {}

float Evaluator::evaluate(const Board& board) {
    if (network) {
        // Use neural network evaluation
        std::vector<float> features(768, 0.0f);
        
        for (int sq = 0; sq < 64; sq++) {
            PieceType piece = board.getPieceAt(sq);
            Color color = board.getColorAt(sq);
            
            if (piece == PieceType::NONE) continue;
            
            int pieceIndex = static_cast<int>(piece) - 1;
            int colorOffset = (color == Color::WHITE) ? 0 : 6;
            int featureIndex = sq * 12 + colorOffset + pieceIndex;
            
            features[featureIndex] = 1.0f;
        }
        
        return network->evaluate(features);
    } else {
        return staticEvaluate(board);
    }
}

float Evaluator::staticEvaluate(const Board& board) {
    float eval = 0;
    eval += evaluateMaterial(board);
    eval += evaluatePieceActivity(board);
    eval += evaluateKingSafety(board);
    eval += evaluatePawnStructure(board);
    return eval;
}

float Evaluator::evaluateMaterial(const Board& board) {
    float eval = 0;
    
    // Material values
    int pawnValue = 1;
    int knightValue = 3;
    int bishopValue = 3;
    int rookValue = 5;
    int queenValue = 9;
    
    // White material
    eval += __builtin_popcountll(board.getPieces(Color::WHITE, PieceType::PAWN)) * pawnValue;
    eval += __builtin_popcountll(board.getPieces(Color::WHITE, PieceType::KNIGHT)) * knightValue;
    eval += __builtin_popcountll(board.getPieces(Color::WHITE, PieceType::BISHOP)) * bishopValue;
    eval += __builtin_popcountll(board.getPieces(Color::WHITE, PieceType::ROOK)) * rookValue;
    eval += __builtin_popcountll(board.getPieces(Color::WHITE, PieceType::QUEEN)) * queenValue;
    
    // Black material
    eval -= __builtin_popcountll(board.getPieces(Color::BLACK, PieceType::PAWN)) * pawnValue;
    eval -= __builtin_popcountll(board.getPieces(Color::BLACK, PieceType::KNIGHT)) * knightValue;
    eval -= __builtin_popcountll(board.getPieces(Color::BLACK, PieceType::BISHOP)) * bishopValue;
    eval -= __builtin_popcountll(board.getPieces(Color::BLACK, PieceType::ROOK)) * rookValue;
    eval -= __builtin_popcountll(board.getPieces(Color::BLACK, PieceType::QUEEN)) * queenValue;
    
    return eval / 100.0f;  // Normalize
}

float Evaluator::evaluatePieceActivity(const Board& board) {
    // TODO: Implement piece activity evaluation
    return 0.0f;
}

float Evaluator::evaluateKingSafety(const Board& board) {
    // TODO: Implement king safety evaluation
    return 0.0f;
}

float Evaluator::evaluatePawnStructure(const Board& board) {
    // TODO: Implement pawn structure evaluation
    return 0.0f;
}
