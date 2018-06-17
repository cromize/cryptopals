#ifndef XOR_H
#define XOR_H

void xor(const char* str1, const char* str2, char* output); 
void detect_singlebyte_xor_cipher(const char* input_file, char* output); 
void repeating_key_xor(const char* input_file, const char* key, char* output);

#endif
