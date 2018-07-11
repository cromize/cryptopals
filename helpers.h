#ifndef HELPERS_H
#define HELPERS_H

#define DEFAULT_SIZE        1024 * 16
#define DEFAULT_LINE_SIZE   512

#include <stdint.h>
#include <string.h>

const char alphabet[64];

uint8_t unhex(const char a, const char b);
int32_t unhex_string(const char* input, uint8_t* output); 

void hex(const uint8_t a, char* output); 
int32_t hex_string(const uint8_t* input, char* output, int32_t n); 

int8_t pos_in_alphabet(char input); 
int hamming_distance(const uint8_t* input1, const uint8_t* input2, int n);

#endif
