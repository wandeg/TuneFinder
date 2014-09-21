import itertools
import requests
import pymongo
from config import USERNAME, PASSWORD
class Tunefind:
	"""docstring for Tunefind"""
	def __init__(self):
		self.conn=pymongo.Connection('localhost',27017) #not yet implemented but will be once all the data is collected
		self.db=self.conn.tunefind
		self.user=None
		self.passw=None
		self.tv_base_url='https://www.tunefind.com/api/v1/show'
		self.movie_base_url='https://www.tunefind.com/api/v1/movie'
		self.artists_base_url='https://www.tunefind.com/api/v1/artist'

	def fetch(self,url,user=None,passw=None,key=None, offset=None):
		res=None
		if user and passw and not offset:
			r=requests.get(url, auth=(user,passw), verify=False) #verify is set to False because of tunefind's SSL issues
		elif user and passw and offset:
			payload={'offset':offset}
			r=requests.get(url,auth=(user,passw),verify=False,params=payload)
		else:
			r=requests.get(url)
		if r.status_code==200:
			res=r.json()
			if key:
			    if res.has_key(key):
				    res=res[key]
		return res

	def fetch_artists(self,offset=None):
		artists=[]
		if offset:
			artist_list=self.fetch(self.artists_base_url,self.user,self.passw,offset=offset)			
			while len(artist_list)>0:
				artists.extend(artist_list)
				offset+=1000
				artist_list=self.fetch(self.artists_base_url,self.user,self.passw,key='artists',offset=offset)
		else:
			artists=self.fetch(self.artists_base_url,self.user,self.passw,key='artists')
		return artists

	def fetch_artist_songs(self,artist_dict): #still needs work
		a_songs=None
		# url=self.artists_base_url+'/'+artist_id
		url=artist_dict.get('tunefind_api_url','')
		a_songs=self.fetch(url,self.user,self.passw,key="songs")
		if isinstance(a_songs,dict):
			# a_songs['artist']=artist_id
			if self.db:
				self.db.artist_songs.save(a_songs)
				return True
		return a_songs



		
		
	def fetch_shows(self):
		shows_list=[]
		shows_list=self.fetch(self.tv_base_url,self.user,self.passw,key='shows')
		return shows_list

	def fetch_movies(self):
		shows_list=[]
		shows_list=self.fetch(self.movie_base_url,self.user,self.passw,key='movies')
		return shows_list

	def fetch_seasons(self,show):
		seasons_list=[]
		if isinstance(show,dict):
			url=show['tunefind_api_url']
			seasons_list=self.fetch(url,self.user,self.passw,key='seasons')
		return seasons_list

	#def fetch_season(self,seasons_list):
		#assert isinstance(seasons_list,list)


	def fetch_episodes(self,seasons_list):
		episodes_list=[]
		if isinstance(seasons_list,list):
			res=None
			for season in seasons_list:
				if isinstance(season,dict):
					url=season['tunefind_api_url']
					res=self.fetch(url,self.user,self.passw,key='episodes')
					episodes_list.append(res)

		return episodes_list

	def flatten_list(nested_list,completely=False):
		if completely:
			return list(itertools.chain.from_iterable(nested_list))
		return list(itertools.chain(nested_list))


	def fetch_songs(self,episodes_list):
		songs_list=[]
		if isinstance(episodes_list,list):
			res=None
			for episode in episodes_list:
				if isinstance(episode,dict):
					if str(episode['song_count']) >0:
					    url=episode['tunefind_api_url']
					    try:
					        res=self.fetch(url,self.user,self.passw,key='songs')
					        songs_list.append(res)
					    except:
					        pass
		return songs_list

	def get_genre(self,song_id):
		itunes_lookup_base="https://itunes.apple.com/lookup"
		params='?id='+song_id
		url=itunes_lookup_base+params
		genre=""
		genre=self.fetch(url,self.user,self.passw,key='primaryGenreName')
		return genre


tf=Tunefind()
tf.user=USERNAME #insert api username here
tf.passw=PASSWORD #insert api password here
# tf.conn=''
# td.db=''
# shows=tf.fetch_shows()
# print len(shows)
# show_sns=map(tf.fetch_seasons,shows)
# print show_sns[0]
# print len(show_sns)
# show_ids=[show['id'] for show in shows]
# show_sns_dict=dict(zip(show_ids,show_sns))
# # show_names=[show['name'] for show in shows]
# # show_episodes=map(tf.fetch_episodes, show_sns)
# # arts=tf.fetch_artists(offset=1)
# # art_ids=[art['id'] for art in arts]
# # art_coll=tf.db.artists
# # map(art_coll.save,arts[1:])
# show_coll=tf.db.shows
# # print dir(show_coll)
# # show_coll.insert(shows)
# sns_coll=tf.db.seasons
# # for k,v in show_sns_dict.iteritems():
# #     sns_coll.save({'id':k,'seasons':v})
# movies=tf.fetch_movies()
# movie_coll=tf.db.movies
# movie_coll.insert(movies)
# show_eps_dict=dict(zip(show_ids,[[show for show in itertools.chain.from_iterable(show_list)] 
# 	for show_list in show_episodes])
# eps_coll=tf.db.episodes
# for k,v in show_eps_dict.iteritems():
#     eps_coll.save({'id':k,'episodes':v})
# show_songs=map(tf.fetch_songs,show_eps_dict.values())
# songs_coll_packed=tf.db.songs_packed
# for k,v in zip(show_eps_dict_new.keys(),show_songs):
#     songs_coll_packed.save({'id':k,'songs':v})
