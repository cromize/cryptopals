// xor functions, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "helpers.c"

void xor(const char* str1, const char* str2, char* output) {
  char buf[DEFAULT_SIZE];
  int32_t size_s1 = strlen(str1);
  
  for (uint8_t i = 0; i < size_s1; i+=2) {
    uint8_t a = unhex(str1[i], str1[i+1]);
    uint8_t b = unhex(str2[i], str2[i+1]);

    char temp[3];
    hex(a ^ b, temp);
    strcat(buf, temp); 
  }

  strcpy(output, buf); 

  return;
}

int main(int argc, char* argv[]) {
  char output[DEFAULT_SIZE];

  if (strlen(argv[1]) != strlen(argv[2])) {
    printf("%s\n", "input lengths don't match");
    exit(0);
  }

  if (strlen(argv[1]) & 1) {
    printf("%s\n", "hex input is odd!");
    exit(0);
  }

  // Print help
  if (argc <= 1) {
    printf("%s\n", "xor tool");
    printf("%s\n", "supply input");
    exit(0);
  }

  // Print xor 
  if (argc == 3) {
    xor(argv[1], argv[2], output);
    printf("%s\n", output);
  }

  return 0;
}
