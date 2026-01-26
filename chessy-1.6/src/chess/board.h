#pragma once

#include <cstdint>
#include <string>
#include <vector>

// Piece types
enum class PieceType : uint8_t {
    NONE = 0,
    PAWN = 1,
    KNIGHT = 2,
    BISHOP = 3,
    ROOK = 4,
    QUEEN = 5,
    KING = 6
};

// Colors
enum class Color : uint8_t {
    WHITE = 0,
    BLACK = 1
};

// Squares (0-63, a1=0, h8=63)
using Square = uint8_t;

// Move representation
struct Move {
    Square from;
    Square to;
    PieceType promotion;  // For pawn promotion
    
    Move() : from(0), to(0), promotion(PieceType::NONE) {}
    Move(Square f, Square t, PieceType p = PieceType::NONE) 
        : from(f), to(t), promotion(p) {}
};

// Bitboard (64-bit representation of board)
using Bitboard = uint64_t;

class Board {
public:
    Board();
    
    // Initialize from FEN
    void fromFEN(const std::string& fen);
    std::string toFEN() const;
    
    // Board state
    Bitboard getPieces(Color color, PieceType type) const;
    Bitboard getOccupancy(Color color) const;
    Bitboard getOccupancy() const;
    
    PieceType getPieceAt(Square sq) const;
    Color getColorAt(Square sq) const;
    
    // Move operations
    void makeMove(const Move& move);
    void unmakeMove(const Move& move);
    
    // Game state
    Color getTurn() const { return turn; }
    bool canCastleKingside(Color color) const;
    bool canCastleQueenside(Color color) const;
    Square getEnPassantSquare() const { return enPassantSquare; }
    
    // Checks
    bool isInCheck(Color color) const;
    bool isCheckmate(Color color) const;
    bool isStalemate(Color color) const;
    
    // Display
    void print() const;
    
private:
    // Bitboards for each piece type and color
    Bitboard pieces[2][7];  // [color][piece_type]
    
    // Game state
    Color turn;
    bool castleRights[2][2];  // [color][kingside/queenside]
    Square enPassantSquare;
    int halfmoveClock;
    int fullmoveNumber;
    
    // Move history for undo
    struct MoveHistory {
        Move move;
        Bitboard capturedPiece;
        bool castleRights[2][2];
        Square enPassantSquare;
        int halfmoveClock;
    };
    std::vector<MoveHistory> history;
    
    // Helper functions
    void clearBoard();
    void setSquare(Square sq, Color color, PieceType type);
    void clearSquare(Square sq);
    bool isSquareAttacked(Square sq, Color byColor) const;
};
