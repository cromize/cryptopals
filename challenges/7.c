#include <stdio.h>
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

int main(int argc, char** argv) {
  FILE *fp = fopen(argv[1], "rb");
  char file_line[DEFAULT_SIZE] = {0};
  char base64_buf[DEFAULT_SIZE] = {0};
  uint8_t buf[DEFAULT_SIZE] = {0};
  uint8_t plaintext_buf[DEFAULT_SIZE] = {0};

  // 16 bytes
  unsigned char* key = (unsigned char*)"YELLOW SUBMARINE"; 

  if (!fp) return -1;

  while (fgets(file_line, DEFAULT_SIZE, fp)) {
    strtok(file_line, "\n");
    strcat(base64_buf, file_line);
  }

  int n = base64_decode(base64_buf, buf);

  printf("%s\n\n", buf);

  decrypt(buf, n, key, plaintext_buf); 

  uint8_t output[DEFAULT_SIZE] = {0};

  encrypt(plaintext_buf, n, key, output); 

  printf("\n%s\n", output);

  return 0;
}
