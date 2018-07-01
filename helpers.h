#ifndef HELPERS_H
#define HELPERS_H

#define DEFAULT_SIZE        1024
#define DEFAULT_LINE_SIZE   512

#include <stdint.h>
#include <string.h>

const char alphabet[64];

uint8_t unhex(char a, char b);
int32_t unhex_string(const char* input, uint8_t* output); 

void hex(uint8_t a, char* output); 
int32_t hex_string(const char* input, char* output); 

int8_t pos_in_alphabet(char input); 
int hamming_distance(const char* input1, const char* input2);

#endif
