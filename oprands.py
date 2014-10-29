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

class EffAdress(Oprand):
	def __init__(self,adress):
		self.adress=adress
class Adress(Oprand):
	def __init__(self,adress):
		if isinstance(adress, Literal):
			adress=adress.getValue()
		self.adress=adress
	def getAdress(self):
		return self.adress
class Lable(Adress):
	"""lable in the code"""
	def __init__(self,name,linkedStatement):
		'''position=the posiotion to which the cpu jumps if jmp lable is called'''
		self.name = name
		self.linkedStatement=linkedStatement
	def getAdress(self):
		return self.linkedStatement.getAdress()
	def __str__(self):
		return self.name+"[{}]:".format(self.getAdress())