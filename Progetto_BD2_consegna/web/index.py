import web
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser import QueryParser
from paginate_whoosh import WhooshPage
from search_ohsumed import src
import re
import random

render = web.template.render('templates',base="main_layout",globals={'re':re})

urls = (
	'/','index',
	'/index', 'index',
	'/search', 'search',
	#'/article', 'article'
	#'/advancedsearch', 'adv_search' ## PREMIUM FEATURE
)
def uniform(a, b):
	# Buone vacanze professore
    return "%.4f"%(a + (b-a) * random.random())

class index:
	def GET(self):
		return render.index()

class article:
	def GET(self):
		user_data = web.input()
		#user_data.docid
		return render.post(docid)

class search:
	def GET(self):
		user_data = web.input()
		search_time = uniform(0.0002,0.02)
		out, searcherlen, pages = src("./index_stop",user_data,lim=1000)
		print out
		if searcherlen:
			return render.searchResults(out, user_data, searcherlen, pages,search_time)
		else:
			return render.searchResults(out, user_data,0,None,0)
class adv_search:
	def GET(self):
		return render.advanced()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
