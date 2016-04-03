from django.shortcuts import render
from WikiLogic.wiki import * 
import itertools
# Create your views here.

def home(request):
	if request.method == 'POST':
		first = "Special:Random"
		first = get_article_name(first)
		last = "Special:Random"
		last = get_article_name(last)
		path = first+"$"+last
		context = {
			"first": first,
			"last": last,
			"path": path,
		}
		return render(request, 'frist.html', context)
	return render(request, 'home.html', {})

def article(request, path=None, article=None):
	if article is not None:
		if ";" in article:
			path = article.rsplit(';')[0]
			target = path.rsplit('$')[1]
			article = article.rsplit(';')[1]
			if article.lower().replace(' ','').replace('_','') == target.lower().replace(' ',''):
				return render(request, 'win.html', {})
			article_name = get_article_name(article)
			links_dict = get_relevant_links(article)
			n = len(links_dict)//2
			i = iter(links_dict.items())
			d1 = dict(itertools.islice(i,n))
			d2 = dict(i)
			links_list = list()
			links_list.append(d1)
			links_list.append(d2)
			context = {
				"article_name": article_name,
				"links_list": links_list,
				"path": path,
				"target": target,
			}
			return render(request, 'article.html', context)
		


