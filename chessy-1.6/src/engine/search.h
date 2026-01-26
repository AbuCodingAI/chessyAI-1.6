#pragma once

#include "../chess/board.h"
#include "evaluator.h"

class Search {
public:
    Search(Evaluator* evaluator);
    
    // Find best move
    Move findBestMove(Board& board, int depth, int timeLimit = 0);
    
    // Alpha-beta search
    float alphaBeta(Board& board, int depth, float alpha, float beta, bool maximizing);
    
    // Smart quiescence search (15 moves + 2 after capture sequence)
    float smartQuiescence(Board& board, float alpha, float beta, int depth = 0, int maxDepth = 15);
    
    // Check if in capture sequence
    bool isInCaptureSequence(Board& board, const Move& move);
    
private:
    Evaluator* evaluator;
    int nodesSearched;
    static const int MAX_QUIESCENCE_DEPTH = 15;
    static const int CAPTURE_EXTENSION = 2;
};
