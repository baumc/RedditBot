import praw, time, re, requests, urllib2, HTMLParser
from pprint import pprint
from datetime import datetime, timedelta
from time import gmtime,strftime
from lxml import html

class Mobius_FF_Bot(object):
	def __init__(self):
		self.userAgent = 'PRAW:Mobius_FF_Bot:v1.2 (by /u/Devoto17)'
		self.username = 'UNAME'
		self.password = "PWRD"
		self.sub = ''
		#server time - a day so it updates in case its been down for a bit
		self.t = datetime.now() - timedelta(1)
		self.sidebar = ''
		self.events = ''

	def connect_to_reddit(self):
		r = praw.Reddit(self.userAgent)
		r.login(self.username,self.password, disable_warning=True)
		self.sub = r.get_subreddit('echoff')
		return r
	
	def get_sidebar(self, r):
		self.sidebar =  self.sub.get_wiki_page("index/edit_sidebar").content_md

	def save_sidebar(self, r):
		self.sub.edit_wiki_page("config/sidebar", self.sidebar)

	def update_sidebar_servertime(self, r):
		t = datetime.utcnow() - timedelta(hours=8)
		self.sidebar = re.sub(r">>######SERVERTI.*", t.strftime("%b %d, %A %I:%M %p"), self.sidebar)
		return t

	def update_seed_bonus(self, r):
		print("Updating Seed Bonus Highlight!")
		if( self.t.weekday()== 6):
			pprint("its Sunday!")
			day = "[Sunday - All](#prismaticseed)"
		if(self.t.weekday() == 0):
			pprint("its Monday!")
			day = "[Monday - Dark](#darkseed)"
		if(self.t.weekday() == 1):
			pprint("its Tuesday!")
			day = "[Tuesday - Fire](#fireseed)"
		if(self.t.weekday() == 2):
			pprint("its Wednesday!")
			day = "[Wednesday - Water](#waterseed)"
		if(self.t.weekday() == 3):
			pprint("its Thursday!")
			day = "[Thursday - Light](#lightseed)"
		if(self.t.weekday() == 4):
			pprint("its Friday!")
			day = "[Friday - Wind](#windseed)"
		if(self.t.weekday() == 5):
			pprint("its Saturday!")
			day = "[Saturday - Earth](#earthseed)"
		self.sidebar = re.sub(r"SEEDBONUS", day , self.sidebar)

	def scrape_se_info(self, r):
		p = requests.get('http://information.mobiusfinalfantasy.com/ne/sp/')
		t = html.fromstring(p.content)
		links = t.xpath('//li[@class="entry"]/a/@href')
		names = t.xpath('//li[@class="entry"]/a/h4/text()')
		self.events = ''
		for l,n in zip(links, names):
			if self.t.strftime("%Y/%m") in n:
				self.events += ">>[**"+n.strip()+"**]("+l+")\n"

	def update_events(self):
		self.sidebar = re.sub(r"EVENTS", self.events, self.sidebar)
		
mobiusbot = Mobius_FF_Bot()
print 'MobiusBot Go!'+ datetime.now().strftime("%b %d, %A %I:%M %p")

while(True):
	print "Starting Check"
	#Get Reddit connection and set local sidebar
	r = mobiusbot.connect_to_reddit()
	mobiusbot.get_sidebar(r)
	
	#update server time in the local sidebar
	t = mobiusbot.update_sidebar_servertime(r)
	#if date change scrape event data, save new date	
	if(t.weekday() != mobiusbot.t.weekday()):
		print "Date change!"
		mobiusbot.t = t
		mobiusbot.scrape_se_info(r)
	#else if hour change, scrape data
	elif (t.strftime("%H") != mobiusbot.t.strftime("%H")):
		print "Hour change!"
		mobiusbot.t = t
		mobiusbot.scrape_se_info(r)

	#update seed bonus runs every minute since low cost
	mobiusbot.update_seed_bonus(r)
	#replace events with scraped data
	mobiusbot.update_events()
	
	#save the sidebar
	mobiusbot.save_sidebar(r)

	#monitor comments


	#sunday rage thread
	#monday archive rage thread
	print 'Sleeping for 1 minutes'
	time.sleep(60)
