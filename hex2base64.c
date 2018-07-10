// hex to base64 and vice versa, by: cromize(2018)

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "hex2base64.h"
#include "helpers.h"

int32_t base64_encode(const char* input, char* output) {
  char buf[DEFAULT_SIZE] = {0};
  int32_t size = strlen(input);
  uint8_t a = 0, b = 0, c = 0;
  uint8_t w = 0, x = 0, y = 0, z = 0;
  uint32_t k = 0;
  uint32_t temp = 0;

  if (size >= DEFAULT_SIZE || size <= 0)
    return -1;
    
  // process at most 3 bytes per iteration
  for (uint32_t i = 0; i < size; i += 6) {
    a = unhex(input[i], input[i+1]);
    b = unhex(input[i+2], input[i+3]);
    c = unhex(input[i+4], input[i+5]);

    temp = (a << 24) | (b << 16) | (c << 8);

    w = (temp & 0xfc000000) >> 26;
    x = (temp & 0x03f00000) >> 20;
    y = (temp & 0x000fc000) >> 14;
    z = (temp & 0x00003f00) >> 8;   

    buf[k++] = alphabet[w];
    buf[k++] = alphabet[x];
 
    // Special processing (fewer than 24 bits in input)
    if ((size > 2) && (i <= size-3)) {
      buf[k++] = alphabet[y];           
    } else buf[k++] = '='; 

    if ((size > 4) && (i <= size-6)) {
      buf[k++] = alphabet[z];           
    } else buf[k++] = '='; 

    // Debug output
    //printf("%u\n%u\n%u\n%u\n\n", w, x, y, z); 
    //printf("%s\n", output);
  }
  memcpy(output, buf, sizeof(uint8_t) * DEFAULT_SIZE);
  return 0;
}

int32_t base64_decode(const char* input, uint8_t* output) {
  uint8_t buf[DEFAULT_SIZE] = {0};
  uint8_t a, b, c, d;
  uint8_t w, x, y;
  uint32_t k = 0;
  uint32_t temp = 0;
  int32_t size = strlen(input);

  if (size >= DEFAULT_SIZE || size <= 0)
    return -1; 

  for (uint32_t i = 0; i < size; i += 4) {
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
  return 0;
}
