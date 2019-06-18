import web
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from paginate_whoosh import WhooshPage
from search_ohsumed import src

render = web.template.render('templates',base="main_layout")


fst = FileStorage("../ohsumed_index_dir_stopwords_clinico")

urls = (
	'/','index',
	'/index', 'index',
	'/search', 'search',
	'/article', 'article'

)

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
		out, searcherlen, pages = src(fst,user_data,lim=1000)
		return render.searchResults(out, user_data, searcherlen, pages)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
