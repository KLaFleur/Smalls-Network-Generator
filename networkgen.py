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
	artists = [0] * 20
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
	visitedPpl[artistLink ] = (1)
	link = getArtistLink(getArtistNum(artistLink))
	#creates an array of shows the artist was recently in 
	shows = getShows(link)

	for i in range(len(shows)):
		if shows[i] is 0:
			pass
		elif shows[i] in visitedShows:
		 	pass
		else:
			visitedShows[shows[i]] = (0)
			nodes[i] = findArtists(shows[i])
	print(nodes)
	

	print(ppl)
	

	for k in range(len(nodes)):
		for j in range (len(nodes[k]) - 1):
			
			if nodes[k][j] is not 0:
				artistAtHand = getArtistName("https://www.smallslive.com" + nodes[k][j]) 

				#this block checks if the edge at hand (artist at hand and the next in the list) is in the edgelist already.
				#If it is, it increases the edges weight. If not, it creates one with weight 1
				if nodes[k][j+1] is not 0:
					nextArtist = getArtistName("https://www.smallslive.com" + nodes[k][j + 1])
					if (artistAtHand + "," + nextArtist) in edges:
						edges[artistAtHand + "," + nextArtist] = edges[artistAtHand + "," + nextArtist] + 1
					elif (nodes[k][j+1] + "," + nodes[k][j]) in edges:
						edges[nextArtist + "," + artistAtHand] = edges[nextArtist + "," + artistAtHand] + 1
					else:
						edges[artistAtHand + "," + nextArtist] = 1

				#this block checks if the artist at hand is in the list of people.
				#if they are, 
				if ("https://www.smallslive.com" + nodes[k][j]) not in ppl:
					ppl[ ("https://www.smallslive.com" + nodes[k][j])] = 1
				else:
					weight = ppl[ ("https://www.smallslive.com" + nodes[k][j])]
					ppl[ ("https://www.smallslive.com" + nodes[k][j])] = weight + 1
	print(edges)
	print(ppl)
	global recurseCount	
	for q in list(ppl):
		if q not in visitedPpl and recurseCount < 10:
			recurseCount = recurseCount + 1
			print("key" + q)
			run(q)									
	print(ppl)
	print(edges)			
	

visitedPpl= {}
visitedShows = {}
edges = {}
recurseCount = 0
ppl = {"https://www.smallslive.com/artists/456-joe-sanders/" : 0}	
run("https://www.smallslive.com/artists/456-joe-sanders/")
#https://www.smallslive.com/artists/317-will-vinson/
for i in list(ppl):
	weight = ppl[i]
	del ppl[i]
	ppl[getArtistName(i)] = weight

print(ppl)


with open('data/nodeList.csv', 'a') as nF:
	fieldnames = ['id' , 'mention weight']
	writer = csv.DictWriter(nF , fieldnames = fieldnames)
	writer.writeheader()
	for i in list(ppl):
		writer.writerow( {'id' : i , 'mention weight' : ppl[i]  })

with open('data/edgeList.csv', 'a') as eF:
	fieldnames = ['source' , 'target', 'weight']
	writer = csv.DictWriter(eF , fieldnames = fieldnames)
	writer.writeheader()
	
	for i in list(edges):
		ends = i.split(",")
		writer.writerow( {'source' : ends[0] , 'target' : ends[1] , 'weight' : edges[i]   })















