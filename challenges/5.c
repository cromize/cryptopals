// repeating key xor, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../helpers.h"
#include "../xor.h"

int main(int argc, char* argv[]) {
  char output[DEFAULT_SIZE];

  // Print help
  if (argc <= 2) {
    printf("%s\n", "repeating key xor tool");
    printf("%s\n", "supply input file and key");
    exit(0);
  }

  // Print xor 
  if (argc == 3) {
    repeating_key_xor(argv[1], argv[2], output);
    printf("%s\n", output);
  }

  return 0;
}
