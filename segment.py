#virtual class
class Segment:
	def __init__(self,statementList,startAdress):
		self.statementList=statementList
		self.parse
		self.startAdress=startAdress
	#virtual function
	def parse(self):
		for statement in self.statementList:
			print(str(statement))
class DataSegment(Segment):
	def __init__(self,variables):
		self.vars={}
		for var in variables:
			self.vars[var.name]=var