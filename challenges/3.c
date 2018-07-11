// find key to a single byte XOR cipher

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "../helpers.h"
#include "../crack_singlebyte_xor.h"

int main(int argc, char* argv[]) {
  char output[DEFAULT_SIZE];
  char key;
  int highest_score;
  
  // Print help
  if (argc <= 1) {
    printf("%s\n", "single byte XOR decrypt tool");
    printf("%s\n", "supply input");
    exit(0);
  }

  // decrypt  
  if (argc == 2) {
    uint8_t temp[DEFAULT_SIZE] = {0};
    int size = strlen(argv[1]);
    unhex_string(argv[1], temp);
    key = crack_singlebyte_xor(temp, output, &highest_score, size/2);
    printf("decrypted: %s\n", output);
    printf("key: %c (decimal: %d)\n", key, key);
  } 

  return 0;
}
