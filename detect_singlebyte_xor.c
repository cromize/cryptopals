// detect xor cipher in file, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "helpers.h"
#include "singlebyte_xor_decrypt.h"

void detect_xor_cipher(const char* input_file, char* output) {
  FILE *input;
  int score_arr[DEFAULT_SIZE] = {0};
  char buf[256];  
  char input_arr[DEFAULT_SIZE][256] = {0};

  input = fopen(input_file, "r");
  if (input == 0) 
    return -1;

  int i = 0;
  while (fgets(buf, 256, input) != 0) {
    char temp[256];
    int score;
    crack_singlebyte_xor(buf, temp, &score);
    //printf("%d. score: %d string: %s\n", i++, highest_score, temp);
    strcpy(input_arr[i], temp);
    score_arr[i++] = score;
  }

  int highest = 0;
  int pos = 0;
  for (int i = 0; i < DEFAULT_SIZE; i++) {
    if (score_arr[i] > highest) {
      highest = score_arr[i];
      pos = i;
    }
  }

  printf("%d. score: %d string: %s\n", pos, highest, input_arr[pos]);
}

#ifndef DETECT_SINGLEBYTE_XOR 
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
    detect_xor_cipher(argv[1], 0);    
  } 

  return 0;
}
#endif
