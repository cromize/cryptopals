// find key to a single byte XOR cipher

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "../helpers.h"
#include "../singlebyte_xor_decrypt.h"

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
    key = crack_singlebyte_xor(argv[1], output, &highest_score);
    printf("decrypted: %s\n", output);
    printf("key: %c (dec: %d)\n", key, key);
  } 

  return 0;
}
