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
		for i, var in enumerate(variables):
			var.inSegmentPosition=i
			self.vars[var.name]=var
	def __str__(self):
		toRet=""
		for key,variable in self.vars.items():
			toRet+="{} = {} \n".format(key,variables.initValue)
class CodeSegment(Segment):
	"""the code segment"""
	def __init__(self, statements):
		Segment.__init__(self)
		self.statements = statements
		for i ,state in enumerate(statements):
			statements[i].locationInSegment=i