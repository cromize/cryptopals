// helper functions, by: cromize(2018)

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

