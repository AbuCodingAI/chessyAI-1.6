#include "blunder_injector.h"
#include <random>

Move BlunderInjector::injectBlunder(const Board& /*board*/, const std::vector<Move>& legalMoves, float blunderRate) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    
    if (dis(gen) < blunderRate && legalMoves.size() > 1) {
        // Select a random move (likely a blunder)
        return selectRandomMove(legalMoves);
    }
    
    // Return first move (best move)
    return legalMoves[0];
}

bool BlunderInjector::isBlunder(const Board& /*board*/, const Move& /*move*/, float /*threshold*/) {
    // TODO: Implement blunder detection
    return false;
}

Move BlunderInjector::selectRandomMove(const std::vector<Move>& moves) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, moves.size() - 1);
    
    return moves[dis(gen)];
}
