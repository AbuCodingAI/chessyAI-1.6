#include "moves.h"
#include <algorithm>

std::vector<Move> MoveGenerator::generateLegalMoves(Board& board) {
    std::vector<Move> pseudoLegal = generatePseudoLegalMoves(board);
    std::vector<Move> legal;
    
    Color currentColor = board.getTurn();
    Color opponentColor = (currentColor == Color::WHITE) ? Color::BLACK : Color::WHITE;
    
    for (const Move& move : pseudoLegal) {
        board.makeMove(move);
        
        // After move, check if our king is in check
        // The turn has switched, so we check if the previous player's king is in check
        bool kingInCheck = board.isInCheck(currentColor);
        
        board.unmakeMove(move);
        
        // Only add move if it doesn't leave our king in check
        if (!kingInCheck) {
            legal.push_back(move);
        }
    }
    
    return legal;
}

std::vector<Move> MoveGenerator::generatePseudoLegalMoves(const Board& board) {
    std::vector<Move> moves;
    Color color = board.getTurn();
    
    // Generate moves for each piece type
    auto pawnMoves = generatePawnMoves(board, color);
    auto knightMoves = generateKnightMoves(board, color);
    auto bishopMoves = generateBishopMoves(board, color);
    auto rookMoves = generateRookMoves(board, color);
    auto queenMoves = generateQueenMoves(board, color);
    auto kingMoves = generateKingMoves(board, color);
    
    moves.insert(moves.end(), pawnMoves.begin(), pawnMoves.end());
    moves.insert(moves.end(), knightMoves.begin(), knightMoves.end());
    moves.insert(moves.end(), bishopMoves.begin(), bishopMoves.end());
    moves.insert(moves.end(), rookMoves.begin(), rookMoves.end());
    moves.insert(moves.end(), queenMoves.begin(), queenMoves.end());
    moves.insert(moves.end(), kingMoves.begin(), kingMoves.end());
    
    return moves;
}

bool MoveGenerator::isLegalMove(Board& board, const Move& move) {
    board.makeMove(move);
    Color opponent = board.getTurn();
    bool legal = !board.isInCheck(opponent);
    board.unmakeMove(move);
    return legal;
}

