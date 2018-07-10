#include <stdio.h>
#include <stdlib.h>
#include "../helpers.h"

int main(int argc, char** argv) {
  // Print help
  if (argc <= 1) {
    printf("%s\n", "ascii to hex tool");
    printf("%s\n", "supply input");
    exit(0);
  }

  // Print ascii to hex 
  if (argc == 2) { 
    char temp[DEFAULT_SIZE] = {0};
    int size = strlen(argv[1]);
    hex_string((uint8_t*)argv[1], temp, size);
    printf("%s\n", temp);
  }

  // Print hex to ascii
  if (argc == 3) {
    if (strlen(argv[2]) & 1) {
      printf("%s\n", "hex input is odd!");
      exit(0);
    }

    if (strcmp(argv[1], "-d") == 0) {
      char temp[DEFAULT_SIZE] = {0};
      unhex_string(argv[2], (uint8_t*) temp);

      for (int i = 0; temp[i] != '\00'; i++) {
        printf("%c", temp[i]);
      }
      printf("\n");
    }
  }

  return 0;
}
