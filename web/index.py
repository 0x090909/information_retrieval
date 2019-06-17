import web
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from paginate_whoosh import WhooshPage

render = web.template.render('templates')

urls = (
	'/','index',
	'/index', 'index',
	'/search', 'search'
)

class index:
	def GET(self):
		return render.index()

class search:
	def GET(self):
		user_data = web.input()
		#inizializzo due documenti
		schema = Schema(docid      	= ID(stored=True),
		        		title      	= TEXT(stored=True),
		        		identifier	= ID(stored=True),
		        		terms 		= NGRAM(stored=True),
		        		authors     = NGRAM(stored=True),
		        		abstract 	= TEXT(stored=True),
		        		publication	= TEXT(stored=True),
		        		source 		= TEXT(stored=True))
		st = FileStorage("../ohsumed_index_dir_stopwords_clinico")
		ix = st.open_index()
		titles = '<ol>'
		with ix.searcher() as searcher:
			q = QueryParser("title",schema, group=qparser.OrGroup).parse(user_data.query)
			searcher = ix.searcher(weighting=scoring.TF_IDF()).search(q, limit=1000)
			page = WhooshPage(
				searcher, # limit=None is required!
				page=user_data.page, items_per_page=10)

		searcherlen = len(searcher)
		out = [{"abstract":article.get('abstract')[:300] + '...' if "abstract" in article.keys() and len(article.get('abstract')) > 300   else article.get('abstract'), "docid":article.get("docid"),"title":article.get("title")} for article in page]
		pages = range(1,max(2,searcherlen/10))
		return render.searchResults(out, user_data, searcherlen, pages)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
