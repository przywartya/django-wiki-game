from collections import OrderedDict
import requests
from bs4 import BeautifulSoup

def get_wiki_page(url):
	wiki_url = "https://en.wikipedia.org/wiki/%s"%url
	wiki_page = requests.get(wiki_url)
	wiki_page.encoding = 'utf-8'
	wiki_page = wiki_page.text
	wiki_soup = BeautifulSoup(wiki_page, 'html.parser')
	return wiki_soup

def get_article_name(url):
	soup = get_wiki_page(url)
	name = soup.find_all('h1', class_="firstHeading")[0]
	name = name.text.strip()
	return name

def get_relevant_links(url):

	def get_body_wiki(soup):
		body = soup.find_all('div', class_="mw-body-content")[0]
		relevant = body.find_all('div', class_="mw-content-ltr")[0]
		return relevant

	def remove_images(paragraph):
		for img in paragraph.find_all('a', class_="image"):
			img.replace_with('')
		return paragraph

	def get_title(link):
		try:
			return link['title']
		except:
			pass

	def get_href(link):
		try:
			return link['href']
		except:
			pass

	def find_links(paragraph):
		links_dict = OrderedDict()
		for link in paragraph.find_all('a',{'href': True}):
			title = get_title(link)
			if title is not None:
				link = get_href(link)
				if (link[0:6] == '/wiki/') and (not link[6:11] == 'Talk:') and ('cite_note' not in link) and (not link[6:15] == 'Category:') and (not link[6:15] == 'Template:') and (not link[6:11] == 'File:') and (not link[6:16] == 'Wikipedia:') and (not link[6:11] == 'Help:') and (not link[6].isdigit()) and (not link[6:11] == 'List_') and (not link[6:15] == 'Special:') and (not link[6:12] == 'Sound:'):
					href = link.rsplit('/',2)[2]
					links_dict[title] = href
		return links_dict

	complete_links_dict = OrderedDict()
	my_soup = get_wiki_page(url)
	content = get_body_wiki(my_soup)
	for par in content.find_all('p'):
		par = remove_images(par)
		links_dict = find_links(par)
		complete_links_dict.update(links_dict)
	return complete_links_dict
	
# poland = get_relevant_links("poland")
# poland = poland.values()
# # print (poland)
# my_list = list(poland)
# print (my_list)
