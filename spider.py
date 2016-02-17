import requests
from bs4 import BeautifulSoup
import re
import os

class Tiezi:
	def __init__(self, url, path):
		__url = url + "1"
		self.url = url
		self.path = path
		__conn = requests.get(__url)
		__data = __conn.text
		self.soup = BeautifulSoup(__data, "html.parser")

	__slots__ = ("url", "path", "soup")

	def get_maxpage(self):
		__pagenum = self.soup.find_all("span", class_ = "red")[1]
		__maxpage = re.findall(">([0-9]+)<", str(__pagenum))[0]
		return __maxpage

	def get_name(self):
		__content = self.soup.find_all("h3")[0]
		__soup = BeautifulSoup(str(__content), "html.parser")
		return __soup.h3["title"]

	def work(self):
		__path = self.path + "\\" + self.get_name()[:12] + "\\"
		__page = 1
		__imglib = list()
		__savenum = 1
		while __page <= int(self.get_maxpage()):
			__url = self.url + "%s" % __page
			__conn = requests.get(__url)
			__data = __conn.text
			__soup = BeautifulSoup(__data, "html.parser")
			__page += 1

			__all0 = __soup.find_all("cc")
			__imgs = BeautifulSoup(str(__all0), "html.parser").find_all("img", class_ = "BDE_Image")

			for img in __imgs:
				__img = str(img)
				if len(re.findall('<br>', __img)) > 0:
					__img = __img.split("<br>")
					for i in __img:
						__src = re.findall('src="(.*)" w', i)[0]
						__imglib.append(__src)
				else:
					__src = re.findall('src="(.*)" w', __img)[0]
					__imglib.append(__src)

		__img_lib = []
		for img in __imglib:
			if img not in __img_lib:
					__img_lib.append(img)
		__imglib = __img_lib
		print(len(__imglib))

		if not os.path.exists(__path):
			os.mkdir(__path)

		for img in __imglib:
			__name = __path + "%s.jpg" % __savenum
			__savenum += 1
			__conn = requests.get(img)
			__f = open(__name, "wb")
			__f.write(__conn.content)
			__f.close()
			print("Saved %s pictures." % __savenum)

		print("======================================================")
		print("           Finished with %s pictures." % __savenum)
		print("======================================================")

while True:
	url0 = input("Enter url: ")
	path = input("Enter saving path: ")

	if len(url0) < 1:
		url0 = "http://tieba.baidu.com/p/3708347889?see_lz=1&pn="
	else:
		url0 += "?see_lz=1&pn="

	if len(path) < 1:
		path = "F:\\BigData\\Pic"

	try:
		requests.get(url0)
	except:
		print("==========Invalid url input=========")
		continue
	t = Tiezi(url0, path)
	t.work()