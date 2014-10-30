.data
msg db "Hello World"
.code
mov AL msg
start:
mov AH AL
jmp start