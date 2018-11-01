// xor two input strings, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../xor.h"
#include "../helpers.h"

int main(int argc, char* argv[]) {
  char output[DEFAULT_SIZE];

  // Print help
  if (argc <= 2) {
    printf("%s\n", "xor tool");
    printf("%s\n", "supply input1 and input2");
    exit(0);
  }

  if (strlen(argv[1]) != strlen(argv[2])) {
    printf("%s\n", "input lengths don't match");
    exit(0);
  }

  if (strlen(argv[1]) & 1) {
    printf("%s\n", "hex input is odd!");
    exit(0);
  }

  // Print xor 
  if (argc == 3) {
    xor(argv[1], argv[2], output);
    printf("%s\n", output);
  }
  
  return 0;
}
