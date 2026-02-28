#include "board.h"
#include <iostream>
#include <sstream>
#include <algorithm>

Board::Board() : turn(Color::WHITE), enPassantSquare(64), halfmoveClock(0), fullmoveNumber(1) {
    clearBoard();
    // Initialize castling rights
    castleRights[0][0] = castleRights[0][1] = true;  // White
    castleRights[1][0] = castleRights[1][1] = true;  // Black
}

void Board::clearBoard() {
    for (int c = 0; c < 2; c++) {
        for (int p = 0; p < 7; p++) {
            pieces[c][p] = 0;
        }
    }
}

void Board::setSquare(Square sq, Color color, PieceType type) {
    pieces[static_cast<int>(color)][static_cast<int>(type)] |= (1ULL << sq);
}

void Board::clearSquare(Square sq) {
    for (int c = 0; c < 2; c++) {
        for (int p = 0; p < 7; p++) {
            pieces[c][p] &= ~(1ULL << sq);
        }
    }
}

void Board::fromFEN(const std::string& fen) {
    clearBoard();
    
    std::istringstream ss(fen);
    std::string board, turn_str, castling, enpassant, halfmove, fullmove;
    
    ss >> board >> turn_str >> castling >> enpassant >> halfmove >> fullmove;
    
    // Parse board
    int sq = 56;  // Start from a8
    for (char c : board) {
        if (c == '/') {
            sq -= 16;  // Move to next rank
        } else if (isdigit(c)) {
            sq += (c - '0');  // Skip empty squares
        } else {
            Color color = isupper(c) ? Color::WHITE : Color::BLACK;
            PieceType type;
            
            switch (tolower(c)) {
                case 'p': type = PieceType::PAWN; break;
                case 'n': type = PieceType::KNIGHT; break;
                case 'b': type = PieceType::BISHOP; break;
                case 'r': type = PieceType::ROOK; break;
                case 'q': type = PieceType::QUEEN; break;
                case 'k': type = PieceType::KING; break;
                default: continue;
            }
            
            setSquare(sq, color, type);
            sq++;
        }
    }
    
    // Parse turn
    turn = (turn_str == "w") ? Color::WHITE : Color::BLACK;
    
    // Parse castling rights
    castleRights[0][0] = castleRights[0][1] = false;
    castleRights[1][0] = castleRights[1][1] = false;
    
    for (char c : castling) {
        if (c == 'K') castleRights[0][0] = true;
        if (c == 'Q') castleRights[0][1] = true;
        if (c == 'k') castleRights[1][0] = true;
        if (c == 'q') castleRights[1][1] = true;
    }
    
    // Parse en passant
    if (enpassant != "-") {
        int file = enpassant[0] - 'a';
        int rank = enpassant[1] - '1';
        enPassantSquare = rank * 8 + file;
    } else {
        enPassantSquare = 64;
    }
    
    // Parse move counters
    halfmoveClock = std::stoi(halfmove);
    fullmoveNumber = std::stoi(fullmove);
}

std::string Board::toFEN() const {
    std::string fen;
    
    // Board position
    for (int rank = 7; rank >= 0; rank--) {
        int empty = 0;
        for (int file = 0; file < 8; file++) {
            Square sq = rank * 8 + file;
            PieceType type = getPieceAt(sq);
            
            if (type == PieceType::NONE) {
                empty++;
            } else {
                if (empty > 0) {
                    fen += std::to_string(empty);
                    empty = 0;
                }
                
                Color color = getColorAt(sq);
                char piece;
                switch (type) {
                    case PieceType::PAWN: piece = 'p'; break;
                    case PieceType::KNIGHT: piece = 'n'; break;
                    case PieceType::BISHOP: piece = 'b'; break;
                    case PieceType::ROOK: piece = 'r'; break;
                    case PieceType::QUEEN: piece = 'q'; break;
                    case PieceType::KING: piece = 'k'; break;
                    default: piece = '?';
                }
                
                if (color == Color::WHITE) piece = toupper(piece);
                fen += piece;
            }
        }
        
        if (empty > 0) fen += std::to_string(empty);
        if (rank > 0) fen += '/';
    }
    
    fen += ' ';
    fen += (turn == Color::WHITE) ? 'w' : 'b';
    fen += ' ';
    
    // Castling rights
    bool hasCastling = false;
    if (castleRights[0][0]) { fen += 'K'; hasCastling = true; }
    if (castleRights[0][1]) { fen += 'Q'; hasCastling = true; }
    if (castleRights[1][0]) { fen += 'k'; hasCastling = true; }
    if (castleRights[1][1]) { fen += 'q'; hasCastling = true; }
    if (!hasCastling) fen += '-';
    
    fen += ' ';
    
    // En passant
    if (enPassantSquare < 64) {
        fen += char('a' + (enPassantSquare % 8));
        fen += char('1' + (enPassantSquare / 8));
    } else {
        fen += '-';
    }
    
    fen += ' ' + std::to_string(halfmoveClock);
    fen += ' ' + std::to_string(fullmoveNumber);
    
    return fen;
}

