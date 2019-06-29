import web
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from paginate_whoosh import WhooshPage
from search_ohsumed import src
import re

render = web.template.render('templates',base="main_layout",globals={'re':re})


fst = FileStorage("../ohsumed_index_dir_stopwords_clinico")

urls = (
	'/','index',
	'/index', 'index',
	'/search', 'search',
	'/article', 'article'
	#'/advancedsearch', 'adv_search' ## PREMIUM FEATURE
)

class index:
	def GET(self):
		return render.index()

class article:
	def GET(self):
		user_data = web.input()
		docid = user_data.docid
		return render.post(getDoc(docid))

class search:
	def GET(self):
		user_data = web.input()
		out, searcherlen, pages = src(fst,user_data,lim=1000)
		if searcherlen:
			return render.searchResults(out, user_data, searcherlen, pages)
		else:
			return render.searchResults(out, user_data,0,None)
class adv_search:
	def GET(self):
		return render.advanced()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
