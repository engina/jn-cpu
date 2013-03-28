#define FOO 0x5000
#include "../jn/some.inc"
#bar
; some comments
main
    ; some indented comment
    mov     X, 0x5000
    mov     X, FOO
    mov     X, *FOO
    mov     X,#FOO ; inline comments
    mov     X, FOO + SP
    mov     X, FOO + SP + 5
    mov     X, INC_DEF
    cmp     X, 0x5000
    call    foo
    nop
    jmp     main