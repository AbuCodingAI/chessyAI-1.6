#include "position.h"

Position::Position(const Board& board) : board(board) {}

int Position::getMaterialCount(Color color) const {
    // Helper lambda for popcount (portable)
    auto popcount = [](Bitboard b) {
        int count = 0;
        while (b) {
            count += b & 1;
            b >>= 1;
        }
        return count;
    };
    
    int material = 0;
    material += popcount(board.getPieces(color, PieceType::PAWN)) * 1;
    material += popcount(board.getPieces(color, PieceType::KNIGHT)) * 3;
    material += popcount(board.getPieces(color, PieceType::BISHOP)) * 3;
    material += popcount(board.getPieces(color, PieceType::ROOK)) * 5;
    material += popcount(board.getPieces(color, PieceType::QUEEN)) * 9;
    return material;
}

float Position::getPieceActivity(Color /*color*/) const {
    // TODO: Implement piece activity evaluation
    return 0.0f;
}

float Position::getKingSafety(Color /*color*/) const {
    // TODO: Implement king safety evaluation
    return 0.0f;
}

float Position::getPawnStructure(Color /*color*/) const {
    // TODO: Implement pawn structure evaluation
    return 0.0f;
}
