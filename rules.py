from registers import registers
from oprands import *
from statement import *
from segment import *
import sys
import json
from tokenizer import *
from main import options
names={}
def expsegment(l):
	with open(options.outputFile, 'w',newline='') as outfile:
		json.dump(l,outfile)

dataSegment=DataSegment()
codeSegment=None
segmentLocations=[]

unsignedVars=dict()
def p_program(t):
	'''program : segmentList'''
	adict=dict()
	for i,x in enumerate(t[1]):
		try:
			x.setAdress(int(segmentLocations[i+1]))
		except IndexError:
			x.setAdress(None)
		m=list()
		fname=""
		if isinstance(x,CodeSegment):
			for y in x.parse():
				m.append(y.blocks)
			adict[".code"+str(x.ID)]=m
		else:
			m=x.parse()
			adict[".data"+str(x.ID)]=m
		
	expsegment(adict)
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
	'''segment : SEGMENT statementList
			   | SEGMENT dataList'''
	if t[1] == '.data':
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
	'''varassign : ID DECLVAR literal'''
	size= 1
	try:
		size= { "db":1,"dw":2,"dd":4}[t[2].lower()]
	except KeyError:
		raise Exception("the decloration is invalid")
	myVar = Variable(t[1],size,t[3],dataSegment)
	dataSegment.aVar(myVar)
	names[myVar.name]=myVar
	
def p_variable(t):
	"variable : ID"
	try:
		t[0]=names[t[1]]
	except KeyError:
		print("WARNING varible %s is undefined"%t[1])
		t[0]=0
def p_opcode(t):
	"opcode : OPCODE"
	t[0]=t[1]

def p_statement(t):
	'statement : opcode oprandList'
	if t[1]=='loop':
		t[0]=LoopStatement(t[1],codeSegment,t[2])
	elif t[1]=="jmp":
		t[0]=JmpStatement(t[1],codeSegment,t[2])
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
		t[0]=LiteralString(t[1])
	else:
		t[0]=Literal(t[1])
def p_oprand(t):
	'''oprand : variable
			  | literal
			  | REGISTER8
			  | REGISTER16'''
	t[0]=t[1]
def p_oprand_adress(t):
	'oprand : LBRACK literal RBRACK '
	t[0]=Adress(t[2])
def p_oprand_effAdress(t):
	'oprand : LBRACK variable RBRACK'
	t[0]=t[2].getAdress()

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
	print("Syntax error at {} {}".format(t.value, t))


import ply.yacc as yacc
yacc.yacc()
s= open(options.inputFile).read()
yacc.parse(s)