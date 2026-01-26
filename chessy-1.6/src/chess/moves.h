#pragma once

#include "board.h"
#include <vector>

class MoveGenerator {
public:
    // Generate all legal moves
    std::vector<Move> generateLegalMoves(Board& board);
    
    // Generate all pseudo-legal moves (doesn't check for check)
    std::vector<Move> generatePseudoLegalMoves(const Board& board);
    
    // Check if a move is legal
    bool isLegalMove(Board& board, const Move& move);
    
private:
    // Generate moves for each piece type
    std::vector<Move> generatePawnMoves(const Board& board, Color color);
    std::vector<Move> generateKnightMoves(const Board& board, Color color);
    std::vector<Move> generateBishopMoves(const Board& board, Color color);
    std::vector<Move> generateRookMoves(const Board& board, Color color);
    std::vector<Move> generateQueenMoves(const Board& board, Color color);
    std::vector<Move> generateKingMoves(const Board& board, Color color);
    
    // Sliding piece moves
    std::vector<Move> generateSlidingMoves(const Board& board, Color color, 
                                          PieceType piece, const int* directions, int numDirections);
    
    // Helper functions
    bool isSquareEmpty(const Board& board, Square sq) const;
    bool isEnemyPiece(const Board& board, Square sq, Color color) const;
    bool isOwnPiece(const Board& board, Square sq, Color color) const;
};
