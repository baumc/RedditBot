from lxml import html
import requests

temp = ''

p = requests.get('http://information.mobiusfinalfantasy.com/ne/sp/')
t = html.fromstring(p.content)
links = t.xpath('//li[@class="entry"]/a/@href')
names = t.xpath('//li[@class="entry"]/a/h4/text()')
for l,n in zip(links, names):
	if "2016/09" in n:
		temp += "[**"+n.strip()+"**]("+l+")"
		print temp
