// detect xor cipher in file, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "helpers.h"
#include "detect_singlebyte_xor.h"
#include "singlebyte_xor_decrypt.h"

void detect_singlebyte_xor_cipher(const char* input_file, char* output) {
  FILE *input;
  int score_arr[DEFAULT_SIZE] = {0};
  char buf[256];  
  char xored_arr[DEFAULT_SIZE][256] = {0};

  input = fopen(input_file, "r");
  if (input == 0) 
    return -1;

  // process each line in file and save it into memory
  int i = 0;
  while (fgets(buf, 256, input) != 0) {
    char temp[256];
    int score;
    crack_singlebyte_xor(buf, temp, &score);
    strcpy(xored_arr[i], temp);
    score_arr[i++] = score;
  }

  // find line with highest score
  int highest = 0;
  int pos = 0;
  for (int i = 0; i < DEFAULT_SIZE; i++) {
    if (score_arr[i] > highest) {
      highest = score_arr[i];
      pos = i;
    }
  }

  strcpy(output, xored_arr[pos]);
  return;
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
    detect_singlebyte_xor_cipher(argv[1], output);    
    printf("string: %s", output);
  } 

  return 0;
}
#endif
