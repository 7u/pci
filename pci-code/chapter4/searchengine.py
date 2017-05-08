import re
import urllib2
import sqlite3
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse

ignoreWords=set(['the','of','to','and','a','in','is','it'])

class crawler:
    # Initialize the crawler with the name of database
    def __init__(self,dbName):
        self.con=sqlite3.connect(dbName)

    def __del__(self):
        self.con.close()
    
    def dbCommit(self):
        self.con.commit()

    # Auxilliary function for getting an entry id and adding
    # it if it's not present
    def getEntryId(self,table,field,value,createNew=True):
        cur=self.con.execute("select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute("insert into %s(%s) values('%s')" % (table,field,value))
            return cur.lastrowid
        return res[0]

    # Index an individual page
    def addToIndex(self,url,soup,depth):
        if self.isIndexed(url):
            return

        if url == 'https://en.wikipedia.org/wiki/Functional_programming' or \
                depth == 2:
            try:
                print 'Indexing %s' % url
            except:
                print 'Indexing unprintable page'

        urlid=self.getEntryId('urllist','url',url)
        
        text=self.getTextOnly(soup)
        words=self.separateWords(text)
        for i in range(len(words)):
            word=words[i]
            if word in ignoreWords:
                continue
            wordid=self.getEntryId('wordlist','word',word)
            self.con.execute('insert into wordlocation(urlid,wordid,location) values(%d,%d,%d)' % (urlid,wordid,i))
    
    # Extract the text from an HTML page (no tags)
    def getTextOnly(self,soup):
        v=soup.string
        if v == None:
            result=''
            for content in soup.contents:
                result+=self.getTextOnly(content)+'\n'
            return result
        return v.strip()

    # Separate the words by any non-whitespace character
    def separateWords(self,text):
        splitter=re.compile('[^a-zA-Z0-9_+-]')
        return [t for t in splitter.split(text) if t!='']

    # Return true if this url is already indexed
    def isIndexed(self,url):
        res=self.con.execute("select rowid from urllist where url='%s'" % url).fetchone()
        if res!=None:
            urlid=res[0]
            res=self.con.execute("select rowid from wordlocation where urlid=%d" % urlid).fetchone()
            return res!=None
        return False

    # Add a link between two pages
    def addLinkRef(self,urlFrom,urlTo,linkText):
        fromid = self.getEntryId('urllist', 'url', urlFrom)
        toid = self.getEntryId('urllist', 'url', urlTo)
        if fromid == toid:
            return
        
        cur = self.con.execute('insert into link(fromid,toid) values(%d,%d)' % (fromid,toid))
        linkid = cur.lastrowid
        
        for word in self.separateWords(linkText):
            if word in ignoreWords:
                continue
            wordid = self.getEntryId('wordlist', 'word', word)
            self.con.execute('insert into linkwords(wordid,linkid) values(%d,%d)' % (wordid,linkid))


    # Starting with a list of pages, do a breadth
    # first search to the given depth, indexing pages
    # as we go
    def crawl(self,pages,depth=2):
        print 'depth=%d' %depth
        for i in range(depth):
            newPages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    try:
                        print 'Could not open %s' % page
                    except:
                        print 'unknown error'
                    
                soup=BeautifulSoup(c, 'html.parser')
                self.addToIndex(page,soup,i)
                parsedUri=urlparse(page)
                scheme='{uri.scheme}'.format(uri=parsedUri)
                domain='{uri.scheme}://{uri.netloc}/'.format(uri=parsedUri)
                links=soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        uri=urljoin(domain,link['href'])
                        if uri.find("'")!=-1: continue
                        uri=uri.split('#')[0]
                        if uri == 'https://en.wikipedia.org/wiki/Functional_programming':
                            print 'Found %s' % uri 

                        if (scheme == 'http' or scheme == 'https') and not self.isIndexed(uri):
                            newPages.add(uri)
                            if uri == 'https://en.wikipedia.org/wiki/Functional_programming':
                                print 'Adding %s' % uri 
                        linkText=self.getTextOnly(link)
                        self.addLinkRef(page,uri,linkText)
                self.dbCommit()
            
            pages=newPages

    # Create the database tables
    def createIndexTables(self):
        self.con.execute('create table if not exists urllist(url)')
        self.con.execute('create table if not exists wordlist(word)')
        self.con.execute('create table if not exists wordlocation(urlid,wordid,location)')
        self.con.execute('create table if not exists link(fromid,toid)')
        self.con.execute('create table if not exists linkwords(wordid,linkid)')
        self.con.execute('create index if not exists urlidx on urllist(url)')
        self.con.execute('create index if not exists wordidx on wordlist(word)')
        self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')
        self.con.execute('create index if not exists urltoidx on link(toid)')
        self.con.execute('create index if not exists urlfromidx on link(fromid)')
        self.dbCommit()

class searcher:
    def __init__(self,dbName):
        self.con=sqlite3.connect(dbName)
    
    def __del__(self):
        self.con.close()

    def getMatchRows(self,q):
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        words = q.split(' ')
        tableNumber = 0

        for word in words:
            res=self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
            if res!=None:
                wordid = res[0]
                wordids.append(wordid)
                
                if tableNumber > 0:
                    clauselist += ' and w%d.urlid=w%d.urlid' % (tableNumber - 1, tableNumber)
                    clauselist += ' and '
                    tablelist += ','
                clauselist += 'w%d.wordid=%d' % (tableNumber, wordid)
                fieldlist += ',w%d.location' % tableNumber
                tablelist += 'wordlocation w%d' % tableNumber
                tableNumber += 1
    
        res = self.con.execute('select %s from %s where %s' % (fieldlist, tablelist, clauselist))
        rows = [row for row in res]
        return rows,wordids

    def getScoredList(self, rows, wordids):
        totalscores = dict([(row[0], 0) for row in rows])

        # To put the scoring functions
        #weights = [(1.0, self.frequencyScore(rows))]
        weights = [(1.0, self.locationScore(rows)),
                    (1.0, self.frequencyScore(rows))
                    ]

        for weight,scores in weights:
            for urlid in totalscores:
                totalscores[urlid] += scores[urlid] * weight

        return totalscores

    def getUrlName(self, urlid):
        res=self.con.execute('select url from urllist where rowid=%d' % urlid).fetchone()
        if res!=None:
            return res[0]
        return None

    def query(self, q):
        rows, wordids = self.getMatchRows(q)
        scores = self.getScoredList(rows, wordids)
        rankedScores = sorted([(score, urlid) for urlid,score in scores.items()], reverse=1)
        for score,urlid in rankedScores[0:10]:
            print '%f\t%s' % (score, self.getUrlName(urlid))

    def normalizeScores(self, scores, smallIsBetter=0):
        vsmall = 0.00001
        maxScore = max(scores.values())
        minScore = min(scores.values())
        if maxScore == 0:
            maxScore = vsmall
        if smallIsBetter:
            return dict([(u, float(minScore) / max(vsmall, c)) for u,c in scores.items()])
        else:
            return dict([(u, float(c) / maxScore) for u,c in scores.items()])
    
    def frequencyScore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalizeScores(counts)

    def locationScore(self, rows):
        locations = dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]: locations[row[0]] = loc
        return self.normalizeScores(locations, smallIsBetter=1)
