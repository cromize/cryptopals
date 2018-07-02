#ifndef HEX2BASE_H
#define HEX2BASE_H

#include <stdint.h>

int32_t base64_encode(const char* input, char* output);
int32_t base64_decode(const char* input, char* output);

#endif
