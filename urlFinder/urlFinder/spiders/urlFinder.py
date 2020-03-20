from __future__ import print_function
import scrapy
import sys
import os

class urlFinder(scrapy.Spider):
	name = "urlFinder"

	parent_url = ""
	urls = []

	def start_requests(self):
		if os.path.exists('urlsFound.txt'):
			os.remove('urlsFound.txt')

		print("Give full urls :", end=" ") # test with 'https://www.cse.iitb.ac.in/~chrahul/'

		self.parent_url =  sys.stdin.readline().strip() 
		self.urls.append(self.parent_url)
	
		for url in self.urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):

		localFile = open('urlsFound.txt', 'a+')
		i = 0
		for url in response.css('a::attr(href)').re('.*html'):
			i = i + 1
			if 'https' not in url:
				url = self.parent_url + url
			if url not in self.urls:
				self.urls.append(url)
				yield scrapy.Request(url=url, callback=self.parse)
				localFile.write(url)
				localFile.write("\n")

		print("found ", i)