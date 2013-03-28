#include <string.h>

#include "jn.h"

#define JN_FACILITY "CPU"
#include "jnlog.h"

#define PC(vm) (vm)->Regs[JN_REG_PC]
#define SP(vm) (vm)->Regs[JN_REG_SP]
#define A(vm)  (vm)->Regs[JN_REG_A]

static void fetch(JN* vm);
static void decode(JN* vm);
static void execute(JN* vm);

void jn_init(JN* vm, const void* mem, size_t size) {
	jn_debug("Initializing vm");
	memset(vm, 0, sizeof *vm);
	vm->Mem      = (uint8_t*) mem;
	vm->MemSize  = size;
	e_ringbuffer_init(&vm->_fetchRB, vm->_fetchBuf, sizeof(vm->_fetchBuf));
}

void jn_tick(JN* vm) {
	jn_debug("tick %d", PC(vm));
	fetch(vm);
	decode(vm);
	execute(vm);
	PC(vm)++;
}

static void fetch(JN* vm) {
	// See if there's space in prefetch ringbuffer
	if(e_ringbuffer_free(&vm->_fetchRB) < 4) {
		return;
	}
}

static void decode(JN* vm) {

}

static void execute(JN* vm) {

}