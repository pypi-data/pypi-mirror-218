#File type: extension <Module> set
#By Junxiang H., 2023/07/1
#wacmk.com/cn Tech. Supp.

#This script updates automaticly! Do not Modify!
#Update time:2023-07-11 04:25:54

GUI={}
try:
	try:
		import ShockFinder.Addon.GUI.XUI as XUI
	except:
		import XUI
	GUI["XUI"]=XUI
except Exception as err:
	print("Module: XUI import failure:",err)

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("GUI:")
	for i in GUI.keys():
		print(i,":",GUI[i])
		print("\t",GUI[i].show)