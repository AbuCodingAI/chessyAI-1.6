#pragma once

#include "../chess/board.h"
#include <string>
#include <vector>

struct Position {
    std::string fen;
    float evaluation;  // From Stockfish
    bool isBlunder;    // 5% of positions
};

class StockfishInterface {
public:
    StockfishInterface(const std::string& stockfishPath);
    ~StockfishInterface();
    
    // Get best move from Stockfish
    Move getBestMove(const std::string& fen, int depth);
    
    // Get evaluation from Stockfish
    float getEvaluation(const std::string& fen, int depth);
    
    // Generate training data
    std::vector<Position> generateTrainingData(int numGames, int depth, float blunderRate = 0.05f);
    
    // Get blunder move (5% of the time)
    Move getBlunderMove(const std::string& fen);
    
    // Check if Stockfish is running
    bool isRunning() const;
    
private:
    std::string stockfishPath;
    void* process;  // Platform-specific process handle
    
    // Communication
    void sendCommand(const std::string& command);
    std::string readOutput();
    
    // Parse Stockfish output
    Move parseBestMove(const std::string& output);
    float parseEvaluation(const std::string& output);
};
