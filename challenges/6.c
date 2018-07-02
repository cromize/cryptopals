#include <stdio.h>
#include <stdlib.h>
#include "../helpers.h"
#include "../crack_multibyte_xor.h"

int main(int argc, char** argv) {
  // Print help
  if (argc < 2) {
    printf("%s\n", "crack Vigenere cipher");
    printf("%s\n", "supply input file");
    exit(0);
  }

  // crack
  if (argc == 2) {
    crack_multibyte_xor(argv[1]);
  }

  return 0;
}
