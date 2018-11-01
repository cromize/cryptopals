#include <stdio.h>
#include <string.h>
#include <math.h>
#include "hex2base64.h"
#include "crack_multibyte_xor.h"
#include "crack_singlebyte_xor.h"
#include "helpers.h"

#define KEYSIZE_DEF     45
#define KEYSIZE_MIN      2

static int determine_keysize(const uint8_t* input, int min_keysize_input, int n) {
  unsigned char first_keysize_bytes[KEYSIZE_DEF+1] = {0};
  unsigned char second_keysize_bytes[KEYSIZE_DEF+1] = {0};
  unsigned char third_keysize_bytes[KEYSIZE_DEF+1] = {0};
  unsigned char fourth_keysize_bytes[KEYSIZE_DEF+1] = {0};

  float smallest_avg = 32767; 
  int smallest_keysize = 0;

  float hamming_dist1 = 0;
  float hamming_dist2 = 0;
  float hamming_avg = 0;

  int keysize_max = KEYSIZE_DEF;
  if (n < keysize_max) keysize_max = n;

  // determine KEYLENGTH
  for (int keysize = min_keysize_input; keysize <= keysize_max; keysize++) {
    for (int i = 0; i < keysize; i++) {
      first_keysize_bytes[i] = input[i];
      second_keysize_bytes[i] = input[i+keysize];
      third_keysize_bytes[i] = input[i+keysize*2];
      fourth_keysize_bytes[i] = input[i+keysize*3];
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
  /*
  printf("\nsmallest avg: %f \n", smallest_avg);
  printf("keysize: %i \n", smallest_keysize);
  */
  return smallest_keysize;
}

int crack_multibyte_xor(const char* input_file, char* key_output, char* output) {
  FILE *fp = fopen(input_file, "rb");

  char file_line[DEFAULT_SIZE] = {0};
  char base64_buf[DEFAULT_SIZE] = {0};
  uint8_t buf[DEFAULT_SIZE] = {0};

  uint8_t output_tmp[DEFAULT_SIZE] = {0};
  uint8_t key_tmp[DEFAULT_SIZE] = {0};

  int highest_score = 0;

  if (!fp) return -1;

  while (fgets(file_line, DEFAULT_SIZE, fp)) {
    strtok(file_line, "\n");
    strcat(base64_buf, file_line);
  }

  int n = base64_decode(base64_buf, buf);
  int keysize = determine_keysize(buf, KEYSIZE_MIN, n); 

  while (keysize <= KEYSIZE_DEF) {
    int num_of_blocks = n/keysize+1;

    // make 2d array for blocks and for loop to shift buf to each block 
    // find output with best histogram 

    // blocks[keysize_length][ciphertext]
    uint8_t blocks[KEYSIZE_DEF][DEFAULT_SIZE] = {0};
    
    // transpose to blocks of KEYSIZE length
    int p = 0;
    for (int i = 0; i < num_of_blocks; i++) {
      for (int j = 0; j < keysize; j++) { 
        blocks[j][i] = buf[p++];
      }
    } 

    int score = 0;
    char cracked_blocks[KEYSIZE_DEF][DEFAULT_SIZE] = {0};

    // crack transposed blocks by singlebyte xor
    char cracked_key[KEYSIZE_DEF] = {0};
    for (int i = 0; i < keysize; i++) {
      cracked_key[i] = crack_singlebyte_xor(blocks[i], cracked_blocks[i], &score, num_of_blocks);
    }

    char final_output[DEFAULT_SIZE] = {0};

    // transpose blocks back to form output
    int k = 0;
    for (int i = 0; i < num_of_blocks; i++) {
      for (int j = 0; j < keysize; j++) {
        if (k >= n) break;
        final_output[k++] = cracked_blocks[j][i];
      }
    } 

    int cracked_text_score = calculate_score(final_output);

    // we need to compare score of cracked output
    if (cracked_text_score > highest_score) {
      strcpy(output_tmp, final_output);
      strcpy(key_tmp, cracked_key);
      highest_score = cracked_text_score;
    }

    if (++keysize < KEYSIZE_DEF) keysize = determine_keysize(buf, keysize, n); 
  }
  
  strcpy(key_output, key_tmp);
  strcpy(output, output_tmp);
  return 0;
}
