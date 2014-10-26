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
		return self.segment.getAdress() + self.locationInSegment	
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
			if isinstance(op,Oprand):
				command+="C"
				toRet.append("`Cdu.arg({0},8).set(Literal({1}))`".format(i,op.getValue()))

			elif isinstance(op,Register):
				command+="R"
				toRet.append("`RegRef{}.origin({})`".format(i+1,op.name))
		toRet.append(command+"(p[{exit}])")
		return toRet
class LoopStatement(Statement):
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		Statement.__init__(self, opcodeName, segment,oprands,locationInSegment,lable)
	def transform(self):
		toRet=list()
		if isinstance(self.oprands[0],Literal):
			toRet.append("Cdu.arg(0,8).set(Literal({value})".format(value=self.oprands[0].getValue()))
		elif isinstance(self.oprands[0],Register):
			raise Exception("loop takes only constatns")
		toRet+=("RegRef1.origin(counterRegister)","DecR(p[{exit}])","flags.zero.setFalse()","RegRef1.checkZero()","JzC({exit})")

		return toRet