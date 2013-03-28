#ifndef JN_H_
#define JN_H_

#include <stdlib.h>
#include <stdint.h>

#include "e_ringbuffer.h"

#define JN_REGS 14

#define JN_REG_A   0
#define JN_REG_X   1
#define JN_REG_Y   2
#define JN_REG_SP  3
#define JN_REG_PC  4
#define JN_REG_ST  5
#define JN_REG_R0  6
#define JN_REG_R1  7
#define JN_REG_R2  8
#define JN_REG_R3  9
#define JN_REG_R4  10
#define JN_REG_R5  11
#define JN_REG_R6  12
#define JN_REG_R7  13

#define JN_MAX_INST 10

typedef struct JN {
	uint8_t*     Mem;                    // Virtual machine memory
	size_t       MemSize;
	uint32_t     Regs[JN_REGS];
	uint8_t      _fetchBuf[JN_MAX_INST]; // Fetch ring buffer c-buffer
	ERingBuffer  _fetchRB;               // Fetch ring buffer
	uint32_t*    _FP;                    // Fetch pointer
	int          _regLocks[JN_REGS];     // Register pipeline locks
	uint32_t*    _memLocks[2];           // RAM pipeline locks          
} JN;

void jn_init(JN* vm, const void* mem, size_t size);
void jn_tick(JN* vm);

#endif
