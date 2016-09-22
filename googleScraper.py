#! /usr/bin/python3
#############################################################################################
## dru1d                                                                                    #
## Original PoC Mukarram Khalid                                                             #
##(SOURCE: https://mukarramkhalid.com/python-making-your-own-google-scraper-mass-exploiter/)#
## Version 1.0 - 09/21/16                                                                   #
#############################################################################################

'''
Usage:
  googleScraper.py <dorks> <search> <pages> <processes>
  googleScraper.py (-h | --help)

Arguments:
  <dorks>         Google dorks (I.E. site:linkedin.com)
  <search>        Company to be Searched
  <pages>         Number of pages
  <processes>     Number of parallel processes

Options:
  -h, --help     Show this screen.

'''

import requests, re, sys
from docopt import docopt
from bs4    import BeautifulSoup
from time   import time as timer
from functools import partial
from multiprocessing import Pool

#Gather URLs for scraping
def get_urls(dork_string, search_string, start):
    temp_url        = []
    temp_name       = []
    url         = 'http://www.google.com/search'
    dork        = dork_string
    query       = search_string
    payload     = { 'q' : [dork,query], 'start' : start }
    my_headers  = { 'User-agent' : 'Mozilla/11.0' }
    r           = requests.get( url, params = payload, headers = my_headers )
    soup        = BeautifulSoup( r.text, 'html.parser' )
    h3tags      = soup.find_all( 'h3', class_='r' )
    for h3 in h3tags:
        try:
#             temp_url.append( re.search('url\?q=(.+?)\&sa', h3.a['href']).group(1) )
             temp_name.append(h3.get_text())
        except:
            continue
    return temp_name

def main():
    start       = timer()
    result      = []
    arguments   = docopt( __doc__, version='Google Scraper' )
    dorks       = arguments['<dorks>']
    search      = arguments['<search>']
    pages       = arguments['<pages>']
    processes   = int( arguments['<processes>'] )
    ####Changes for Multi-Processing####
    make_request = partial( get_urls, dorks, search )
    pagelist     = [ str(x*10) for x in range( 0, int(pages) ) ]
    with Pool(processes) as p:
        tmp = p.map(make_request, pagelist)
    for x in tmp:
        result.extend(x)
    ####Changes for Multi-Processing####
    result = list( set( result ) )
    print( *result, sep = '\n' )
    print( '\nTotal names Scraped : %s ' % str( len( result ) ) )
    print( 'Script Execution Time : %s ' % ( timer() - start, ) )

if __name__ == '__main__':
    main()

#End
