#include "position.h"

Position::Position(const Board& board) : board(board) {}

int Position::getMaterialCount(Color color) const {
    int material = 0;
    material += __builtin_popcountll(board.getPieces(color, PieceType::PAWN)) * 1;
    material += __builtin_popcountll(board.getPieces(color, PieceType::KNIGHT)) * 3;
    material += __builtin_popcountll(board.getPieces(color, PieceType::BISHOP)) * 3;
    material += __builtin_popcountll(board.getPieces(color, PieceType::ROOK)) * 5;
    material += __builtin_popcountll(board.getPieces(color, PieceType::QUEEN)) * 9;
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
