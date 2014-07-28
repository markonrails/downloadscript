import json
import urllib2
import sys
import logging
import requests
from optparse import OptionParser

useragent = 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'

responses = {
  100: ('Continue', 'Request received, please continue'),
  101: ('Switching Protocols',
      'Switching to new protocol; obey Upgrade header'),

  200: ('OK', 'Request fulfilled, document follows'),
  201: ('Created', 'Document created, URL follows'),
  202: ('Accepted',
      'Request accepted, processing continues off-line'),
  203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
  204: ('No Content', 'Request fulfilled, nothing follows'),
  205: ('Reset Content', 'Clear input form for further input.'), 206: ('Partial Content', 'Partial content follows.'), 
  300: ('Multiple Choices',
      'Object has several resources -- see URI list'),
  301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
  302: ('Found', 'Object moved temporarily -- see URI list'),
  303: ('See Other', 'Object moved -- see Method and URL list'),
  304: ('Not Modified',
      'Document has not changed since given time'),
  305: ('Use Proxy',
      'You must use proxy specified in Location to access this '
      'resource.'),
  307: ('Temporary Redirect',
      'Object moved temporarily -- see URI list'),

  400: ('Bad Request',
      'Bad request syntax or unsupported method'),
  401: ('Unauthorized',
      'No permission -- see authorization schemes'),
  402: ('Payment Required',
      'No payment -- see charging schemes'),
  403: ('Forbidden',
      'Request forbidden -- authorization will not help'),
  404: ('Not Found', 'Nothing matches the given URI'),
  405: ('Method Not Allowed',
      'Specified method is invalid for this server.'),
  406: ('Not Acceptable', 'URI not available in preferred format.'),
  407: ('Proxy Authentication Required', 'You must authenticate with '
      'this proxy before proceeding.'),
  408: ('Request Timeout', 'Request timed out; try again later.'),
  409: ('Conflict', 'Request conflict.'),
  410: ('Gone',
      'URI no longer exists and has been permanently removed.'),
  411: ('Length Required', 'Client must specify Content-Length.'),
  412: ('Precondition Failed', 'Precondition in headers is false.'),
  413: ('Request Entity Too Large', 'Entity is too large.'),
  414: ('Request-URI Too Long', 'URI is too long.'),
  415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
  416: ('Requested Range Not Satisfiable',
      'Cannot satisfy request range.'),
  417: ('Expectation Failed',
      'Expect condition could not be satisfied.'),

  500: ('Internal Server Error', 'Server got itself in trouble'),
  501: ('Not Implemented',
      'Server does not support this operation'),
  502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
  503: ('Service Unavailable',
      'The server cannot process the request due to a high load'),
  504: ('Gateway Timeout',
      'The gateway server did not receive a timely response'),
  505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
  }

def downloadpage(tid, url):
  logging.info('Prepare to download: %s' % url)

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', useragent)]
  response = opener.open(url)

  logging.info('Finished urlopen')

  downloader_result = {}

  downloader_result['requested_url'] = response.geturl()
  downloader_result['http_resp_code'] = response.getcode()
  downloader_result['http_resp_msg']  = responses.get(downloader_result['http_resp_code'])[0]
  
  contenttype = response.info().getheaders('Content-Type')[0].split(';')
  downloader_result['mime_type'] = contenttype[0]
  if (len(contenttype) > 1):
    downloader_result['charset'] = contenttype[1].split('=')[1]
  else:
    downloader_result['charset'] = ''
  downloader_result['task_id']   = tid
  downloader_result['state']     = 'OK'

  downloader_result['content']  = unicode(response.read(), 'utf-8', errors='ignore')

  ret = {'downloader_result': downloader_result}

  result = json.dumps(ret)

  logging.debug('Result: %s' % result)

  print result 
  
def getoptions():
  parser = OptionParser()

  parser.add_option('--log', dest = 'log', default = 'WARNING', 
      help = "Set logging level: WARNING(default), INFO, DEBUG)")

  return parser.parse_args()
  
def setuplogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
  logging.basicConfig(
      filename = '/home/mark/workplace/BSDownloader/log/downloader.log', 
      level = numeric_level, format = '%(asctime)s %(message)s')

def main():
  (options, args) = getoptions()
  setuplogging(options.log)

  tid = sys.argv[1]
  url = sys.argv[2]

  try:
    downloadpage(tid, url)
  except Exception as e:
    logging.error('Exception in downloading: %s' % e)
    print 'Exception in downloading: %s' % e

if __name__ == '__main__':
  main()
