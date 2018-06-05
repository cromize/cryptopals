// xor two equal buffers, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "helpers.c"

char* xor(const char* str1, const char* str2) {
  uint32_t k = 0;
  char* output = malloc(sizeof(char) * 1000);
  
  if (!output)
    return NULL; 

  if (strlen(str1) != strlen(str2)) {
    printf("%s\n", "input lengths don't match");
    exit(0);
  }

  if (strlen(str1) & 1) {
    printf("%s\n", "hex input is odd!");
    exit(0);
  }
 
  for (uint8_t i = 0; i < strlen(str1); i+=2) {
    uint8_t a = unhex(str1[i], str1[i+1]);
    uint8_t b = unhex(str2[i], str2[i+1]);

    strcat(output, hex(a ^ b)); 
  }

  return output;
}

int main(int argc, char* argv[]) {
  // Print help
  if (argc <= 1) {
    printf("%s\n", "xor tool");
    printf("%s\n", "supply input");
    exit(0);
  }

  // Print xor 
  if (argc == 3)
    printf("%s\n", xor(argv[1], argv[2]));

  return 0;
}
