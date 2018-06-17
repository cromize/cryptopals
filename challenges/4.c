// detect xor cipher in file, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../helpers.h"
#include "../xor.h"

int main(int argc, char* argv[]) {
  char output[DEFAULT_SIZE];

  // Print help
  if (argc <= 1) {
    printf("%s\n", "detect single byte XOR cipher tool");
    printf("%s\n", "supply input file");
    exit(0);
  }

  // detect 
  if (argc == 2) {
    detect_singlebyte_xor_cipher(argv[1], output);    
    printf("string: %s", output);
  } 

  return 0;
}
