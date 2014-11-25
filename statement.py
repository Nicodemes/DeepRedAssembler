from interfaces import IAdressable
from oprands import *
from registers import Register
import types
class Statement(IAdressable):
	'''each new line of assembly code'''
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		'''opcode-the name of the opcode
			adress-the adress in the memory
			'''
		self.opcodeName=opcodeName
		self.segment=segment
		self.oprands=oprands
		self.locationInSegment=locationInSegment
		self.lable=lable

	def getAdress(self):
		x=self.segment.getAdress()
		if isinstance( x, str):
			return x + "+"+str(self.locationInSegment)
		return x + self.locationInSegment
	def __str__(self):
		if self.lable != None:
			toRet=str(self.lable)+" "
		else:
			toRet=""
		toRet+=self.opcodeName

		for x in self.oprands:
			toRet+=' '+str(x)
		return toRet

	def transform(self): 
		'''retuns an array of the cmd commands'''
		command="`"
		command+=self.opcodeName.title()
		
		toRet=list()
		#HACK
		if(self.opcodeName=='mov' and isinstance(self.oprands[1],Literal) and not isinstance(self.oprands[1],IAdressable)):
			toRet.append("`{}.set(Literal({}))`".format(self.oprands[0].name,self.oprands[1].getValue()))
			toRet.append("`{exit}()`")
			return toRet
		for i,op in enumerate(self.oprands):
			if isinstance(op, IAdressable):
				command+="A"
				toRet.append("`Cdu.arg({0},8).set(Literal({1}))`".format(i,op.getAdress()))
			elif isinstance(op,Literal):
				command+="C"
				toRet.append("`Cdu.arg({0},8).set(Literal({1}))`".format(i,op.getValue()))
			elif isinstance(op,Register):
				command+="R"
				toRet.append("`regRef{}.origin({})`".format(i+1,op.name))
		if command=="`MovAR":
			command="`MovMdR"
		if command=="`MovRA":
			command="`MovRdM"
		toRet.append(command+"({exit})`")
		return toRet
class LoopStatement(Statement):
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		Statement.__init__(self, opcodeName, segment,oprands,locationInSegment,lable)
	def transform(self):
		toRet=list()
		op=self.oprands[0]
		if isinstance(op, IAdressable):
			toRet.append("`Cdu.arg(0,8).set(Literal({}))`".format(op.getAdress()))
		elif isinstance(op,Literal):
			toRet.append("`Cdu.arg(0,8).set(Literal({}))`".format(op.getValue()))
		else:
			raise Exception("loop takes only constatns")
		toRet+=("`RegRef1.origin(counterRegister)`","`DecR(p[3])`","`flags.zero.setFalse()`","`regRef1.checkZero()`","`JzA({exit})`")

		return toRet
class JmpStatement(Statement):
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		Statement.__init__(self, opcodeName, segment,oprands,locationInSegment,lable)
		if len(oprands)>1:
			raise Exception("jmp statement resive only 1 oprand")
	def transform(self):
		toRet=list()
		op=self.oprands[0]
		if isinstance(op, IAdressable):
			toRet.append("`Cdu.arg(0,8).set(Literal({}))`".format(op.getAdress()))
		elif isinstance(op,Literal):
			toRet.append("`Cdu.arg(0,8).set(Literal({}))`".format(op.getValue()))
		else:
			raise Exception("loop takes only constatns")
		toRet.append("'JmpA({exit})")
		return toRet

class IntStatement(Statement):
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		Statement.__init__(self, opcodeName, segment,oprands,locationInSegment,lable)
	def transform(self):
		num=self.oprands[0]
		if not isinstance(num, Literal):
			raise SyntaxError("int oprand must be a number")
		if len(self.oprands)!=1:
			raise SyntaxError("unimplamented more then 1 oprand for int")
		num=num.getValue()
		return {
			22:self.iKeyboard,
			16:self.iScreen,
		}[num]()
	def iKeyboard(self):
		return ['keyboard.plant(p[1]())','keyboard.tmp.get(AL)','{exit}()']
	def iScreen(self):
		return ['/say [ERROR] screen is unimplamented','{exit}()']
class RawStatement(Statement):
	#TODO:make a raw statment a machine statemnt list instead
	def __init__(self,raw,segment):
		locationInSegment=None
		self.segment=segment
		self.raw=raw
		self.lable=None
	def transform(self):
		return [self.raw,"`{exit}()`"]
	def __str__(self):
		return [self.raw,"`{exit}`"]
