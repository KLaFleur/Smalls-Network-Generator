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
	nodeCount = 0
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
def getArtistName(artistLink):
	splitLink = artistLink.split("/")
	artistId= splitLink[4].split("-")
	return artistId[1] + " " + artistId[2]

# Returns a link to a page with 10 or so of the artists recent shows
def getArtistLink(artistNum):
	return "https://www.smallslive.com/search/event/?artist=" + artistNum

def run (artistLink):
	nodes = [[0 for x in range(70)] for y in range(70)]
	nodeCount = 0
	link = getArtistLink(getArtistNum(artistLink))
	#creates an array of shows the artist was recently in 
	shows = getShows(link)

	for i in range(len(shows)):
		if shows[i] is 0:
			pass
		else:
			nodes[i] = findArtists(shows[i])
	print(nodes)
	nodes2 = [0] * 200

	ppl = {getArtistName(artistLink) : 0}
	edges = {}

	for k in range(len(nodes)):
		for j in range (len(nodes[0])):
			
			if nodes[k][j] is not 0:
				artistAtHand = getArtistName("https://www.smallslive.com" + nodes[k][j]) 

				if artistAtHand not in ppl:
					ppl[artistAtHand] = 1
				else:
					weight = ppl[artistAtHand]
					ppl[artistAtHand] = weight + 1

				if artistAtHand not in nodes2:
					nodes2[nodeCount]  = artistAtHand
					nodeCount = nodeCount + 1
			#run("https://www.smallslive.com" + nodes[k][j])
	print(ppl)			
	print(nodes2)

nodes = [[0 for x in range(3)] for y in range(70)]
print(nodes)

	
run("https://www.smallslive.com/artists/458-aaron-parks/")


# nodes = [0] * 200
# nodeCount = 0


# arr = getShows("https://www.smallslive.com/artists/458-aaron-parks/")
# print (arr)
# for i in range(len(arr)):
# 	if arr[i] is 0:
# 		pass
# 	else:
# 		print (findArtists(arr[i]))

# print(nodes)

# if getArtistName("https://www.smallslive.com" + thisLink) not in nodes:
	# 				nodes[nodeCount] = getArtistName("https://www.smallslive.com" + thisLink)
	# 				nodeCount = nodeCount + 1




#arr2 = findArtists(arr[2])
#print (arr2)
