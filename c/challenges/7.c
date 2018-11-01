#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <openssl/ssl.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include "../helpers.h"
#include "../hex2base64.h"

void handleErrors() {
  ERR_print_errors_fp(stderr);
  abort();
}

int encrypt(uint8_t* plaintext, int plaintext_len, uint8_t *key, uint8_t* ciphertext) {
  EVP_CIPHER_CTX *ctx;
  int len = 0;
  int ciphertext_len = 0;

  if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors(); 
  if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)) handleErrors();
  
  if (1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)) handleErrors();
  ciphertext_len = len;

  if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) handleErrors();
  ciphertext_len += len;

  EVP_CIPHER_CTX_free(ctx);
  
  return ciphertext_len;
}

int decrypt(uint8_t* ciphertext, int ciphertext_len, uint8_t* key, uint8_t* plaintext) {
  EVP_CIPHER_CTX *ctx;
  int len = 0;
  int plaintext_len = 0;
  
  if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors(); 
  if (1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL)) handleErrors();
  
  if (1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len)) handleErrors();
  plaintext_len = len;

  if (1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
  plaintext_len += len;

  EVP_CIPHER_CTX_free(ctx);

  plaintext[plaintext_len] = '\0';

  return plaintext_len;
}

int read_file(const char* filename, bool strip_newline, char* output) {
  char file_line[DEFAULT_SIZE] = {0};
  FILE* fp = fopen(filename, "rb");
  if (!fp) return -1;

  while (fgets(file_line, DEFAULT_SIZE, fp)) {
    if (strip_newline) strtok(file_line, "\n");
    strcat(output, file_line);
  }
  return strlen(output);
}

int main(int argc, char** argv) {
  char base64_buf[DEFAULT_SIZE] = {0};
  char plaintext[DEFAULT_SIZE] = {0};
  char key[DEFAULT_SIZE] = {0};
  uint8_t ciphertext[DEFAULT_SIZE] = {0};
  
  // Print help
  if (argc < 3) {
    printf("%s\n", "AES-128 ECB encrypt/decrypt tool");
    printf("%s\n", "supply input file and password (-d for decryption)");
    exit(0);
  }

  // encrypt
  if (argc == 3) {
    FILE* fp = fopen(argv[1], "rb");
    if (!fp) return -1;

    int n = read_file(argv[1], 0, plaintext); 
    strcpy(key, argv[2]);
    n = encrypt((uint8_t*) plaintext, n, (uint8_t*) key, ciphertext); 
    n = base64_encode(ciphertext, n, base64_buf);

    printf("%s\n", base64_buf);
  }

  // decrypt
  if (argc == 4) {
    if (strcmp(argv[1], "-d") == 0) {
      FILE* fp = fopen(argv[2], "rb");
      if (!fp) return -1;

      int n = read_file(argv[2], 1, base64_buf); 
      strcpy(key, argv[3]);
      n = base64_decode(base64_buf, ciphertext);
      n = decrypt(ciphertext, n, (uint8_t*) key, (uint8_t*) plaintext); 

      printf("%s", (char*) plaintext);
    }
  }
  return 0;
}
