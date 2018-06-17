// helper functions, by: cromize(2018)

#include <stdio.h>
#include "helpers.h"

const char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

// *** Helpers ***
uint8_t unhex(char a, char b) {
  char temp[] = {a, b};
  return strtol(temp, 0, 16);
}

int32_t unhex_string(const char* input, uint8_t* output) {
  char buf[DEFAULT_SIZE] = {0};
  int32_t size = strlen(input);
  int32_t j = 0;

  if (size >= DEFAULT_SIZE || size <= 0)
    return -1; 

  for (int i = 0; i < size; i+=2) {
    buf[j++] = unhex(input[i], input[i+1]);
  }
  memcpy(output, buf, strlen(buf));
  //strcpy(output, buf);
  return 0;
}

void hex(uint8_t a, char* output) {
  char buf[3] = {0};

  sprintf(buf, "%02x", a);
  strcpy(output, buf);
  return;
}

int32_t hex_string(const char* input, char* output) {
  char buf[DEFAULT_SIZE] = {0};
  int32_t size = strlen(input);

  if (size >= DEFAULT_SIZE || size <= 0)
    return -1; 

  for (int i = 0; i < size; i++) {
    sprintf(buf + strlen(buf), "%02x", input[i]);
  }
  strcpy(output, buf);
  return 0;
}

int8_t pos_in_alphabet(char input) {
  for (uint8_t j = 0; j < 64; j++) {
    if (input == alphabet[j])  
      return j;
  }

  return -1;
}
