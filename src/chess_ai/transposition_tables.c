#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#define TABLE_ENTRIES 1000000
#define EMPTY_SCORE 42069

uint64_t zobrist_keys[8][8][12];

typedef struct {
    uint64_t hash;
    int score;
    // Other fields as needed
} TranspositionEntry;
TranspositionEntry table[TABLE_ENTRIES];

void init_zobrist_keys() {
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j) {
            for (int piece = 0; piece < 12; ++piece) {
                zobrist_keys[i][j][piece] = ((uint64_t)rand() << 32) | rand();
            }
        }
    }
}

void init_table() {
    for (size_t i = 0; i < TABLE_ENTRIES; i++) {
        table[i].score = EMPTY_SCORE;
    }
}

void init() {
    init_zobrist_keys();
    init_table();
}

uint64_t get_piece_index(int piece_value) {
    if (piece_value >= 0) {
        return piece_value;
    } else {
        return 6 - piece_value;
    }
}

void set_table(uint64_t hash, int score) {
    int index = hash % TABLE_ENTRIES;
    table[index].hash = hash;
    table[index].score = score;
    // Other fields can be updated as needed
}

uint64_t get_hash(int (*board)[8]) {
    uint64_t hash = 0;
    for (int i = 0; i < 8; ++i) {
        for (size_t j = 0; j < 8; j++) {
            int piece = get_piece_index(board[i][j]);
            if (piece != 0) {
                hash ^= zobrist_keys[i][j][piece];
            }
        }
    }
    return hash;
}

TranspositionEntry get_table(int (*board)[8]) {
    uint64_t hash = get_hash(board);
    int index = hash % TABLE_ENTRIES;
    TranspositionEntry entry = table[index];
    return entry;
}
