// find key to a single byte XOR cipher

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "helpers.h"
#include "crack_singlebyte_xor.h"

// Take input, do INPUT XOR KEY(1byte)
// Save each variation
// Evaluate score of each variation
// Print first few outputs with highest score

char freq[] = "zqxjkvbpygfwmucldrhsnioate";

int calculate_score(const char* input) {
  int size = strlen(input);
  int score = 0;
  // each char in input
  for (int j = 0; j < size; j++) {

    // check if input char is in frequently used table
    for (int i = 0; i < 26; i++) {
      if (tolower(input[j]) == freq[i]) {
        score += i+1; 

        // continue to next iteration
        i = 32767;
      }
    }
  }
  return score;
}

// add score by frequency of usage of each letter
// the higher you are in freq array, the bigger the score
static void add_score(const char* input, uint32_t* score_arr_input, int line_num) {
  score_arr_input[line_num] = calculate_score(input); 
}

// returns a key with highest score
static char get_key_highest_score(uint32_t* score_arr, int32_t* highest_score) {
  int32_t highest = 0; 
  char highest_char = 0;

  // iterate through all keys(1byte)
  for (int i = 0; i < 256; i++) {
    if (score_arr[i] > highest) {
      highest = score_arr[i];
      highest_char = (char) i;
    }
  }
  *highest_score = highest;
  return highest_char;
}

// returns cracked key 
int32_t crack_singlebyte_xor(const uint8_t* input, char* output, int* highest_score_output, int n) {
  uint32_t score[256] = {0}; 
  char buf[DEFAULT_SIZE] = {0};

  if (n > DEFAULT_SIZE || n <= 0)
    return -1;

  // xor and score each input
  for (int32_t key = 1; key < 256; key++) {
    for(int j = 0; j < n; j++) {
      buf[j] = input[j] ^ key; 
    }
    add_score(buf, score, key);
  }

  int32_t highest_score = 0;
  char key = get_key_highest_score(score, &highest_score);

  // decrypt final output
  for (int j = 0; j < n; j++)
    buf[j] = input[j] ^ key;

  *highest_score_output = highest_score; 
  strcpy(output, buf);
  return key;
}
