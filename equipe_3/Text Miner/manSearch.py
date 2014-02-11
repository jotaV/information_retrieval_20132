# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================
#
# Author: Erik Hatcher
#
# to query the index generated with manindex.py
#  python mansearch.py <query>
# by default, the index is stored in 'pages', which can be overriden with
# the MANDEX environment variable
# ====================================================================


import sys, os, lucene

from string import Template
from datetime import datetime
from getopt import getopt, GetoptError

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

field = 'partido'
status = False

class CustomTemplate(Template):
	delimiter = '#'

def search(termo, **args):
	
	indexDir = os.environ.get('MANDEX') or '3iteracao'
	fsDir = SimpleFSDirectory(File(indexDir))
	searcher = IndexSearcher(DirectoryReader.open(fsDir))
	
	analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
	parser = QueryParser(Version.LUCENE_CURRENT, field, analyzer)
	parser.setDefaultOperator(QueryParser.Operator.OR)
	query = parser.parse(termo + ' '.join(args.values()))
	start = datetime.now()
	scoreDocs = searcher.search(query, 50).scoreDocs
	duration = datetime.now() - start

	politicos = []
	for scoreDoc in scoreDocs:	    
	    doc = searcher.doc(scoreDoc.doc)
	    table = dict((field.name(), field.stringValue()) for field in doc.getFields())	   
	    politicos.append(table)

	return politicos

