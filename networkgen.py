import bs4 as bs 
import urllib.request
from urllib.request import urlopen
import csv

def getShows(artistPage):
	shows = [0] * 40
	#soup = bs.BeautifulSoup(artistPage, 'lxml')
	soup = bs.BeautifulSoup(urlopen(artistPage), 'lxml')
	i = 0
	for url in soup.find_all('a'):
		thisLink = url.get('href')
		
		if thisLink is not None and "/events/" in thisLink and thisLink not in shows and "/live-stream/" not in thisLink:
			print(thisLink)
			shows[i] = thisLink
			i = i + 1

	return shows

def findArtists(showPage):
	artists = [0] * 10
	showPage = "https://www.smallslive.com" + showPage 
	soup = bs.BeautifulSoup(urlopen(showPage), 'lxml')
	i = 0
	for url in soup.find_all('a'):
		thisLink = url.get('href')

		if thisLink is not None and "/artists/" in thisLink and thisLink not in artists:
			#print(thisLink)
			artists[i] = thisLink
			i = i + 1
	return artists 

#gets unique artist number from artist page
def getArtistNum(artistLink):
	splitLink = artistLink.split("/")
	artistId= splitLink[4].split("-")
	return artistId[0]
#parses the artist's name from their page url
def getArtistname(artistLink):
	splitLink = artistLink.split("/")
	artistId= splitLink[4].split("-")
	return artistId[1] + " " + artistId[2]

# Returns a link to a page with 10 or so of the artists recent shows
def getArtistLink(artistNum):
	return "https://www.smallslive.com/search/event/?artist=" + artistNum












arr = getShows("https://www.smallslive.com/artists/458-aaron-parks/")
print (arr)
for i in range(len(arr)):
	if arr[i] is 0:
		pass
	else:
		print (findArtists(arr[i]))







#arr2 = findArtists(arr[2])
#print (arr2)
