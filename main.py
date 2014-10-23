from registers import generalPurpase as gpRegisters
import oprands
tokens = (
	'OPCODE','NUMBER','STRING','UNKNOWNVALUE',
	'NAME','DECVAR','SEGMENT','LBRACK','RBRAKC',
	'REGISTER','LABLESIGN'
	)
# Tokens
t_OPCODE      = r'[(mov)(push)(pop)(add)(sub)(inc)(dec)(neg)(lea)(int)(jmp)(jz)(jnz)(je)(loop)(xor)(shl)(shr)]'
t_STRING      =	r'"[\x00-\x7F]+"'
t_UNKNOWNVALUE=	r'\?'
t_NAME        = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LBRACK      = r'\['
t_RBRACK      = r'\]'
t_SEGMENT     =	r'[(\.data)(\.code)]'
t_DECVAR      =	r'[(DB)(db)(DW)(dw)(DD)(dd)]'
t_LABLESIGN	  = r':'

def t_NUMBER(t):
	r'[(\d+)(0[xX][0-9a-fA-F]+)(0[bB][0-1]+)\?]'
	try:
		base = t.value[:2].lower()
		if base =="0b":
			t.value = int(t.value,2)
		elif base == "0x":
			t.value = int(t.value,16)
		elif t.value=='?':
			#TODO: possibility for random
			t.value=0
		else:
			t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t
def t_REGISTER(t):
	r'[A-Da-d][LHlh]?'
	try:
		t.value = gpRegisters[t.value.lower()]
	except KeyError:
		t.value=None
		raise Exception("register name is invlid")
	return t
# Ignored characters
t_ignore = " \t"
def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules
# segments
dataSegment=None
codeSegment=None

def p_segment_data(t):
	'segment : SEGMENT dataList'
	dataSegment=DataSegment(t[2])
	t[0]=dataSegment
def p_varassign(t):
	''' varassign: NAME DECVAR literal'''
	size={"db":1,"dw":2,"dd":4}[t[2].lower()]
	t[0]=oprands.Varialble(t[1],size,t[3])
def p_dataList_single(t):
	'dataList : varassign'
	t[0]=[]
	t[0].append(t[1])
def p_dataList_multi(t):
	'dataList : dataList varassign'
	t[1].append(t[2])
	t[0]=t[1]
def p_oprand_literal(t):
	'''literal : NUMBER
			   | STRING'''
	if isinstance(t[1],str):
		t[0]=oprands.StringLiteral(t[1])
	else:
		t[0]=oprands.Literal(t[1])
def p_oprand_effadress(t):
	'''oprand : LBRACK NUMBER RBRACK
			| LBRACK REGISTER RBRACK '''
	t[0]=oprands.EffAdress(t[2])

def p_statement_labled(t):
	'labled: NAME LABLESIGN expression'
	t[0]=
	
def p_error(t):
	print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

while 1:
	try:
		s = input('calc > ')   # Use raw_input on Python 2
	except EOFError:
		break
	yacc.parse(s)