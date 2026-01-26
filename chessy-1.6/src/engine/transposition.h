#pragma once

#include <unordered_map>
#include <cstdint>

struct TranspositionEntry {
    float eval;
    int depth;
    int flag;  // 0 = exact, 1 = lower bound, 2 = upper bound
};

class TranspositionTable {
public:
    TranspositionTable(size_t size = 1000000);
    
    void store(uint64_t hash, float eval, int depth, int flag);
    bool lookup(uint64_t hash, float& eval, int depth);
    void clear();
    
private:
    std::unordered_map<uint64_t, TranspositionEntry> table;
    size_t maxSize;
};
