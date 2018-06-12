#ifndef HELPERS_H
#define HELPERS_H

#define DEFAULT_SIZE    1024

#include <stdint.h>
#include <stdio.h>
#include <string.h>

const char alphabet[26];

uint8_t unhex(char a, char b);
int32_t unhex_string(const char* input, uint8_t* output); 

void hex(uint8_t a, char* output); 
int32_t hex_string(const char* input, char* output); 

int8_t pos_in_alphabet(char input); 

#endif
