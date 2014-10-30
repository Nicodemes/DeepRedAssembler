from interfaces import IAdressable
class Oprand:
	#virtual
	def getValue(self):
		return self.value

class Literal(Oprand):
	def __init__(self,value):
		self.value=value
class LiteralString(Literal):
	"""docstring for  LiterString"""
	def __init__(self, value):
		Literal.__init__(self,value)
	def getValue(self):
		return self.value[0]

class Adress(Oprand,IAdressable):
	def __init__(self,adress):
		if isinstance(adress, Literal):
			adress=adress.getValue()
		self.adress=adress
	def getAdress(self):
		return self.adress

class Lable(Oprand,IAdressable):
	"""lable in the code"""
	def __init__(self,name,linkedStatement):
		'''position=the posiotion to which the cpu jumps if jmp lable is called'''
		self.name = name
		self.linkedStatement=linkedStatement
	def getAdress(self):
		return self.linkedStatement.getAdress()
	def __str__(self):
		return self.name+"[{}]:".format(self.getAdress())
class Variable(Oprand,IAdressable):
	'''a variable that is defined in the .data segment, can be refferd from the .code segment '''
	def __init__(self,name,size,initValue,segment,inSegmentPosition=None):
		self.name=name
		self.size=size
		self.initValue=initValue
		self.segment=segment
		self.inSegmentPosition=inSegmentPosition
	def __str__(self):
		return "Variable[name:'{name}' ,value:'{value}' ]".format(name=self.name,value=str(self.initValue))
	def getAdress(self):
		x=self.segment.getAdress()
		if isinstance( x, str):
			return x + "+"+str(self.inSegmentPosition)	
		return x + self.inSegmentPosition