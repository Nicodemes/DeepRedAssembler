class Oprand:
	#virtual
	def getValue(self):
		return self.value
	def getEffValue(self):
		raise self.eff(self.getValue())

class Literal(Oprand):
	def __init__(self,value):
		self.value=value
class LiterString(Listeral):
	"""docstring for  LiterString"""
	def __init__(self, arg):
		super(LiterString, self).__init__(arg)
	def getValue(self):
		return self.value[0]

class RelatedAdress(Oprand):
	"""used for labels and the posiotions of the opcodes"""
	def __init__(self, value):
		Oprand.__init__(self.value)
	def getValue(self,reloation_adress):
		'''gets the value by realting to a base adress'''
		return self.value+reloation_adress
class Holder(Oprand):
	'''[abstract] the value that the hallder have is allways effictive adress.'''
	pass
class Variable(Holder):
	'''a variable that is defined in the .data segment, can be refferd from the .code segment '''
	def __init__(self,name,size,initValue,adress=None):
		self.name=name
		self.size=size
		self.initValue=initValue
		self.adress=adress

class Lable:
	"""lable in the code"""
	def __init__(self,name,position=RelatedAdress(0)):
		'''position=the posiotion to which the cpu jumps if jmp lable is called'''
		self.name = name
		self.position = position
		