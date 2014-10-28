class InteruptStatement(Statement):
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None,lable=None):
		Statement.__init__(self, opcodeName, segment,oprands,locationInSegment,lable)
	def transform(self):
		return {
			16:int16,

		}[]()
	def int16():
		toRet=list()
		toRet.append('keyboard.waitPress({})'.format(p[2]))
		toRet.append('keyboard.lastKey.get(AL)')