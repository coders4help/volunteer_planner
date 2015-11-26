import urllib, urllib2, json
from decimal import Decimal
from django.utils.encoding import smart_str

def geocode(address):
    address = urllib.quote_plus(smart_str(address))
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % address
    response = urllib2.urlopen(url).read()
    result = json.loads(response)

    if result['status'] == 'OK':
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
        return Decimal(lat), Decimal(lng)

