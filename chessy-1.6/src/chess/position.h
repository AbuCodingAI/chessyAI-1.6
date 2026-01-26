#pragma once

#include "board.h"

class Position {
public:
    Position(const Board& board);
    
    // Material count
    int getMaterialCount(Color color) const;
    
    // Piece activity
    float getPieceActivity(Color color) const;
    
    // King safety
    float getKingSafety(Color color) const;
    
    // Pawn structure
    float getPawnStructure(Color color) const;
    
private:
    const Board& board;
};
