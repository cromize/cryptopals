// hex to base64 and vice versa, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "../helpers.h"
#include "../hex2base64.h"

int main(int argc, char* argv[]) {
  // Print help
  if (argc <= 1) {
    printf("%s\n", "hex to base64 tool");
    printf("%s\n", "supply input or -d for decryption");
    exit(0);
  }

  // Print hex to base64
  if (argc == 2) { 
    if (strlen(argv[1]) & 1) {
      printf("%s\n", "hex input is odd!");
      exit(0);
    }
 
    char output[DEFAULT_SIZE] = {0};
    uint8_t buf[DEFAULT_SIZE] = {0};
    int n = unhex_string(argv[1], buf); 
    base64_encode((uint8_t*) buf, n, output);
    printf("%s\n", output);
  }

  // Print base64 to hex
  if (argc == 3) {
    if (strcmp(argv[1], "-d") == 0) {
      uint8_t bytes[DEFAULT_SIZE] = {0};
      base64_decode(argv[2], bytes);

      for (int i = 0; bytes[i] != '\00'; i++) {
        printf("%02x", bytes[i]);
      }
      printf("\n");
    }
  }

  return 0;
}

