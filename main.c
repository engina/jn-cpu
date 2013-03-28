#include <stdio.h>

#include "jn.h"
#include "jnlog.h"

int main(void) {
	char mem[1024];
	JN vm;
	jn_log_init(JNLogDebug);
	jn_init(&vm, mem, sizeof mem);
	for(int i = 0; i < 100; i++) {
		jn_tick(&vm);
	}
	return 0;
}