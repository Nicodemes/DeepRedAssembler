from registers import registers 
tokens = (
	'DECLVAR','REGISTER8','REGISTER16',
	'OPCODE','STRING','UNKNOWNVALUE','ID',
	'SEGMENT','LBRACK','RBRACK',
	'LABLE','COMMENT','BIN','DEC','HEX',"CURLR","CURLL","MACHINE"
	)
# Tokens
t_UNKNOWNVALUE=	r'\?'
t_LBRACK      = r'\['
t_RBRACK      = r'\]'
t_SEGMENT     = r'\.data|\.code'
t_CURLL		  =r'}'
t_CURLR		  =r'{'
t_MACHINE     = r'>[\x00-\x7F]*\n'
reserved={}

def reserve(alist,category,capitalise=True):
	for item in alist:
		reserved[item]=category
		if capitalise:
			reserved[item.upper()]=category

#reserved opcodes
opcodes=["mov","push","pop","add","sub","inc","dec","neg","lea","int","jmp","jz","jnz","je","loop","xor","shl","shr"]	
reserve(opcodes,"OPCODE")
declorators=["db","dw","dd","ds"]
reserve(declorators,"DECLVAR",False)
regbase=['a','b','c','d']
reg8=[]
reg16=[]
for c in regbase:
	reg8+=[c+"l",c+"h"]
	reg16.append(c+"x")
reserve(reg8,"REGISTER8")
reserve(reg16,"REGISTER16")

def t_BIN(t):
	r'0[bB][10]+'
	t.value = int(t.value.lower().split('b')[1],2)
	return t
def t_HEX(t):
	r'0[xX][0-9a-fA-F]+'
	t.value = int(t.value.lower().split('x')[1],16)
	return t
def t_DEC(t):
	r'[1-9][0-9]*'
	t.value=int(t.value)
	return t

def t_STRING(t):
	r'\"[\x00-\x7F]*\"'
	t.value=t.value.split("\"")[1]
	return t
# Ignored characters
t_ignore = " \t"
def t_ignore_COMMENT(t):
	r';.+\n'
	pass
def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
def t_LABLE(t) :
	r'[a-zA-Z_][a-zA-Z0-9_]*:'
	t.value=t.value.split(":")[0]
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	try:
		t.type = reserved[t.value] # Check for reserved
		if t.type == "REGISTER8":
			t.value=registers[t.value]
	except KeyError:
		t.type="ID"
	return t
# Build the lexert[0]
import ply.lex as lex
lex.lex()
