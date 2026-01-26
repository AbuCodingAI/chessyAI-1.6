#include "transposition.h"

TranspositionTable::TranspositionTable(size_t size) : maxSize(size) {}

void TranspositionTable::store(uint64_t hash, float eval, int depth, int flag) {
    if (table.size() >= maxSize) {
        table.clear();  // Simple replacement strategy
    }
    
    table[hash] = {eval, depth, flag};
}

bool TranspositionTable::lookup(uint64_t hash, float& eval, int depth) {
    auto it = table.find(hash);
    if (it == table.end()) return false;
    
    if (it->second.depth >= depth) {
        eval = it->second.eval;
        return true;
    }
    
    return false;
}

void TranspositionTable::clear() {
    table.clear();
}
