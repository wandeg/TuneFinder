import requests
import urllib2
import urllib
import json
import pymongo
import base64


class Tunefind:
	"""docstring for Tunefind"""
	def __init__(self):
		self.conn=pymongo.Connection('localhost',27017)
		self.db=self.conn.tunefind
		self.user=''
		self.passw=''
		self. base_url='https://www.tunefind.com/api/v1/show'
		payload={'Username':'','password':''}
		#from requests.auth import HTTPBasicAuth
		##r=requests.get(base_url, auth=HTTPBasicAuth(payload['Username'], payload['password']))
		r=requests.get(self.base_url, auth=(self.user,self.passw), verify=False)
		#data = urllib.urlencode(payload)
		##req = urllib2.Request(base_url, data)
		#req = base_url + '?' + data
		##print req
		#response = urllib2.urlopen(req)
		#the_page = response.read()

	def fetch(self,url,user=None,passw=None,key=None):
		res=None
		if user and passw:
			r=requests.get(url, auth=(user,passw), verify=False)
		else:
			r=requests.get(url)
		if r.status_code==200:
			response=r.json()
			if response.has_key(key):
				res=response[key]
		return res
		
	def fetch_shows(self):
		# request = urllib2.Request(base_url)
		# base64string = base64.encodestring('%s:%s' % (user, passw)).replace('\n', '')
		# request.add_header("Authorization", "Basic %s" % base64string)   
		# result = urllib2.urlopen(request)
		# response=json.loads(result.read())
		#r=requests.get(url, auth=(user,passw), verify=False)
		shows_list=[]
		# if r.status_code==200:
		# 	response=r.json()
		# 	if response.has_key('shows'):
		# 		shows_list=response['shows']
		shows_list=self.fetch(self.base_url,self.user,self.passw,key='shows')
		return shows_list

	def fetch_seasons(self,show):
		assert isinstance(show,dict)
		url=show['tunefind_api_url']
		# r=requests.get(url,auth=(self.user,self.passw), verify=False)
		seasons_list=[]
		# if r.status_code==200:
		# 	response=r.json()			
		# 	if response.has_key('seasons'):
		# 		seasons_list=response['seasons']
		seasons_list=self.fetch(url,self.user,self.passw,key='seasons')
		return seasons_list

	def fetch_season(self,seasons_list):
		assert isinstance(seasons_list,list)


	def fetch_episodes(self,seasons_list):
		assert isinstance(seasons_list,list)
		episodes_list=[]
		res=None
		for season in seasons_list:
			assert isinstance(season,dict)
			url=season['tunefind_api_url']
			# r=requests.get(url,auth=(self.user,self.passw), verify=False)			
			# if r.status_code==200:
			# 	response=r.json()			
			# 	if response.has_key('episodes'):
			res=self.fetch(url,self.user,self.passw,key='episodes')
			episodes_list.append(res)

		return episodes_list

	def fetch_songs(self,episodes_list):
		assert isinstance(episodes_list,list)
		res=None
		songs_list=[]
		for episode in episodes_list:
			assert isinstance(episode,dict)
			url=episode['tunefind_api_url']
			# r=requests.get(url,auth=(self.user,self.passw), verify=False)		
			# if r.status_code==200:
			# 	response=r.json()			
			# 	if response.has_key('songs'):
			res=self.fetch(url,self.user,self.passw,key='songs')
			songs_list.append(res)
		return songs_list

	def get_genre(song_id):
		itunes_lookup_base="https://itunes.apple.com/lookup"
		params='?id='+song_id
		url=itunes_lookup_base+params
		genre=""
		# r=requests.get(url)
		# if r.status_code == 200:
		# 	response=r.json()
		# 	if response.has_key('primaryGenreName'):
		genre=self.fetch(url,self.user,self.passw,key='primaryGenreName')
		return genre






# tf=Tunefind()
# shows=tf.fetch_shows(tf.base_url,tf.user,tf.passw)
# show_sns=map(tf.fetch_seasons,shows)
# show_names=[show['name'] for show in shows]
# show_episodes=map(tf.fetch_episodes, show_sns)