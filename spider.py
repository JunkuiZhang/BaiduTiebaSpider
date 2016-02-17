import requests
from bs4 import BeautifulSoup
import re

url0 = input("Enter url: ")
if len(url0) < 1:
	url0 = "http://tieba.baidu.com/p/3708347889?see_lz=1&pn="

p = 1
url1 = url0 + "1"
conn = requests.get(url1)
data = conn.text
soup = BeautifulSoup(data, "html.parser")
ps = soup.find_all("span", class_ = "red")[1]
p_max = re.findall(">([0-9]+)<", str(ps))[0]
num = 0
img_lib = list()
path = "F:\\BigData\\Pic\\Pic_"

while p <= int(p_max):
	url = url0 + "%s" % p
	conn = requests.get(url)
	data = conn.text
	soup = BeautifulSoup(data, "html.parser")
	p += 1

	all0 = soup.find_all("cc")
	imgs = BeautifulSoup(str(all0), "html.parser").find_all("img", class_ = "BDE_Image")

	for img in imgs:
		img = str(img)
		if len(re.findall('<br>', img)) > 0:
			img = img.split("<br>")
			for i in img:
				src = re.findall('src="(.*)" w', i)[0]
				img_lib.append(src)
		else:
			src = re.findall('src="(.*)" w', img)[0]
			img_lib.append(src)

img_lib_ = []
for img in img_lib:
	if img not in img_lib_:
			img_lib_.append(img)
img_lib = img_lib_
print(len(img_lib))
for img in img_lib:
	name = path + "%s.jpg" % num
	num += 1
	conn = requests.get(img)
	f = open(name, "wb")
	f.write(conn.content)
	f.close()
	print("Saved %s pictures." % num)

print("======================================================")
print("Finished with %s pictures." % num)
print("======================================================")