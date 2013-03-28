#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>

#define JN_FACILITY "LOGGING"
#include "jnlog.h"

static JNLogLevel _filter = JNLogDebug;
static FILE*      _file   = NULL;
static const char* _levels[] = {
	"DEBUG",
	"WARN",
	"ERR"
};

void jn_log_init(JNLogLevel level) {
	_filter = level;
	_file   = fopen("jn.log", "wb");
	if(!_file) {
		fprintf(stderr, "Could not open log file [%s]\n", strerror(errno));
		return;
	}
	jn_debug("JN Log init");
}

void jn_log(JNLogLevel level, const char* facility, const char* fmt, ...) {
	if(level < _filter) {
		return;
	}
	fprintf(_file, "[%s][%s] ", _levels[level], facility);
	va_list vargs;
	va_start(vargs, fmt);
	vfprintf(_file, fmt, vargs);
	va_end(vargs);
	fputs("\n", _file);
}

void jn_flush() {
	fflush(_file);
}

void jn_close() {
	fclose(_file);
}