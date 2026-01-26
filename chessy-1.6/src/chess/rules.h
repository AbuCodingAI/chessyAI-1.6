#pragma once

#include "board.h"

class ChessRules {
public:
    // Validate move according to chess rules
    static bool isValidMove(Board& board, const Move& move);
    
    // Check specific rules
    static bool isValidCastling(const Board& board, const Move& move);
    static bool isValidEnPassant(const Board& board, const Move& move);
    static bool isValidPromotion(const Board& board, const Move& move);
    
    // Game state
    static bool isCheckmate(Board& board);
    static bool isStalemate(Board& board);
    static bool isThreefoldRepetition(const Board& board);
    static bool isFiftyMoveRule(const Board& board);
};