Bitboard Board::getPieces(Color color, PieceType type) const {
    return pieces[static_cast<int>(color)][static_cast<int>(type)];
}

Bitboard Board::getOccupancy(Color color) const {
    Bitboard occ = 0;
    for (int p = 1; p < 7; p++) {
        occ |= pieces[static_cast<int>(color)][p];
    }
    return occ;
}

Bitboard Board::getOccupancy() const {
    return getOccupancy(Color::WHITE) | getOccupancy(Color::BLACK);
}

PieceType Board::getPieceAt(Square sq) const {
    for (int p = 1; p < 7; p++) {
        for (int c = 0; c < 2; c++) {
            if (pieces[c][p] & (1ULL << sq)) {
                return static_cast<PieceType>(p);
            }
        }
    }
    return PieceType::NONE;
}

Color Board::getColorAt(Square sq) const {
    for (int c = 0; c < 2; c++) {
        for (int p = 1; p < 7; p++) {
            if (pieces[c][p] & (1ULL << sq)) {
                return static_cast<Color>(c);
            }
        }
    }
    return Color::WHITE;  // Default
}

void Board::makeMove(const Move& move) {
    // Store history
    MoveHistory hist;
    hist.move = move;
    hist.capturedPiece = 0;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            hist.castleRights[i][j] = castleRights[i][j];
        }
    }
    hist.enPassantSquare = enPassantSquare;
    hist.halfmoveClock = halfmoveClock;
    
    // Get piece being moved
    PieceType piece = getPieceAt(move.from);
    Color color = getColorAt(move.from);
    
    // Handle capture
    PieceType captured = getPieceAt(move.to);
    if (captured != PieceType::NONE) {
        hist.capturedPiece = 1ULL << move.to;
        clearSquare(move.to);
        halfmoveClock = 0;
    } else {
        halfmoveClock++;
    }
    
    // Move piece
    clearSquare(move.from);
    setSquare(move.to, color, piece);
    
    // Handle pawn moves
    if (piece == PieceType::PAWN) {
        halfmoveClock = 0;
        
        // Promotion
        if (move.promotion != PieceType::NONE) {
            clearSquare(move.to);
            setSquare(move.to, color, move.promotion);
        }
        
        // En passant capture
        if (move.to == enPassantSquare) {
            Square capturedSq = (color == Color::WHITE) ? move.to - 8 : move.to + 8;
            clearSquare(capturedSq);
        }
        
        // Set en passant square
        if (abs(move.to - move.from) == 16) {
            enPassantSquare = (move.from + move.to) / 2;
        } else {
            enPassantSquare = 64;
        }
    } else {
        enPassantSquare = 64;
    }
    
    // Handle castling
    if (piece == PieceType::KING) {
        castleRights[static_cast<int>(color)][0] = false;
        castleRights[static_cast<int>(color)][1] = false;
        
        // Move rook for castling
        if (move.from == (color == Color::WHITE ? 4 : 60)) {
            if (move.to == (color == Color::WHITE ? 6 : 62)) {  // Kingside
                Square rookFrom = color == Color::WHITE ? 7 : 63;
                Square rookTo = color == Color::WHITE ? 5 : 61;
                clearSquare(rookFrom);
                setSquare(rookTo, color, PieceType::ROOK);
            } else if (move.to == (color == Color::WHITE ? 2 : 58)) {  // Queenside
                Square rookFrom = color == Color::WHITE ? 0 : 56;
                Square rookTo = color == Color::WHITE ? 3 : 59;
                clearSquare(rookFrom);
                setSquare(rookTo, color, PieceType::ROOK);
            }
        }
    }
    
    // Update castling rights if rook moves
    if (piece == PieceType::ROOK) {
        if (move.from == (color == Color::WHITE ? 7 : 63)) {
            castleRights[static_cast<int>(color)][0] = false;
        } else if (move.from == (color == Color::WHITE ? 0 : 56)) {
            castleRights[static_cast<int>(color)][1] = false;
        }
    }
    
    // Switch turn
    turn = (turn == Color::WHITE) ? Color::BLACK : Color::WHITE;
    if (turn == Color::WHITE) fullmoveNumber++;
    
    history.push_back(hist);
}

