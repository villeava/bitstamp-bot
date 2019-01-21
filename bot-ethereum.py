import hmac
import time
import datetime
import hashlib
import urllib2, urllib, json

def getPrice():

	url = "https://www.bitstamp.net/api/v2/ticker/ethusd"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	# print data
	return data['last'];

def queryUSDs():

	nonce = str(int(time.time() * 1000))
	message = nonce + 'BITSTAMP-KÄYTTÄJÄTUNNUS' + 'OMA-API-AVAIN'
	signature = hmac.new(
	   'API-AVAIMEN-SALAINEN-AVAIN',
		msg=message,
		digestmod=hashlib.sha256
	).hexdigest().upper()

	postdata = {
			'key': 'OMA-API-AVAIN',
			'signature': signature,
			'nonce': nonce}
	response = urllib2.urlopen(urllib2.Request('https://www.bitstamp.net/api/v2/balance/ethusd/', urllib.urlencode(postdata)))
	data = json.loads(response.read())
	# print 'Ethereum available: ', data['eth_available'], ' USD avaialble ', data['usd_available']
	return  data['usd_available'];

def queryEthereums():

	nonce = str(int(time.time() * 1000))
	message = nonce + 'BITSTAMP-KÄYTTÄJÄTUNNUS' + 'OMA-API-AVAIN'
	signature = hmac.new(
	   'API-AVAIMEN-SALAINEN-AVAIN',
		msg=message,
		digestmod=hashlib.sha256
	).hexdigest().upper()

	postdata = {
			'key': 'OMA-API-AVAIN',
			'signature': signature,
			'nonce': nonce}
	response = urllib2.urlopen(urllib2.Request('https://www.bitstamp.net/api/v2/balance/ethusd/', urllib.urlencode(postdata)))
	data = json.loads(response.read())
	# print 'Ethereum available: ', data['eth_available'], ' USD avaialble ', data['usd_available']
	return  data['eth_available'];


def sell(amount):
	nonce = str(int(time.time() * 1000))
	message = nonce + 'BITSTAMP-KÄYTTÄJÄTUNNUS' + 'OMA-API-AVAIN'
	signature = hmac.new(
	   'API-AVAIMEN-SALAINEN-AVAIN',
		msg=message,
		digestmod=hashlib.sha256
	).hexdigest().upper()

	postdata = {
			'key': 'OMA-API-AVAIN',
			'signature': signature,
			'nonce': nonce,
			'amount': amount}
	response = urllib2.urlopen(urllib2.Request('https://www.bitstamp.net/api/v2/sell/market/ethusd/', urllib.urlencode(postdata)))
	data = json.loads(response.read())

	print data
	print data['price']
	print data['amount']
	file = open("lastsellprice2.log", "w")
	file.write(data['price'])
	file.write('\n')
	file.close()
	fixedvalue = float(data['amount']) * float(data['price'])
	print fixedvalue
	return fixedvalue;


def buy(amount):
	nonce = str(int(time.time() * 1000))
	message = nonce + 'BITSTAMP-KÄYTTÄJÄTUNNUS' + 'OMA-API-AVAIN'
	signature = hmac.new(
	   'API-AVAIMEN-SALAINEN-AVAIN',
		msg=message,
		digestmod=hashlib.sha256
	).hexdigest().upper()

	postdata = {
			'key': 'OMA-API-AVAIN',
			'signature': signature,
			'nonce': nonce,
			'amount': amount}
	response = urllib2.urlopen(urllib2.Request('https://www.bitstamp.net/api/v2/buy/market/ethusd/', urllib.urlencode(postdata)))
	data = json.loads(response.read())
	file = open("lastbuyprice2.log", "w")
	file.write(data['price'])
	file.write('\n')
	file.close()
	print data
	return;

def calcandbuy():
	#print round(float(queryUSDs()) / float(getPrice()),8)
	targetsumfirst =  round(float(queryUSDs()) / float(getPrice()),8)
	targetsum = targetsumfirst * 0.95
	print round(targetsum,8)

	##print queryUSDs()
	buy(round(targetsum,8))
	return;
	def choiceactions():
	if float(queryUSDs()) >= round(float(getPrice()) * float(queryEthereums()),8):
		print 'There is more USDs available than ethereum in USD'
		choice = 1
	else:
		print 'There is more ethereums in USD available than USDs'
	choice = 2
	return choice;



def lastbuyprice():
	f1 = open("lastbuyprice2.log", "r")
	line1 = (f1.readline())
	return line1;

def lastsellprice():
	f2 = open("lastsellprice2.log", "r")
	line2 = (f2.readline())
	return line2;

	print 'Last buy price is: ', lastbuyprice()
	print 'Last sell price is: ', lastsellprice()


while True:
	if choiceactions() == 2:
		saleSuccess = 0
		i = 0
		score = 0
		attop = 0
		memory = {}
		historyprice = 0
		
	while saleSuccess == 0:
		curprice = getPrice()

		if curprice < 300:
			sell(queryEthereums())
		if historyprice == 0:
			historyprice = curprice
			print 'Previous: ',historyprice, 'Current', curprice, ' Previous: ', float(curprice)
		if curprice > historyprice:
			print 'Price is rising. Current price:  ', curprice, ' Previous price:', historyprice
			score = 1
		if curprice == historyprice:
			print 'Price is hanging!'
		if score == 1 and historyprice > curprice:
			score = 0
			print 'Do the sales!'
			
		value = sell(queryEthereums())
		changeofvalue = value - float(queryEthereums()) * float(lastbuyprice())
		file = open("changeofvalue2.log", "a")
		file.write(str(changeofvalue))
		file.write(' {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
		file.write('\n')
		file.close()
		saleSuccess = 1

		historyprice = curprice
		time.sleep(1800)
		
		if choiceactions() == 1:
			buySuccess = 0
			i = 0
			score = 0
			atbottom = 0
		historyprice = 0
		memory = {}
		print 'Starting to buy'
		
	while buySuccess == 0:
		if historyprice == 0:
			curprice = getPrice()
			historyprice = curprice
			curprice = getPrice()
			print curprice
			print historyprice
		if curprice < historyprice:
			print 'Price is lowering. Current price: ',curprice, '. Previous price: ', historyprice
			score = 1
		if curprice == historyprice:
			print 'Price is hanging'
		if score == 1 and historyprice < curprice:
				score = 0
			print 'Bying now!'
			calcandbuy()
			buySuccess = 1
			
	time.sleep(1800)
