#virtual class
from memoryRow import MemoryRow
from oprands import *
class Segment:
	def __init__(self,statementList,startAdress):
		self.statementList=statementList
		self.parse
		self.setAdress(startAdress)
		
	def getAdress(self):
		return self.adress
	def setAdress(self,newAdress):
		if newAdress==None:
			self.adress="\a"
		else:
			self.adress=newAdress
	def __str__(self):
		toRet=""
		for x in self.statementList:
			toRet+=str(x)+'\n'
		return toRet+'\n'
class DataSegment(Segment):
	def __init__(self):
	def addVariable(self,var):
	def parse(self):
		toRet=list()
		for var in self.statementList:
			toRet+=DataSegment.parseInit(var)
		return toRet
	def parseInit(var):
		toRet=list()
		if isinstance(var.initValue,LiteralString):
			for c in var.initValue.value:
				toRet.append(ord(c))
		elif isinstance(var.initValue, Literal):
			toRet.append(var.initValue.value)
		return toRet
class CodeSegment(Segment):
	"""the code segment"""
	def __init__(self, statements):
		Segment.__init__(self,statements,None)
		for i ,state in enumerate(statements):
			state.locationInSegment=i
			state.segment=self
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