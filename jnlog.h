#ifndef JN_LOG_H
#define JN_LOG_H

#ifndef JN_FACILITY
#define JN_FACILITY ""
#endif

typedef enum JNLogLevel {
	JNLogDebug = 0,
	JNLogWarn  = 1,
	JNLogError = 2
} JNLogLevel;

void jn_log_init(JNLogLevel level);
void jn_log(JNLogLevel level, const char* facility, const char* fmt, ...);
void jn_flush();
void jn_close();

#define jn_debug(...) jn_log(JNLogDebug, JN_FACILITY, __VA_ARGS__)
#define jn_warn(...)  jn_log(JNLogWarn,  JN_FACILITY, __VA_ARGS__)
#define jn_error(...) jn_log(JNLogError, JN_FACILITY, __VA_ARGS__)

#endif
