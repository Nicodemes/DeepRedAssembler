from registers import generalPurpase as gpRegisters
from oprands import *
from statement import *
from segment import *
import sys
import registers
import json

def exp(l,outputfilename):
	with open(outputfilename, 'w',newline='') as outfile:
		json.dump(l, outfile)
tokens = (
	'OPCODE','STRING','UNKNOWNVALUE','NAME',
	'DECLVAR','SEGMENT','LBRACK','RBRACK',
	'LABLE','COMMENT','BIN','DEC','HEX','VARNAME'
	)
# Tokens

t_STRING      =	r'\"[\x00-\x7F]+\"'
t_UNKNOWNVALUE=	r'\?'
t_NAME        = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LBRACK      = r'\['
t_RBRACK      = r'\]'
t_DECLVAR      =r'db'
t_OPCODE      =	r'mov|push|pop|add|sub|inc|dec|neg|lea|int|jmp|jz|jnz|je|loop|xor|shl|shr'

t_SEGMENT     = r'\.data|\.code'
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
# Ignored characters
t_ignore = " \t"
def t_COMMENT(t):
	r';.+\n'
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
# Build the lexert[0]
import ply.lex as lex
lex.lex()

# Parsing rules
# segments
names={}
names.update(registers.generalPurpase)
opnames = {"mov":1, "push":1, "pop":1, "add":1, "sub":1,\
	"inc":1, "dec":1, "neg":1, "lea":1, "int":1, "jmp":1, "jz":1,\
	"jnz":1, "je":1, "loop":1, "xor":1, "shl":1, "shr":1}
dataSegment=None
codeSegment=None
segmentLocations=sys.argv
def p_program(t):
	'''program : segmentList'''
	m=list()
	for i,x in enumerate(t[1]):
		try:
			x.setAdress(int(segmentLocations[i+1]))
		except IndexError:
			x.setAdress(None)
		for y in x.parse():
			m.append(y.blocks)
	exp(m,"E:\\cs\\proj\\DeepRedAssembler\\bin\\out\\program.json")
def p_segmentList(t):
	'''segmentList : segment
				   | segmentList segment'''
	try:
		myVar=t[2]
		t[1].append(myVar)
		t[0]=t[1]
	except IndexError:
		t[0]=list()
		t[0].append(t[1])
def p_segment(t):
	'''segment : SEGMENT statementList'''
	if t[1] == '.data':
		dataSegment=DataSegment(t[2])
		t[0]=dataSegment
		
	elif t[1]=='.code':
		codeSegment=CodeSegment(t[2])
		t[0]=codeSegment
	else:
		raise Exception("invalid segment type")
def p_dataList(t):
	'''dataList : varassign
				| dataList varassign'''
	
	try:
		myVar=t[2]
		t[1].append(t[2])
		t[0]=t[1]
		
	except IndexError:
		t[0]=list()
		t[0].append(t[1])
		
def p_varassign(t):
	'''varassign : VARNAME DECLVAR literal'''
	size= 1
	try:
		size= { "db":1,"dw":2,"dd":4}[t[2].lower()]
	except KeyError:
		raise Exception("the decloration is invalid") 
	myVar = Variable(t[1],size,t[3],dataSegment)
	names[t[1]]=myVar
	t[0]=myVar
def p_variable(t):
	"variable : NAME"
	try:
		t[0]=names[t[1]]
	except KeyError:
		t[0]=t[1]

def p_opcode(t):
	"opcode : OPCODE"
	try:
		if not opnames[t[1].lower()]:
			raise Exception("the opcode %s is currently inactive" % t[1])

		t[0]=t[1].lower()
	except KeyError:
		raise Exception("the opcode %s is invalid" % t[1])
def p_statement(t):
	'statement : opcode oprandList'
	if t[1]=='loop':
		t[0]=LoopStatement(t[1],codeSegment,t[2])
	else:
		t[0]=Statement(t[1],codeSegment,t[2])
def p_statement_labled(t):
	'statement : LABLE statement'
	myLable=Lable(t[1],t[2])
	names[t[1]]=myLable
	t[2].lable=myLable
	t[0]=t[2]
def p_statementList(t):
	'''statementList : statement
					 | statementList statement'''
	try:
		state=t[2]
		state.locationInSegment=len(t[1])
		t[1].append(state)
		t[0]=t[1]
	except IndexError:
		t[0] = list()
		t[1].locationInSegment=0
		t[0].append(t[1])
		

def p_literal(t):
	'''literal : DEC
			   | HEX
			   | BIN
			   | STRING'''
	if isinstance(t[1],str):
		t[0]=StringLiteral(t[1])
	else:
		t[0]=Literal(t[1])
def p_oprand(t):
	'''oprand : variable
			  | literal'''
	t[0]=t[1]
def p_oprand_adress(t):
	'oprand : LBRACK literal RBRACK '
	t[0]=Adress(t[2])
def p_oprand_effAdress(t):
	'oprand : LBRACK variable RBRACK'
	t[0]=EffAdress(t[2])
def p_oprandList(t):
	'''oprandList : oprand
				  | oprandList oprand'''
	if len(t)==2:
		t[0]=list()
		t[0].append(t[1])
	else:
		t[1].append(t[2])
		t[0]=t[1]
def p_error(t):
	print("Syntax error at {}".format(t.value))

import ply.yacc as yacc
yacc.yacc()

s= open("E:/cs/proj/DeepRedAssembler/bin/in/test.asm").read()
yacc.parse(s)
