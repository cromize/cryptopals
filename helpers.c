// helper functions, by: cromize(2018)

#include <stdio.h>
#include <stdlib.h>
#include "helpers.h"

const char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

// *** Helpers ***
uint8_t unhex(const char a, const char b) {
  char temp[] = {a, b};
  return strtol(temp, 0, 16);
}

int32_t unhex_string(const char* input, uint8_t* output) {
  uint8_t buf[DEFAULT_SIZE] = {0};
  int32_t size = strlen(input);
  int32_t j = 0;

  if (size >= DEFAULT_SIZE || size <= 0)
    return -1; 

  for (int i = 0; i < size; i+=2) {
    buf[j++] = unhex(input[i], input[i+1]);
  }
  memcpy(output, buf, sizeof(uint8_t) * DEFAULT_SIZE);
  return 0;
}

void hex(const uint8_t a, char* output) {
  char buf[3] = {0};

  sprintf(buf, "%02x", a);
  buf[2] = '\0';
  memcpy(output, buf, sizeof(char) * 3);
  return;
}

int32_t hex_string(const uint8_t* input, char* output, int32_t n) {
  char buf[DEFAULT_SIZE] = {0};

  if (n >= DEFAULT_SIZE || n <= 0)
    return -1; 

  for (int i = 0; i < n; i++) {
    sprintf(buf + i*2, "%02x", input[i]);
  }
  strcpy(output, buf);
  return 0;
}

int8_t pos_in_alphabet(char input) {
  for (uint8_t j = 0; j < 64; j++) {
    if (input == alphabet[j])  
      return j;
    else if (input == '=') 
      return 65;
  }

  return -1;
}

int hamming_distance(const uint8_t* input1, const uint8_t* input2, int n) {
  //int len1 = strlen(input1);
  //int len2 = strlen(input2);
  int dist = 0;

  if (n <= 0) return -1;
  //if (len1 != len2) return -1;

  for (int i = 0; i < n; i++) {
    unsigned char val = input1[i] ^ input2[i];
    while (val != 0) {
      dist++;
      val &= val - 1;   // remove 1 bit each time
    }
  }

  return dist;
}
