#File type: extension <Module> set
#By Junxiang H., 2023/07/1
#wacmk.com/cn Tech. Supp.

#This script updates automaticly! Do not Modify!
#Update time:2023-07-11 04:25:54

Loader={}
try:
	try:
		import ShockFinder.Addon.Loader.Pluto as Pluto
	except:
		import Pluto
	Loader["Pluto"]=Pluto
except Exception as err:
	print("Module: Pluto import failure:",err)

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("Loader:")
	for i in Loader.keys():
		print(i,":",Loader[i])
		print("\t",Loader[i].load)