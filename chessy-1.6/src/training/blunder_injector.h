#pragma once

#include "../chess/board.h"
#include <vector>

class BlunderInjector {
public:
    // Inject blunders into positions (5% of the time)
    static Move injectBlunder(const Board& board, const std::vector<Move>& legalMoves, float blunderRate = 0.05f);
    
    // Detect if a move is a blunder
    static bool isBlunder(const Board& board, const Move& move, float threshold = -2.0f);
    
private:
    // Select a random move
    static Move selectRandomMove(const std::vector<Move>& moves);
};
