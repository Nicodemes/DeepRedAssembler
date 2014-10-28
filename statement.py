import interfaces
from oprands import *
from registers import Register
import types
class Statement(interfaces.IAdressable):
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
	
		command=self.opcodeName.title()
		toRet=list()
		for i,op in enumerate(self.oprands):
			if isinstance(op, EffAdress):
				raise Exception("unimplamented")
			elif isinstance(op, Adress):
				command+="A"
				toRet.append("`Cdu.arg({0},8).set(Literal({1}))`".format(i,op.getAdress()))
			elif isinstance(op,Literal):
				command+="C"
				toRet.append("`Cdu.arg({0},8).set(Literal({1}))`".format(i,op.getValue()))

			elif isinstance(op,Register):
				command+="R"
				toRet.append("`regRef{}.origin({})`".format(i+1,op.name))
		toRet.append(command+"(p[{exit}])")
		return toRet
class LoopStatement(Statement):
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		Statement.__init__(self, opcodeName, segment,oprands,locationInSegment,lable)
	def transform(self):
		toRet=list()
		op=self.oprands[0]
		if isinstance(op, Adress):
			toRet.append("`Cdu.arg(0,8).set(Literal({}))`".format(op.getAdress()))
		elif isinstance(op,Literal):
			toRet.append("`Cdu.arg(0,8).set(Literal({}))`".format(op.getValue()))

		elif isinstance(self.oprands[0],Register):
			raise Exception("loop takes only constatns")
		toRet+=("`RegRef1.origin(counterRegister)`","`DecR(p[3])`","`flags.zero.setFalse()`","`regRef1.checkZero()`","`JzA({exit})`")

		return toRet
