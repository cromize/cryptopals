#include <stdio.h>
#include <string.h>
#include <math.h>
#include "hex2base64.h"
#include "crack_multibyte_xor.h"
#include "crack_singlebyte_xor.h"
#include "helpers.h"

#define KEYSIZE_DEF     45

int crack_multibyte_xor(const char* input_file) {
  FILE *fp = fopen(input_file, "rb");

  char file_line[DEFAULT_SIZE] = {0};
  char base64_buf[DEFAULT_SIZE] = {0};
  unsigned char buf[DEFAULT_SIZE] = {0};

  unsigned char first_keysize_bytes[KEYSIZE_DEF+1] = {0};
  unsigned char second_keysize_bytes[KEYSIZE_DEF+1] = {0};
  unsigned char third_keysize_bytes[KEYSIZE_DEF+1] = {0};
  unsigned char fourth_keysize_bytes[KEYSIZE_DEF+1] = {0};

  float smallest_avg = 32767; 
  int smallest_keysize = 0;
  int n = 0;

  float hamming_dist1 = 0;
  float hamming_dist2 = 0;
  float hamming_avg = 0;

  while (fgets(file_line, DEFAULT_SIZE, fp)) {
    strtok(file_line, "\n");
    strcat(base64_buf, file_line);
  }

  n = base64_decode(base64_buf, buf);

  int keysize_max = KEYSIZE_DEF;
  if (n < keysize_max) keysize_max = n/4;

  for (int keysize = 14; keysize < keysize_max; keysize++) {
    for (int i = 0; i < keysize; i++) {
      first_keysize_bytes[i] = buf[i];
      second_keysize_bytes[i] = buf[i+keysize];
      third_keysize_bytes[i] = buf[i+keysize*2];
      fourth_keysize_bytes[i] = buf[i+keysize*3];
    }
    hamming_dist1 = hamming_distance(first_keysize_bytes, second_keysize_bytes, keysize)/(float)keysize;
    hamming_dist2 = hamming_distance(third_keysize_bytes, fourth_keysize_bytes, keysize)/(float)keysize;
    hamming_avg = (hamming_dist1 + hamming_dist2)/2;

    memset(first_keysize_bytes, 0, sizeof(first_keysize_bytes));
    memset(second_keysize_bytes, 0, sizeof(first_keysize_bytes));
    memset(third_keysize_bytes, 0, sizeof(first_keysize_bytes));
    memset(fourth_keysize_bytes, 0, sizeof(first_keysize_bytes));

    if (hamming_dist1 < 0 || hamming_dist2 < 0) break;
    if (hamming_avg < smallest_avg) {
      smallest_keysize = keysize;
      smallest_avg = hamming_avg;
    }
    /*
    printf("dist1: %f \n", hamming_dist1);
    printf("dist2: %f \n", hamming_dist2);
    printf("hamming_avg: %f \n", hamming_avg);
    printf("keysize: %i \n", keysize);
    */
  }
  printf("\nsmallest avg: %f \n", smallest_avg);
  printf("keysize: %i \n", smallest_keysize);

/*
  for (int i = 0; i < n; i++) {
    printf("%03i ", buf[i]);
  } 
  printf("\n");
*/

  // TODO: make 2d array for blocks and for loop to shift buf to each block 
  //       find output with best histogram 

  // blocks[keysize_length][ciphertext]
  uint8_t blocks[KEYSIZE_DEF][DEFAULT_SIZE] = {0};
  
  // transpose to blocks of KEYSIZE length
  int p = 0;
  for (int i = 0; i < n/smallest_keysize; i++) {
    for (int j = 0; j < smallest_keysize; j++) { 
      blocks[j][i] = buf[p++];
    }
  } 

  // just for print
  /*
  for (int i = 0; i < n/smallest_keysize; i++) {
    for (int j = 0; j < smallest_keysize; j++) { 
      printf("%03i ", blocks[j][i]);
    }
    printf("\n");
  } 
  printf("\n");
 */ 

    //exit(0);
  int highest_score = 0;
  uint8_t temp[DEFAULT_SIZE] = {0};
  uint8_t cracked_blocks[KEYSIZE_DEF][DEFAULT_SIZE] = {0};

  // crack transposed blocks by singlebyte xor
  for (int i = 0; i < smallest_keysize; i++) {
    crack_singlebyte_xor(blocks[i], cracked_blocks[i], &highest_score, n/smallest_keysize);
  }

  /*
  for (int i = 0; i < smallest_keysize; i++) {
    printf("%s\n", cracked_blocks[i]);
  }

  for (int i = 0; i < n/smallest_keysize; i++) { 
    for (int j = 0; j < smallest_keysize; j++) {
      printf("%c ", cracked_blocks[j][i]);
    }
    printf("\n");
  }
  exit(0);

  */
  char final_output[DEFAULT_SIZE] = {0};

  int k = 0;
  for (int i = 0; i < n/smallest_keysize; i++) {
    for (int j = 0; j < smallest_keysize; j++) {
      final_output[k++] = cracked_blocks[j][i];
    }
  } 

  printf("string: %s\n", final_output);
  return 0;
}
