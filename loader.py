#loades an assembled file into an image file
import json
import ntpath
class ImageFile:
	def __init__(self,fileName):
		self.path=fileName
		self.slots=json.loads(open(self.path).read())
		print("loading to '{}'({} bytes).".format(ntpath.basename(self.path),len(self.slots)))
	def save(self):
		with open(self.path, 'w',newline='') as outfile:
				json.dump(self.slots,outfile)
	def reset(self):
		self.slots=[0]*256
		self.save()
class Program:
	def __init__(self,fileName,posiotins):
		self.path=fileName
		f=open(fileName,'r').read()
		self.adict=json.loads(f)
		self.segs=posiotins
	def getBaseName(self):
		return 
	def loadSegment(self,name,img):
		toLoad=self.adict["."+name]
		stype="."+name[:4]
		if stype==".code":
			for i , row in enumerate(toLoad):
				if not isinstance(row,list):
					row=[None] * 8
				for j,block in enumerate(row):
					if isinstance(block, str):
						try:
							row[j] = block.format(**self.segs)
						except KeyError:
							continue
				adress=self.segs[name]+i
				img.slots[adress]=row
				print("loading \n\t{}\nto -->adress {} ".format(str(row),adress))
		elif stype==".data":
			for i , byte in enumerate(toLoad):
				adress=self.segs[name]+i
				print("loading {} to adress {}".format(byte,adress))
				img.slots[adress]=byte
			
		img.save()
	def getSegmentNames(self):
		toRet=list()
		for key,value in self.adict.items():
			print(key)
			toRet.append(key)
		return toRet
def lod(program,image,segmentlocations):
	img=ImageFile(image)
	img.reset()
	prog=Program(program,segmentlocations)
	for segname,adress in segmentlocations.items():
		prog.loadSegment(segname,img)
	print("done")
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--img","--image","--imageFile",
                  action="store", type="string", dest="img")
parser.add_option("-b", "--bin","--program",
                  action="store", type="string", dest="bin")
parser.add_option("-s", "--seg","--segments",
                  action="store", type="string", dest="segs")
(options, args) = parser.parse_args()
lod(options.bin,options.img,{'code0':0,'data0':20})
