class Register():
	def __init__(self,name):
		self.name=name
	def getValue(self):
		return self

registers={
"AL":Register("AL"),\
"AH":Register("AH"),\
"BL":Register("BL"),\
"BH":Register("BH"),\
"CL":Register("CL"),\
"CH":Register("CH"),\
"DL":Register("DL"),\
"DH":Register("DH")
}