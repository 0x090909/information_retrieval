import web
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

render = web.template.render('templates')

urls = (
	'/hello', 'hello',
	'/search', 'search'
)

class hello:
	def GET(self):
		return render.hello('marco','dussin')

class search:
	def GET(self):
		#inizializzo due documenti
		schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
		ix = create_in("indexdir", schema)
		writer = ix.writer()
		writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")
		writer.add_document(title=u"Second document", path=u"/b", content=u"The second one is even more interesting!")
		writer.add_document(title=u"Third document", path=u"/b", content=u"The third one is a copy of the first!")
		writer.commit()
		titles = '<ol>'
		with ix.searcher() as searcher:
			query = QueryParser("content", ix.schema).parse("first")
			results = searcher.search(query)
			for r in results:
				titles = titles + '<li>' +(r["title"]) + '</li>'
		titles = titles + '</ol>'
		return render.searchResults(titles)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()