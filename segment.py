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
	
	def __str__(self):
		toRet=""
		for x in self.statementList:
			toRet+=str(x)+'\n'
		return toRet+'\n'
class DataSegment(Segment):
	count=0
	def __init__(self):
		self.ID=DataSegment.count
		DataSegment.count+=1
		Segment.__init__(self,list(),None)
		self.nextLocation=0
		self.statementList=list()
	def aVar(self, x):
		self.statementList.append(x)
		x.inSegmentPosition=self.nextLocation
		x.segment=self
		if isinstance(x,LiteralString):
			self.nextLocation+=len(x.value)
		else:
			self.nextLocation+=x.size
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
	def setAdress(self,newAdress):
		if not newAdress:
			self.adress="{data"+str(self.ID)+"}"
		else:
			self.adress=newAdress
class CodeSegment(Segment):
	count=0
	"""the code segment"""
	def __init__(self, statements):
		self.ID=CodeSegment.count
		CodeSegment.count+=1
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
					raise Exception("Tue statement %s is too big for this memory"%str(statement))
			statement.inSegmentPosition=len(rows)-1
		rows[-1].seal()
		return rows
	def setAdress(self,newAdress):
		if not newAdress:
			self.adress="{data"+str(CodeSegment.count)+"}"
		else:
			self.adress=newAdress