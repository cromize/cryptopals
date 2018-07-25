// hex to base64 and vice versa, by: cromize(2018)

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "hex2base64.h"
#include "helpers.h"

int32_t base64_encode(const uint8_t* input, int len, char* output) {
  char buf[DEFAULT_SIZE] = {0};
  uint8_t w = 0, x = 0, y = 0, z = 0;
  uint32_t k = 0;
  uint32_t temp = 0;
  bool padding1 = 0, padding2 = 0;

  if (len >= DEFAULT_SIZE || len <= 0)
    return -1;

  // Set padding bytes
  if (len % 3 == 2)
    padding2 = 1;
  else if (len % 3 == 1) {
    padding1 = 1;
    padding2 = 1;
  }

  // process at most 3 bytes per iteration
  for (int i = 0; i < len; i += 3) {
    temp = (input[i] << 24) | (input[i+1] << 16) | (input[i+2] << 8);

    w = (temp & 0xfc000000) >> 26;
    x = (temp & 0x03f00000) >> 20;
    y = (temp & 0x000fc000) >> 14;
    z = (temp & 0x00003f00) >> 8;   

    buf[k++] = alphabet[w];
    buf[k++] = alphabet[x];
 
    // Special processing (fewer than 24 bits in input)
    if ((i > len-3) && padding1)
      buf[k++] = '='; 
    else buf[k++] = alphabet[y];

    if ((i > len-3) && padding2)
      buf[k++] = '=';
    else buf[k++] = alphabet[z];

    // Debug output
    //printf("%u\n%u\n%u\n%u\n\n", w, x, y, z); 
    //exit(0);
  }
  memcpy(output, buf, sizeof(char) * DEFAULT_SIZE);
  return k;
}

int32_t base64_decode(const char* input, uint8_t* output) {
  uint8_t buf[DEFAULT_SIZE] = {0};
  uint8_t a, b, c, d;
  uint8_t w, x, y;
  uint32_t k = 0;
  uint32_t temp = 0;
  int len = strlen(input);

  if (len >= DEFAULT_SIZE || len <= 0)
    return -1; 

  for (uint32_t i = 0; i < len; i += 4) {
    // Input bytes
    a = pos_in_alphabet(input[i]);
    b = pos_in_alphabet(input[i+1]);
    c = pos_in_alphabet(input[i+2]);
    d = pos_in_alphabet(input[i+3]);
    
    temp = (a << 26) | (b << 20) | (c << 14) | (d << 8);

    // Output bytes
    w = (temp >> 24);
    x = (temp >> 16);
    y = (temp >> 8);

    buf[k++] = w;

    if (c != 65)
      buf[k++] = x;

    if (d != 65)
      buf[k++] = y;
  }

  memcpy(output, buf, sizeof(uint8_t) * DEFAULT_SIZE);
  return k;
}
