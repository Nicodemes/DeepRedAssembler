class Oprand:
	#virtual
	def getValue(self):
		return self.value
	def getEffValue(self):
		return self.eff(self.getValue())
	def eff(self,value):
		return value
	def __str__(self):
		return str(self.value)

class Literal(Oprand):
	def __init__(self,value):
		self.value=value
	

class LiteralString(Literal):
	"""docstring for  LiterString"""
	def __init__(self, value):
		Literal.__init__(self,value)
	def getValue(self):
		return self.value[0]

class Holder(Oprand):
	'''[abstract] the value that the hallder have is allways effictive adress.'''
	pass
class Variable(Holder):
	'''a variable that is defined in the .data segment, can be refferd from the .code segment '''
	def __init__(self,name,size,initValue,segment,inSegmentPosition=None):
		print("variable was created")
		self.name=name
		self.size=size
		self.initValue=initValue
		self.segment=segment
		self.inSegmentPosition=inSegmentPosition
class Lable(Oprand):
	"""lable in the code"""
	def __init__(self,name,linkedStatement):
		'''position=the posiotion to which the cpu jumps if jmp lable is called'''
		self.name = name
		self.linkedStatement=linkedStatement
	def getAdress(self):
		return self.linkedStatement.getAdress()
	def getValue(self):
		return self.getAdress()
	def __str__(self):
		return self.name+"[{}]:".format(self.getAdress())