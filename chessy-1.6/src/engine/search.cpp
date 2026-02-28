#include "search.h"
#include "../chess/moves.h"
#include <algorithm>
#include <limits>

Search::Search(Evaluator* evaluator) : evaluator(evaluator), nodesSearched(0) {}

Move Search::findBestMove(Board& board, int depth, int /*timeLimit*/) {
    MoveGenerator moveGen;
    std::vector<Move> moves = moveGen.generateLegalMoves(board);
    
    if (moves.empty()) return Move();
    
    Move bestMove = moves[0];
    float bestEval = -std::numeric_limits<float>::infinity();
    
    for (const Move& move : moves) {
        board.makeMove(move);
        float eval = -alphaBeta(board, depth - 1, -std::numeric_limits<float>::infinity(), 
                                std::numeric_limits<float>::infinity(), false);
        board.unmakeMove(move);
        
        if (eval > bestEval) {
            bestEval = eval;
            bestMove = move;
        }
    }
    
    return bestMove;
}

float Search::alphaBeta(Board& board, int depth, float alpha, float beta, bool maximizing) {
    nodesSearched++;
    
    if (depth == 0) {
        return smartQuiescence(board, alpha, beta, 0, MAX_QUIESCENCE_DEPTH);
    }
    
    MoveGenerator moveGen;
    std::vector<Move> moves = moveGen.generateLegalMoves(board);
    
    if (moves.empty()) {
        if (board.isInCheck(board.getTurn())) {
            return -1000.0f;  // Checkmate
        } else {
            return 0.0f;  // Stalemate
        }
    }
    
    if (maximizing) {
        float maxEval = -std::numeric_limits<float>::infinity();
        for (const Move& move : moves) {
            board.makeMove(move);
            float eval = alphaBeta(board, depth - 1, alpha, beta, false);
            board.unmakeMove(move);
            
            maxEval = std::max(maxEval, eval);
            alpha = std::max(alpha, eval);
            if (beta <= alpha) break;  // Beta cutoff
        }
        return maxEval;
    } else {
        float minEval = std::numeric_limits<float>::infinity();
        for (const Move& move : moves) {
            board.makeMove(move);
            float eval = alphaBeta(board, depth - 1, alpha, beta, true);
            board.unmakeMove(move);
            
            minEval = std::min(minEval, eval);
            beta = std::min(beta, eval);
            if (beta <= alpha) break;  // Alpha cutoff
        }
        return minEval;
    }
}

float Search::smartQuiescence(Board& board, float alpha, float beta, int depth, int maxDepth) {
    // Evaluate current position
    float eval = evaluator->evaluate(board);
    
    // Beta cutoff
    if (eval >= beta) return beta;
    
    // Update alpha
    if (alpha < eval) alpha = eval;
    
    // Stop if max depth reached
    if (depth >= maxDepth) return eval;
    
    MoveGenerator moveGen;
    std::vector<Move> moves = moveGen.generateLegalMoves(board);
    
    // Separate captures and quiet moves
    std::vector<Move> captures;
    std::vector<Move> quietMoves;
    
    for (const Move& move : moves) {
        if (board.getPieceAt(move.to) != PieceType::NONE) {
            captures.push_back(move);
        } else {
            quietMoves.push_back(move);
        }
    }
    
    // Sort captures by piece value (MVV-LVA: Most Valuable Victim - Least Valuable Attacker)
    std::sort(captures.begin(), captures.end(), [&board](const Move& a, const Move& b) {
        int victimA = static_cast<int>(board.getPieceAt(a.to));
        int victimB = static_cast<int>(board.getPieceAt(b.to));
        return victimA > victimB;
    });
    
    // Process captures
    bool inCaptureSequence = false;
    int captureExtensionDepth = 0;
    
    for (const Move& move : captures) {
        board.makeMove(move);
        
        // Check if we're in a capture sequence
        inCaptureSequence = isInCaptureSequence(board, move);
        
        // Extend depth if in capture sequence
        int nextDepth = depth + 1;
        if (inCaptureSequence) {
            captureExtensionDepth = nextDepth + CAPTURE_EXTENSION;
        }
        
        float score = -smartQuiescence(board, -beta, -alpha, nextDepth, 
                                       inCaptureSequence ? captureExtensionDepth : maxDepth);
        board.unmakeMove(move);
        
        // Beta cutoff
        if (score >= beta) return beta;
        
        // Update alpha
        if (score > alpha) alpha = score;
    }
    
    // Consider quiet moves only if not in capture sequence
    if (!inCaptureSequence && depth < maxDepth - 5) {
        for (const Move& move : quietMoves) {
            // Only consider checks and promotions
            board.makeMove(move);
            bool isCheck = board.isInCheck(board.getTurn() == Color::WHITE ? Color::BLACK : Color::WHITE);
            board.unmakeMove(move);
            
            if (!isCheck) continue;
            
            board.makeMove(move);
            float score = -smartQuiescence(board, -beta, -alpha, depth + 1, maxDepth);
            board.unmakeMove(move);
            
            if (score >= beta) return beta;
            if (score > alpha) alpha = score;
        }
    }
    
    return alpha;
}

bool Search::isInCaptureSequence(Board& board, const Move& move) {
    // Check if the destination square is under attack
    // This indicates a potential recapture
    
    Color opponent = board.getTurn();  // After move, it's opponent's turn
    Square targetSq = move.to;
    
    // Simple check: see if opponent has a capture available
    MoveGenerator moveGen;
    std::vector<Move> opponentMoves = moveGen.generateLegalMoves(board);
    
    for (const Move& opMove : opponentMoves) {
        if (opMove.to == targetSq && board.getPieceAt(opMove.to) != PieceType::NONE) {
            return true;  // Opponent can recapture
        }
    }
    
    return false;
}
