#include "rules.h"
#include "moves.h"

bool ChessRules::isValidMove(Board& board, const Move& move) {
    MoveGenerator gen;
    std::vector<Move> legalMoves = gen.generateLegalMoves(board);
    
    for (const Move& m : legalMoves) {
        if (m.from == move.from && m.to == move.to && m.promotion == move.promotion) {
            return true;
        }
    }
    return false;
}

bool ChessRules::isValidCastling(const Board& board, const Move& move) {
    Color color = board.getColorAt(move.from);
    PieceType piece = board.getPieceAt(move.from);
    
    if (piece != PieceType::KING) return false;
    
    // Kingside castling
    if (move.to == (color == Color::WHITE ? 6 : 62)) {
        return board.canCastleKingside(color);
    }
    
    // Queenside castling
    if (move.to == (color == Color::WHITE ? 2 : 58)) {
        return board.canCastleQueenside(color);
    }
    
    return false;
}

bool ChessRules::isValidEnPassant(const Board& board, const Move& move) {
    PieceType piece = board.getPieceAt(move.from);
    if (piece != PieceType::PAWN) return false;
    
    return move.to == board.getEnPassantSquare();
}

bool ChessRules::isValidPromotion(const Board& board, const Move& move) {
    PieceType piece = board.getPieceAt(move.from);
    if (piece != PieceType::PAWN) return false;
    
    Color color = board.getColorAt(move.from);
    int promotionRank = (color == Color::WHITE) ? 56 : 0;
    
    return move.to >= promotionRank && move.to < promotionRank + 8;
}

bool ChessRules::isCheckmate(Board& board) {
    return board.isCheckmate(board.getTurn());
}

bool ChessRules::isStalemate(Board& board) {
    return board.isStalemate(board.getTurn());
}

bool ChessRules::isThreefoldRepetition(const Board& /*board*/) {
    // TODO: Implement threefold repetition check
    return false;
}

bool ChessRules::isFiftyMoveRule(const Board& /*board*/) {
    // TODO: Implement fifty move rule check
    return false;
}
