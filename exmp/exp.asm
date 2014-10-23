.data
msg	db	"Hello World$"
numbin db 0b00001
numoct db 0123453
numhex db 0x000A1
numun db ?

.code
start:
	mov	ah, 09h   ; Display the message
	lea	dx, msg
	int	21h
	mov	ax, 4C00h  ; Terminate the executable
	int	21h