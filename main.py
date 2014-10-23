from registers import generalPurpase as gpRegisters
import oprands
from statement import Statement
tokens = (
	'OPCODE','STRING','UNKNOWNVALUE',
	'NAME','DECVAR','DATASEGMENT','CODESEGMENT','LBRACK','RBRACK',
	'LABLESIGN','COMMENT','BIN','DEC','HEX'
	)
# Tokens
t_OPCODE      = r'[(mov)(push)(pop)(add)(sub)(inc)(dec)(neg)(lea)(int)(jmp)(jz)(jnz)(je)(loop)(xor)(shl)(shr)]'
t_STRING      =	r'"[\x00-\x7F]+"'
t_UNKNOWNVALUE=	r'\?'
t_NAME        = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LBRACK      = r'\['
t_RBRACK      = r'\]'
t_DATASEGMENT =r'\.data'
t_CODESEGMENT= r'\.code'
t_DECVAR      =	r'[(DB)(db)(DW)(dw)(DD)(dd)]'
t_LABLESIGN	  = r':'

def t_BIN(t):
	r'0[bB][0-1]+'
	nv=""
	for i,x in enumerate(t.value):
		if i >1:
			nv+=x
	t.value = int(nv,2)
	return t
def t_HEX(t):
	r'0[xX][0-9a-fA-F]+'
	nv=""
	for i,x in enumerate(t.value):
		if i >1:
			nv+=x
	t.value = int(nv,16)
	return t
def t_DEC(t):
	r'\d+'
	t.value=int(t.value)
	return t
# Ignored characters
t_ignore = " \t"
def t_COMMENT(t):
	r';(.+)\n'
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
names={}
dataSegment=None
codeSegment=None
def p(t):
	'''p : segmentList'''
	for each in t[1]:
		print(str(each))
def p_segmentList(t):
	'''segmentList : segment
				   | segmentList segment'''
	if len(t)==2:
		t[1].appeand(t[2])
	else:
		a=list()
		a.append(t[1])
		t[0]=a
def p_segment(t):
	'segment : DATASEGMENT dataList'
	if t[1] == '.data':
		dataSegment=DataSegment(t[2])
		t[0]=dataSegment
		return dataSegment
	elif t[2]=='.code':
		codeSegment=CodeSegment(t[2])
		return codeSegment
	else:
		raise Exception("initValue segment type")
		
def p_dataList(t):
	'''dataList : varassign
				| dataList varassign'''
	if len(t)==2:
		t[0]=list()
		t[0].append(t[1])
	else:
		t[1].append(t[2])
		t[0]=t[1]
def p_varassign(t):
	''' varassign : NAME DECVAR literal'''
	size={"db":1,"dw":2,"dd":4}[t[2].lower()]
	myVar=oprands.Varialble(t[1],size,t[3])
	names[t[1]]=myVar
	t[0]=myVar
def p_variable(t):
	"variable : NAME"
	t[0]=names[t[1]].getValue()

def p_statement_labled(t):
	'statement : NAME LABLESIGN statement'
	myLable=oprands.Lable(t[1],t[3])
	names[t[1]]=myLable
def p_statement(t):
	'statement : OPCODE oprandList'
	t[0]=Statement(t[1],codeSegment,oprandList)

def p_oprandList(t):
	'''oprandList : oprand
				  | oprandList oprand'''
	if len(t)==2:
		t[0]=list()
		t[0].append(t[1])
	else:
		t[1].append(t[2])
		t[0]=t[1]
def p_oprand_literal(t):
	'''literal : DEC
			   | HEX
			   | BIN
			   | STRING'''
	if isinstance(t[1],str):
		t[0]=oprands.StringLiteral(t[1])
	else:
		t[0]=oprands.Literal(t[1])
def p_oprand_var(t):
	"oprand : variable"
	t[0]=t[1]
def p_oprand_effadress(t):
	'''oprand : LBRACK literal RBRACK 
			  | LBRACK variable RBRACK'''
	t[0]=t[2].getEffValue()


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