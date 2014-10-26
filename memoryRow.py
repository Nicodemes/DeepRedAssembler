class MemoryRow:
	"""this class represents a row in the memory"""
	def __init__(self, size=8):
		self.size = size
		self.blocks=list()
		self.blocks.append("`p[{exit}]()`")
		self.freeSlots=7
	def addBlock(self,command):
		if not isinstance(command,str):
			raise Exception("command %s must be a string" % command)
		self.freeSlots-=1
		self.blocks.append(command)
	def addStatement(self,statement):
		formed=statement.transform()
		if len(formed) > self.freeSlots:
			raise MemoryRow.FullException()
		self.formatLast(len(formed))
		for block in formed:
			self.addBlock(block)
	def seal(self):
		self.formatLast("Cdu.Fetcher")
		for i in range(self.freeSlots):
			self.blocks.append('')
	def formatLast(self,mexit):
		self.blocks[-1]=self.blocks[-1].format(exit=mexit)
	def __str__(self):
		toRet=""
		for b in self.blocks:
			toRet+="["+b+"]"
		return toRet
	class FullException(Exception):
		pass