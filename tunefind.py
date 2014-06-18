import requests
import pymongo

class Tunefind:
	"""docstring for Tunefind"""
	def __init__(self):
		#self.conn=pymongo.Connection('localhost',27017) #not yet implemented but will be once all the data is collected
		#self.db=self.conn.tunefind
		self.user=''
		self.passw=''
		self.tv_base_url='https://www.tunefind.com/api/v1/show'
		

	def fetch(self,url,user=None,passw=None,key=None):
		res=None
		if user and passw:
			r=requests.get(url, auth=(user,passw), verify=False)
		else:
			r=requests.get(url)
		if r.status_code==200:
			res=r.json()
			if key:
			    if res.has_key(key):
				    res=response[key]
		return res
		
	def fetch_shows(self):
		shows_list=[]
		shows_list=self.fetch(self.tv_base_url,self.user,self.passw,key='shows')
		return shows_list

	def fetch_seasons(self,show):
		assert isinstance(show,dict)
		url=show['tunefind_api_url']
		seasons_list=[]
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
			res=self.fetch(url,self.user,self.passw,key='songs')
			songs_list.append(res)
		return songs_list

	def get_genre(self,song_id):
		itunes_lookup_base="https://itunes.apple.com/lookup"
		params='?id='+song_id
		url=itunes_lookup_base+params
		genre=""
		genre=self.fetch(url,self.user,self.passw,key='primaryGenreName')
		return genre


# tf=Tunefind()
# shows=tf.fetch_shows(tf.tv_base_url,tf.user,tf.passw)
# show_sns=map(tf.fetch_seasons,shows)
# show_names=[show['name'] for show in shows]
# show_episodes=map(tf.fetch_episodes, show_sns)
