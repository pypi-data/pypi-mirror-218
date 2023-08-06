#File type: extension <Module> set
#By Junxiang H., 2023/07/1
#wacmk.com/cn Tech. Supp.

#This script updates automaticly! Do not Modify!
#Update time:2023-07-11 04:25:54

Painter={}
try:
	try:
		import ShockFinder.Addon.Painter.Line as Line
	except:
		import Line
	Painter["Line"]=Line
except Exception as err:
	print("Module: Line import failure:",err)

try:
	try:
		import ShockFinder.Addon.Painter.Surface as Surface
	except:
		import Surface
	Painter["Surface"]=Surface
except Exception as err:
	print("Module: Surface import failure:",err)

try:
	try:
		import ShockFinder.Addon.Painter.Basic as Basic
	except:
		import Basic
	Painter["Basic"]=Basic
except Exception as err:
	print("Module: Basic import failure:",err)

try:
	try:
		import ShockFinder.Addon.Painter.P2D as P2D
	except:
		import P2D
	Painter["P2D"]=P2D
except Exception as err:
	print("Module: P2D import failure:",err)

try:
	try:
		import ShockFinder.Addon.Painter.P3D as P3D
	except:
		import P3D
	Painter["P3D"]=P3D
except Exception as err:
	print("Module: P3D import failure:",err)

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("Painter:")
	for i in Painter.keys():
		print(i,":",Painter[i])
		print("\t",Painter[i].info)