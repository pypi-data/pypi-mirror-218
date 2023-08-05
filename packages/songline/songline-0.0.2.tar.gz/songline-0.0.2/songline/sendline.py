import requests

class Sendline:
	'''
	#download sticker https://uncle-engineer.com/api/sticker.pdf

	#generate token from https://notify-bot.line.me/my/
	Example:
	----------------------------------
	token = 'xdkakfdjksjdfayfdyaodf'
	messenger = Sendline(token)

	#send message
	messenger.sendtext('Hello world')

	#send sticker
	messenger.sticker(1,1)

	#send image
	messenger.sendimage('https://img.pngio.com/python-logo-python-logo-png-268_300.png')
	----------------------------------
	'''

	def __init__(self,tok):
		self.tok = tok

	def Lineconfig(self,command):
		url = 'https://notify-api.line.me/api/notify'
		token = self.tok ## EDIT
		header = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
		return requests.post(url, headers=header, data = command)

	def sendtext(self,message):
		# send plain text to line
		command = {'message':message}
		return self.Lineconfig(command)


	def sticker(self,sticker_id,package_id,message=' '):
		command = {'message':message,'stickerPackageId':package_id,'stickerId':sticker_id}
		return self.Lineconfig(command)


	def sendimage(self,url):
		command = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
		return self.Lineconfig(command)
	
	def sendimage_file(self,path,text=None):
		url = "https://notify-api.line.me/api/notify"
		file = {'imageFile':open(path,'rb')}

		if text == None:
			text=''
		data = ({
				'message':'\n{}'.format(text)
			})
		LINE_HEADERS = {"Authorization":"Bearer "+self.tok}
		session = requests.Session()
		r=session.post(url, headers=LINE_HEADERS, files=file, data=data)


if __name__ == '__main__':
	
	token = 'DGkp9la8GAjzJ6mVNbgLaetHRm8a25H3xPV7'
	messenger = Sendline(token)

	#send message
	# messenger.sendtext('Hello world')

	#send sticker
	# messenger.sticker(1,1)

	#send image
	# messenger.sendimage('https://img.pngio.com/python-logo-python-logo-png-268_300.png')

	#messenger.sendimage_file(r'C:\Users\Uncle Engineer\Desktop\PythonFile\songline-master\songline-master\songline\sample.png')