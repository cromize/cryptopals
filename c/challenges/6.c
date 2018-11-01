// crack repeating key xor, by: cromize(2018)

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
    char cracked_key[DEFAULT_SIZE] = {0};
    char cracked_output[DEFAULT_SIZE] = {0};
    crack_multibyte_xor(argv[1], cracked_key, cracked_output);
    printf("output: \n%s\n", cracked_output);
    printf("key: %s\n", cracked_key);
    printf("keysize: %i\n", strlen(cracked_key));
  }

  return 0;
}
