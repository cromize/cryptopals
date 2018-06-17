// xor functions, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "xor.h"
#include "helpers.h"

void xor(const char* str1, const char* str2, char* output) {
  char buf[DEFAULT_SIZE];
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

void repeating_key_xor(const char* input_file, const char* key, char* output) {
  FILE* input;
  char buf[256] = {0};
  int ch = 0;
  int i = 0;
  int j = 0;

  input = fopen(input_file, "r");
  if (!input) 
    return -1;

  uint8_t temp[256] = {0};

  // process each line in file
  while ((ch = fgetc(input)) != EOF) {
    if (ch == '\n') break;
    temp[i++] = ch ^ key[j++];
    if (j >= strlen(key)) j = 0;
  }
  
  hex_string(temp, buf);
  strcpy(output, buf);

  fclose(input);
}

void detect_singlebyte_xor_cipher(const char* input_file, char* output) {
  FILE* input;
  int score_arr[DEFAULT_SIZE] = {0};
  char buf[256];  
  char xored_arr[DEFAULT_SIZE][256] = {0};

  input = fopen(input_file, "r");
  if (!input) 
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
  fclose(input);
  return;
}