std::vector<Move> MoveGenerator::generatePawnMoves(const Board& board, Color color) {
    std::vector<Move> moves;
    Bitboard pawns = board.getPieces(color, PieceType::PAWN);
    
    int forward = (color == Color::WHITE) ? 8 : -8;
    int startRank = (color == Color::WHITE) ? 8 : 48;
    int promotionRank = (color == Color::WHITE) ? 56 : 0;
    
    for (int sq = 0; sq < 64; sq++) {
        if (!(pawns & (1ULL << sq))) continue;
        
        // Forward move
        int target = sq + forward;
        if (target >= 0 && target < 64 && isSquareEmpty(board, target)) {
            if (target >= promotionRank && target < promotionRank + 8) {
                // Promotion
                moves.push_back(Move(sq, target, PieceType::QUEEN));
                moves.push_back(Move(sq, target, PieceType::ROOK));
                moves.push_back(Move(sq, target, PieceType::BISHOP));
                moves.push_back(Move(sq, target, PieceType::KNIGHT));
            } else {
                moves.push_back(Move(sq, target));
            }
            
            // Double move from start
            if (sq >= startRank && sq < startRank + 8) {
                int target2 = sq + 2 * forward;
                if (isSquareEmpty(board, target2)) {
                    moves.push_back(Move(sq, target2));
                }
            }
        }
        
        // Captures
        int captureLeft = sq + forward - 1;
        int captureRight = sq + forward + 1;
        
        if (captureLeft >= 0 && captureLeft < 64 && isEnemyPiece(board, captureLeft, color)) {
            if (captureLeft >= promotionRank && captureLeft < promotionRank + 8) {
                moves.push_back(Move(sq, captureLeft, PieceType::QUEEN));
                moves.push_back(Move(sq, captureLeft, PieceType::ROOK));
                moves.push_back(Move(sq, captureLeft, PieceType::BISHOP));
                moves.push_back(Move(sq, captureLeft, PieceType::KNIGHT));
            } else {
                moves.push_back(Move(sq, captureLeft));
            }
        }
        
        if (captureRight >= 0 && captureRight < 64 && isEnemyPiece(board, captureRight, color)) {
            if (captureRight >= promotionRank && captureRight < promotionRank + 8) {
                moves.push_back(Move(sq, captureRight, PieceType::QUEEN));
                moves.push_back(Move(sq, captureRight, PieceType::ROOK));
                moves.push_back(Move(sq, captureRight, PieceType::BISHOP));
                moves.push_back(Move(sq, captureRight, PieceType::KNIGHT));
            } else {
                moves.push_back(Move(sq, captureRight));
            }
        }
        
        // En passant
        Square epSq = board.getEnPassantSquare();
        if (epSq < 64) {
            if (captureLeft == epSq || captureRight == epSq) {
                moves.push_back(Move(sq, epSq));
            }
        }
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateKnightMoves(const Board& board, Color color) {
    std::vector<Move> moves;
    Bitboard knights = board.getPieces(color, PieceType::KNIGHT);
    
    int knightMoves[] = {-17, -15, -10, -6, 6, 10, 15, 17};
    
    for (int sq = 0; sq < 64; sq++) {
        if (!(knights & (1ULL << sq))) continue;
        
        for (int move : knightMoves) {
            int target = sq + move;
            if (target >= 0 && target < 64) {
                if (isSquareEmpty(board, target) || isEnemyPiece(board, target, color)) {
                    moves.push_back(Move(sq, target));
                }
            }
        }
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateBishopMoves(const Board& board, Color color) {
    int directions[] = {-9, -7, 7, 9};
    return generateSlidingMoves(board, color, PieceType::BISHOP, directions, 4);
}

std::vector<Move> MoveGenerator::generateRookMoves(const Board& board, Color color) {
    int directions[] = {-8, -1, 1, 8};
    return generateSlidingMoves(board, color, PieceType::ROOK, directions, 4);
}

std::vector<Move> MoveGenerator::generateQueenMoves(const Board& board, Color color) {
    int directions[] = {-9, -8, -7, -1, 1, 7, 8, 9};
    return generateSlidingMoves(board, color, PieceType::QUEEN, directions, 8);
}

std::vector<Move> MoveGenerator::generateSlidingMoves(const Board& board, Color color,
                                                      PieceType piece, const int* directions, int numDirections) {
    std::vector<Move> moves;
    Bitboard pieces = board.getPieces(color, piece);
    
    for (int sq = 0; sq < 64; sq++) {
        if (!(pieces & (1ULL << sq))) continue;
        
        for (int d = 0; d < numDirections; d++) {
            int target = sq + directions[d];
            
            while (target >= 0 && target < 64) {
                if (isSquareEmpty(board, target)) {
                    moves.push_back(Move(sq, target));
                } else if (isEnemyPiece(board, target, color)) {
                    moves.push_back(Move(sq, target));
                    break;
                } else {
                    break;
                }
                
                target += directions[d];
            }
        }
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateKingMoves(const Board& board, Color color) {
    std::vector<Move> moves;
    Bitboard king = board.getPieces(color, PieceType::KING);
    
    int kingMoves[] = {-9, -8, -7, -1, 1, 7, 8, 9};
    
    for (int sq = 0; sq < 64; sq++) {
        if (!(king & (1ULL << sq))) continue;
        
        // Regular king moves
        for (int move : kingMoves) {
            int target = sq + move;
            if (target >= 0 && target < 64) {
                if (isSquareEmpty(board, target) || isEnemyPiece(board, target, color)) {
                    moves.push_back(Move(sq, target));
                }
            }
        }
        
        // Castling
        if (color == Color::WHITE) {
            if (board.canCastleKingside(color) && isSquareEmpty(board, 5) && isSquareEmpty(board, 6)) {
                moves.push_back(Move(4, 6));
            }
            if (board.canCastleQueenside(color) && isSquareEmpty(board, 1) && 
                isSquareEmpty(board, 2) && isSquareEmpty(board, 3)) {
                moves.push_back(Move(4, 2));
            }
        } else {
            if (board.canCastleKingside(color) && isSquareEmpty(board, 61) && isSquareEmpty(board, 62)) {
                moves.push_back(Move(60, 62));
            }
            if (board.canCastleQueenside(color) && isSquareEmpty(board, 57) && 
                isSquareEmpty(board, 58) && isSquareEmpty(board, 59)) {
                moves.push_back(Move(60, 58));
            }
        }
    }
    
    return moves;
}

bool MoveGenerator::isSquareEmpty(const Board& board, Square sq) const {
    return board.getPieceAt(sq) == PieceType::NONE;
}

bool MoveGenerator::isEnemyPiece(const Board& board, Square sq, Color color) const {
    PieceType piece = board.getPieceAt(sq);
    if (piece == PieceType::NONE) return false;
    return board.getColorAt(sq) != color;
}

bool MoveGenerator::isOwnPiece(const Board& board, Square sq, Color color) const {
    PieceType piece = board.getPieceAt(sq);
    if (piece == PieceType::NONE) return false;
    return board.getColorAt(sq) == color;
}
