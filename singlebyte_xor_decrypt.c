// find key to a single byte XOR cipher

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "helpers.c"

// Take input, do INPUT XOR KEY(1byte)
// Save each variation
// Evaluate score of each variation
// Print first few outputs with highest score

char freq[] = "zqxjkvbpygfwmucldrhsnioate";

// add score by frequency of usage of each letter
// the higher you are in freq array, the bigger the score
void add_score(const char* input, uint32_t* score_arr, int line_num) {
  for (int j = 0; j < strlen(input); j++) {
    for (int i = 0; i < 26; i++) {
      if (tolower(input[j]) == freq[i]) {
        score_arr[line_num] += i+1; 

        // continue to next iteration
        i = 32767;
      }
      else
        score_arr[line_num] -= 0; 
    }
  }
}

// return a key with highest score
char get_key_highest_score(uint32_t* score_arr) {
  int32_t highest = 0; 
  char highest_char = 0;

  // iterate through all keys(1byte)
  for (int i = 0; i < 256; i++) {
    if (score_arr[i] > highest) {
      highest = score_arr[i];
      highest_char = (char) i;
    }
  }
  
  return highest_char;
}

int32_t crack(const char* input, char* output, char* output_key) {
  uint32_t score[256] = {0}; 
  uint8_t buf[DEFAULT_SIZE] = {0};
  uint8_t unhexed[DEFAULT_SIZE] = {0};

  // unhex input
  unhex_string(input, unhexed);

  // xor and score each input
  for (int32_t key = 1; key < 256; key++) {
    for(int j = 0; j < strlen(unhexed); j++) {
      buf[j] = unhexed[j] ^ key; 
    }
    
    add_score(buf, score, key);
  }

  char key = get_key_highest_score(score);

  for(int j = 0; j < strlen(unhexed); j++)
    buf[j] = unhexed[j] ^ key;

  //*output_key = key;

  //strcpy(output_key, key);
  strcpy(output, buf);
  return 0;

/*
  for (int i = 0; i < 256; i++) {
    printf("%d(%c)\t", score[i], i);

    for(int j = 0; j < strlen(buf); j++)
      printf("%c", buf[j] ^ i);

    printf("\n");
  }
  printf("\n");
*/

  /*
  for (int i = 0; i < 26; i++) {
    char key = get_highest_score(score) ^ freq[i];
    printf("\nkey: %c ", key);

    for(int j = 0; j < strlen(input); j++)
      printf("%c", key ^ input[j]); 
  }
  */
}

int main(int argc, char* argv[]) {
  char output[DEFAULT_SIZE];
  char key;
  
  // Print help
  if (argc <= 1) {
    printf("%s\n", "single byte XOR decrypt tool");
    printf("%s\n", "supply input");
    exit(0);
  }

  // decrypt  
  if (argc == 2) {
    crack(argv[1], output, key);
    printf("decrypted: %s\n", output);
    printf("key: %c (ASCII: %d)\n", key, key);
  } 

  return 0;
}
