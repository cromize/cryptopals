// xor functions, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "crack_singlebyte_xor.h"
#include "xor.h"
#include "helpers.h"

void xor(const char* str1, const char* str2, char* output) {
  char buf[DEFAULT_SIZE] = {0};
  int32_t size_s1 = strlen(str1);
  
  for (uint8_t i = 0; i < size_s1; i+=2) {
    uint8_t a = unhex(str1[i], str1[i+1]);
    uint8_t b = unhex(str2[i], str2[i+1]);

    char temp[3];
    hex(a ^ b, temp);
    strcat(buf, temp); 
  }

  strcpy(output, buf); 
  return;
}

int repeating_key_xor(const char* input_file, const char* key, char* output) {
  FILE* input;
  char buf[DEFAULT_LINE_SIZE] = {0};
  int ch = 0;
  int n = 0;
  int keypos = 0;

  input = fopen(input_file, "r");
  if (!input) 
    return -1;

  int keysize = strlen(key);
  uint8_t temp[DEFAULT_SIZE] = {0};

  // process each line in file
  while ((ch = fgetc(input)) != EOF) {
    if (ch == '\n') continue;
    temp[n++] = ch ^ key[keypos++];
    if (keypos >= keysize) keypos = 0;
  }
  
  hex_string(temp, buf, n*2);
  strcpy(output, buf);

  fclose(input);
  return 0;
}

int detect_singlebyte_xor_cipher(const char* input_file, int* score_output, char* output) {
  FILE* input;
  int score_tmp = 0;
  char output_buf[DEFAULT_SIZE] = {0};
  char input_buf[DEFAULT_LINE_SIZE] = {0};  

  input = fopen(input_file, "r");
  if (!input) 
    return -1;

  // process each line in file, hold the line with biggest score
  while (fgets(input_buf, DEFAULT_LINE_SIZE, input) != 0) {
    uint8_t input_unhexed[DEFAULT_SIZE] = {0};
    char temp[DEFAULT_LINE_SIZE] = {0};
    int unhexed_size = strlen(input_buf)/2;
    int score = 0;
    unhex_string(input_buf, input_unhexed);
    crack_singlebyte_xor(input_unhexed, temp, &score, unhexed_size);
    if (score > score_tmp) {
      score_tmp = score;
      strcpy(output_buf, temp);
    }
  }

  strcpy(output, output_buf);
  *score_output = score_tmp; 
  fclose(input);
  return 0;
}
