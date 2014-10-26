#virtual class
from memoryRow import MemoryRow
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
		Segment.__init__(self,variables,None)
		self.vars={}
		for i, var in enumerate(variables):
			var.inSegmentPosition=i
			self.vars[var.name]=var
	
class CodeSegment(Segment):
	"""the code segment"""
	def __init__(self, statements):
		Segment.__init__(self,statements,None)
		for i ,state in enumerate(statements):
			statements[i].locationInSegment=i
			statements[i].segment=self
	def getAdress(self):
		return 0
	def __str__(self):
		toRet=""
		for x in self.statementList:
			toRet+=str(x)+'\n'
		return toRet+'\n'
	
	def parse(self):
		rows=list()
		rows.append(MemoryRow())
		for statement in self.statementList:
			if statement.lable!=None:
				rows[-1].seal()
				rows.append(MemoryRow())
			try:
				rows[-1].addStatement(statement)
			except MemoryRow.FullException:
				rows[-1].seal()
				rows.append(MemoryRow())
				try:	
					rows[-1].addStatement(statement)
				except MemoryRow.FullException:
					raise Exception("Tue statement %s is too big for this memory")
			statement.inSegmentPosition=len(rows)-1
		rows[-1].seal()
		return rows