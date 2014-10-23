import interfaces
class Statement(interfaces.IAdressable):
	'''each new line of assembly code'''
	def __init__(self, opcodeName, segment,oprands,locationInSegment=None):
		'''opcode-the name of the opcode
			adress-the adress in the memory
			'''
		self.opcodeName=opcodeName
		self.adress=adress
		self.oprands=oprands
		self.locationInSegment=locationInSegment
	def getRealAdress():
		raise Exception()