void Board::unmakeMove(const Move& move) {
    if (history.empty()) return;
    
    MoveHistory hist = history.back();
    history.pop_back();
    
    // Restore state
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            castleRights[i][j] = hist.castleRights[i][j];
        }
    }
    enPassantSquare = hist.enPassantSquare;
    halfmoveClock = hist.halfmoveClock;
    
    // Switch turn back
    turn = (turn == Color::WHITE) ? Color::BLACK : Color::WHITE;
    if (turn == Color::BLACK) fullmoveNumber--;
    
    // Move piece back
    PieceType piece = getPieceAt(move.to);
    Color color = getColorAt(move.to);
    
    clearSquare(move.to);
    setSquare(move.from, color, piece);
    
    // Restore captured piece
    if (hist.capturedPiece != 0) {
        for (int sq = 0; sq < 64; sq++) {
            if (hist.capturedPiece & (1ULL << sq)) {
                // Determine captured piece type
                PieceType capturedType = getPieceAt(sq);
                setSquare(sq, (color == Color::WHITE) ? Color::BLACK : Color::WHITE, capturedType);
            }
        }
    }
}

bool Board::isInCheck(Color color) const {
    // Find king
    Bitboard king = getPieces(color, PieceType::KING);
    if (king == 0) return false;
    
    Square kingSq = 0;
    for (int i = 0; i < 64; i++) {
        if (king & (1ULL << i)) {
            kingSq = i;
            break;
        }
    }
    
    // Check if attacked by opponent
    Color opponent = (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
    return isSquareAttacked(kingSq, opponent);
}

bool Board::isSquareAttacked(Square sq, Color byColor) const {
    // Check pawn attacks
    int direction = (byColor == Color::WHITE) ? 8 : -8;
    if ((sq + direction + 1 < 64) && getPieceAt(sq + direction + 1) == PieceType::PAWN &&
        getColorAt(sq + direction + 1) == byColor) return true;
    if ((sq + direction - 1 >= 0) && getPieceAt(sq + direction - 1) == PieceType::PAWN &&
        getColorAt(sq + direction - 1) == byColor) return true;
    
    // Check knight attacks
    int knightMoves[] = {-17, -15, -10, -6, 6, 10, 15, 17};
    for (int move : knightMoves) {
        int target = sq + move;
        if (target >= 0 && target < 64 && getPieceAt(target) == PieceType::KNIGHT &&
            getColorAt(target) == byColor) return true;
    }
    
    // TODO: Check sliding pieces (bishop, rook, queen)
    // TODO: Check king attacks
    
    return false;
}

bool Board::isCheckmate(Color color) const {
    if (!isInCheck(color)) return false;
    // TODO: Check if any legal moves exist
    return true;
}

bool Board::isStalemate(Color color) const {
    if (isInCheck(color)) return false;
    // TODO: Check if any legal moves exist
    return true;
}

void Board::print() const {
    std::cout << "\n  a b c d e f g h\n";
    for (int rank = 7; rank >= 0; rank--) {
        std::cout << rank + 1 << " ";
        for (int file = 0; file < 8; file++) {
            Square sq = rank * 8 + file;
            PieceType type = getPieceAt(sq);
            Color color = getColorAt(sq);
            
            if (type == PieceType::NONE) {
                std::cout << ". ";
            } else {
                char piece;
                switch (type) {
                    case PieceType::PAWN: piece = 'P'; break;
                    case PieceType::KNIGHT: piece = 'N'; break;
                    case PieceType::BISHOP: piece = 'B'; break;
                    case PieceType::ROOK: piece = 'R'; break;
                    case PieceType::QUEEN: piece = 'Q'; break;
                    case PieceType::KING: piece = 'K'; break;
                    default: piece = '?';
                }
                
                if (color == Color::BLACK) piece = tolower(piece);
                std::cout << piece << " ";
            }
        }
        std::cout << rank + 1 << "\n";
    }
    std::cout << "  a b c d e f g h\n\n";
}


// Castling rights
bool Board::canCastleKingside(Color color) const {
    return castleRights[static_cast<int>(color)][0];
}

bool Board::canCastleQueenside(Color color) const {
    return castleRights[static_cast<int>(color)][1];
}
