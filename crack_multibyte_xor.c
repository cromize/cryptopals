#include <stdio.h>
#include <string.h>
#include "hex2base64.h"
#include "crack_multibyte_xor.h"
#include "helpers.h"

#define KEYSIZE_DEF     45

int crack_multibyte_xor(const char* input_file) {
  FILE *fp = fopen(input_file, "rb");

  char base64_buf[32767] = {0};
  char buf[32767] = {0};

  char first_keysize_bytes[KEYSIZE_DEF+1] = {0};
  char second_keysize_bytes[KEYSIZE_DEF+1] = {0};
  char third_keysize_bytes[KEYSIZE_DEF+1] = {0};
  char fourth_keysize_bytes[KEYSIZE_DEF+1] = {0};

  int smallest_keysize = 32767; 

  float hamming_dist1 = 0;
  float hamming_dist2 = 0;
  float hamming_avg = 0;

  int pos = 0;
  while (fgets(base64_buf, DEFAULT_SIZE, fp)) {
    char temp[DEFAULT_SIZE] = {0};
    strtok(base64_buf, "\n");
    base64_decode(base64_buf, temp);
    strcat(buf, temp);
  }

  int keysize_max = KEYSIZE_DEF;
  if (strlen(buf) < keysize_max) keysize_max = strlen(buf)/4;

  for (int keysize = 2; ; keysize++) {
    for (int i = 0; i < keysize; i++) {
      first_keysize_bytes[i] = buf[i];
      second_keysize_bytes[i] = buf[i+keysize];
      third_keysize_bytes[i] = buf[i+keysize*2];
      fourth_keysize_bytes[i] = buf[i+keysize*3];
    }
    hamming_dist1 = hamming_distance(first_keysize_bytes, second_keysize_bytes)/(float)keysize;
    hamming_dist2 = hamming_distance(third_keysize_bytes, fourth_keysize_bytes)/(float)keysize;
    hamming_avg = (hamming_dist1 + hamming_dist2)/2;

    if (hamming_dist1 < 0 || hamming_dist2 < 0) break;
    if (hamming_avg < smallest_keysize) smallest_keysize = hamming_avg;

    printf("dist1: %f \n", hamming_dist1);
    printf("dist2: %f \n", hamming_dist2);
  }
  printf("smallest average: %i\n", smallest_keysize);
  return 0;
}
