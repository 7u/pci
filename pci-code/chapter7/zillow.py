import xml.dom.minidom
import urllib2

zwskey='X1-ZWz1fwmpozzx1n_aui2x'

def getaddressdata(address,city):
    escad=address.replace(' ','+')

    # Construct the URL
    url='http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
    url+='zws-id=%s&address=%scitystatezip=%s' % (zwskey,escad,city)
    
    # Parse resulting XML



