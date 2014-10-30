.data
msg db "what is up?"
msg2 db 256
.code
mov AL msg
start:
mov AH msg2
jmp start