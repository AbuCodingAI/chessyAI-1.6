#include <iostream>
#include <string>
#include <vector>
#include "chess/board.h"
#include "chess/moves.h"
#include "training/trainer.h"
#include "engine/search.h"
#include "engine/evaluator.h"

void printUsage() {
    std::cout << "Chessy 1.6 - C++ Neural Chess Engine\n\n";
    std::cout << "Usage:\n";
    std::cout << "  chessy-1.6 --train              Train the neural network\n";
    std::cout << "  chessy-1.6 --play               Play interactive chess\n";
    std::cout << "  chessy-1.6 --test               Test vs Stockfish\n";
    std::cout << "  chessy-1.6 --generate-data      Generate training data\n";
    std::cout << "  chessy-1.6 --help               Show this help message\n";
}

void playInteractive() {
    std::cout << "=== Chessy 1.6 Interactive Mode ===" << std::endl;
    
    Board board;
    board.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    
    MoveGenerator moveGen;
    NeuralNetwork network({768, 512, 256, 128, 1});
    Evaluator evaluator(&network);
    Search search(&evaluator);
    
    int moveCount = 0;
    while (moveCount < 200) {
        board.print();
        
        std::vector<Move> moves = moveGen.generateLegalMoves(board);
        if (moves.empty()) {
            if (board.isInCheck(board.getTurn())) {
                std::cout << "Checkmate!" << std::endl;
            } else {
                std::cout << "Stalemate!" << std::endl;
            }
            break;
        }
        
        if (board.getTurn() == Color::WHITE) {
            // Human move
            std::cout << "Enter your move (e.g., e2e4): ";
            std::string moveStr;
            std::cin >> moveStr;
            
            if (moveStr.length() < 4) {
                std::cout << "Invalid move format!" << std::endl;
                continue;
            }
            
            int from = (moveStr[1] - '1') * 8 + (moveStr[0] - 'a');
            int to = (moveStr[3] - '1') * 8 + (moveStr[2] - 'a');
            
            Move move(from, to);
            if (moveGen.isLegalMove(board, move)) {
                board.makeMove(move);
                moveCount++;
            } else {
                std::cout << "Illegal move!" << std::endl;
            }
        } else {
            // AI move
            std::cout << "Chessy 1.6 is thinking..." << std::endl;
            Move move = search.findBestMove(board, 6);
            
            if (move.from != move.to) {
                board.makeMove(move);
                std::cout << "Chessy 1.6 plays: " << char('a' + move.from % 8) << (move.from / 8 + 1)
                          << char('a' + move.to % 8) << (move.to / 8 + 1) << std::endl;
                moveCount++;
            } else {
                std::cout << "No legal moves!" << std::endl;
                break;
            }
        }
    }
}

void trainModel() {
    std::cout << "=== Chessy 1.6 Training ===" << std::endl;
    
    TrainingConfig config;
    config.numGamesGeneration = 100;      // Start small for testing
    config.stockfishDepth = 20;
    config.blunderRate = 0.05f;
    config.epochs = 50;
    config.learningRate = 0.001f;
    config.batchSize = 32;
    config.numSelfPlayGames = 50;
    config.numTestGames = 100;
    
    std::string stockfishPath = "stockfish/stockfish-windows-x86-64-avx2.exe";
    
    Trainer trainer(config, stockfishPath);
    TrainingResult result = trainer.train();
    
    std::cout << "\n=== Training Results ===" << std::endl;
    std::cout << "Training Loss: " << result.trainingLoss << std::endl;
    std::cout << "Validation Loss: " << result.validationLoss << std::endl;
    std::cout << "Self-play Win Rate: " << (result.selfPlayWinRate * 100) << "%" << std::endl;
    std::cout << "vs Stockfish Win Rate: " << (result.stockfishWinRate * 100) << "%" << std::endl;
    std::cout << "Estimated ELO: " << result.estimatedELO << std::endl;
    
    // Save model
    trainer.saveModel("models/chessy_1.6_weights.bin");
}

void generateTrainingData() {
    std::cout << "=== Generating Training Data ===" << std::endl;
    
    TrainingConfig config;
    config.numGamesGeneration = 1000;
    config.stockfishDepth = 25;
    config.blunderRate = 0.05f;
    
    std::string stockfishPath = "stockfish/stockfish-windows-x86-64-avx2.exe";
    
    Trainer trainer(config, stockfishPath);
    trainer.generateTrainingData();
    
    std::cout << "Training data generated successfully!" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printUsage();
        return 0;
    }
    
    std::string command = argv[1];
    
    if (command == "--help") {
        printUsage();
    } else if (command == "--play") {
        playInteractive();
    } else if (command == "--train") {
        trainModel();
    } else if (command == "--generate-data") {
        generateTrainingData();
    } else if (command == "--test") {
        std::cout << "Testing mode not yet implemented" << std::endl;
    } else {
        std::cout << "Unknown command: " << command << std::endl;
        printUsage();
    }
    
    return 0;
}
