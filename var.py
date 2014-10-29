class Variable:
	'''a variable that is defined in the .data segment, can be refferd from the .code segment '''
	def __init__(self,name,size,initValue,segment,inSegmentPosition=None):
		print("variable was created")
		self.name=name
		self.size=size
		self.initValue=initValue
		self.segment=segment
		self.inSegmentPosition=inSegmentPosition
class UnsignedVar:
	def __init__(self,name):
		self.name=name