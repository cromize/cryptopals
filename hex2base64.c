// hex to base64, by: cromize(2018)

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

const char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

// *** Helpers ***
long hex(char a, char b) {
  char temp[] = {a, b};
  return strtol(temp, NULL, 16);
}

char* unhex(uint8_t a) {
  char* temp = malloc(sizeof(uint8_t));  
  if (!temp)
    return NULL;

  sprintf(temp, "%x", a);
  return temp;
}

int8_t pos_in_alphabet(char input) {
  for (uint8_t j = 0; j < 64; j++) {
    if (input == alphabet[j])  
      return j;
  }

  return 0;
}


char* encode(const char* input) {
  uint32_t temp;
  uint32_t k = 0;
  uint8_t a, b, c;
  uint8_t w, x, y, z;
  char* output;

  output = malloc(sizeof(char) * 1000);
  if (!output)
    return NULL;

  if (strlen(input) <= 0)
    return "";

  if (strlen(input) & 1) {
    printf("%s\n", "hex input is odd!");
    exit(0);
  }
    
  // process at most 6 bytes per iteration
  for (uint32_t i = 0; i < (strlen(input)); i += 6) {
    a = hex(input[i], input[i+1]);
    b = hex(input[i+2], input[i+3]);
    c = hex(input[i+4], input[i+5]);

    temp = (a << 24) | (b << 16) | (c << 8);

    w = (temp & 0xfc000000) >> 26;
    x = (temp & 0x03f00000) >> 20;
    y = (temp & 0x000fc000) >> 14;
    z = (temp & 0x00003f00) >> 8;   

    output[k++] = alphabet[w];
    output[k++] = alphabet[x];

    // Special processing (fewer than 24 bits in input)
    if ((strlen(input) > 2) & (i <= strlen(input)-6)) {
      output[k++] = alphabet[y];           
    } else output[k++] = '='; 

    if ((strlen(input) > 4) & (i <= strlen(input)-6)) {
      output[k++] = alphabet[z];           
    } else output[k++] = '='; 

    // Debug output
    //printf("%u\n%u\n%u\n%u\n\n", w, x, y, z); 
    //printf("%s\n", output);
  }

  return output;
}

uint8_t* decode(const char* input) {
  char* output = malloc(1000*sizeof(char));
  uint8_t a = 0, b = 0, c = 0, d = 0;
  uint8_t w = 0, x = 0, y = 0;
  uint32_t k = 0;
  uint32_t temp = 0;

  if (strlen(input) <= 0)
      return "";

  for(uint32_t i = 0; i < strlen(input); i += 4) {
    // Input bytes
    a = pos_in_alphabet(input[i]);
    b = pos_in_alphabet(input[i+1]);
    c = pos_in_alphabet(input[i+2]);
    d = pos_in_alphabet(input[i+3]);
    
    temp = (a << 26) | (b << 20) | (c << 14) | (d << 8);

    // Output bytes
    w = (temp >> 24);
    x = (temp >> 16);
    y = (temp >> 8);

    output[k++] = w;

    if ((strlen(input) > 1))
      output[k++] = x;

    if ((strlen(input) > 2))
      output[k++] = y;
  }
  
  return output;
}


int main(int argc, char* argv[]) {
  // Print help
  if (argc <= 1) {
    printf("%s\n", "base64 to hex tool");
    printf("%s\n", "supply input or -d for decryption.");
    exit(0);
  }

  // Print hex to base64
  if (argc == 2)
    printf("%s\n", encode(argv[1]));

  // Print base64 to hex
  if (argc == 3) {
    if (strcmp(argv[1], "-d") == 0) {
      uint8_t* bytes = decode(argv[2]);

      for (int i = 0; i < strlen((const char*) bytes); i++) {
        printf("%x", bytes[i]);
      }
      printf("\n");
    }
  }

  return 0;
}
