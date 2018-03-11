#encoding="utf-8"
import bitcoin
import hashlib
import time
import urllib
import urllib2
import json
import smtp
from copy import deepcopy

Num = 1000000
guessNum = 1

# Generate a random private key
def Generate_random_private_key():
    valid_private_key = False 
    while not valid_private_key:
        private_key = bitcoin.random_key()
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key =  0 < decoded_private_key < bitcoin.N
    return private_key

def from_private_key_to_address(private_key):
    compressed_private_key = private_key + '01'
    bitcoin_address = bitcoin.privkey_to_address(private_key)
    compressed_bitcoin_address = bitcoin.privkey_to_address(compressed_private_key)
    return bitcoin_address,compressed_bitcoin_address


def querybalance(Address):
    queryurl = 'https://blockchain.info/q/addressbalance/' + Address
    response = urllib2.urlopen(queryurl)
    balance = response.read()
    print "query BTC address %s query balance is %s " % (Address,balance)
    response.close()
    return balance

def querybalainceV3(Address):
    queryurl = 'https://chain.api.btc.com/v3/address/' + Address
    response = urllib2.urlopen(queryurl)
    queryString = response.read()
    querydata = json.loads(queryString)
    if querydata[u'data'] == None:
        print "address %s has no BTC" % Address
        response.close()
        return '0'
    balance = querydata[u'data'][u'balance']
    print "query BTC address %s query balance is %s " % (Address,balance)
    response.close()
    return balance

def add_unquery_address_to_log(private_key,address):
    linestring = time.strftime("%Y-%m-%d %H:%M") + " " + str(private_key) + " " + str(address) + '\n'
    f = open("unqueryaddress.log","a")
    f.write(linestring)
    f.close()

def add_query_address_has_btc(private_key,address):
    linestring = time.strftime("%Y-%m-%d %H:%M") + " " + str(private_key) + " " + str(address) + '\n'
    f = open("address_has_btc.log","a")
    f.write(linestring)
    f.close()


def Check1000k_address(start_private_key,Num):
    global guessNum
    private_key = deepcopy(start_private_key)
    # private_key=26563230048437957592232553826663696440606756685920117476832299673293013768870
    startkey = deepcopy(start_private_key)
    while private_key < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
        random_private_key=Generate_random_private_key()
        random_addresss = from_private_key_to_address(random_private_key)
        private_key += 1
        guessNum += 1
        PrivateKey_WIF = bitcoin.encode_privkey(private_key,'wif')
        compressed_private_key = bitcoin.encode_privkey(private_key,'hex') + '01'
        PrivateKey_WIF_Compressed = bitcoin.encode_privkey(bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif')
        bitcoin_address = bitcoin.privkey_to_address(PrivateKey_WIF)
        compressed_bitcoin_address = bitcoin.privkey_to_address(PrivateKey_WIF_Compressed)
        addresss = [bitcoin_address,compressed_bitcoin_address,random_addresss[0],random_addresss[1]]
        for address in addresss:
            try:
                balance = querybalainceV3(address)
            except:
                print 'failed to query private_key %s ,address %s' % (private_key,address)
                add_unquery_address_to_log(private_key,address)
                continue
            time.sleep(0.5)
            #balance = querybalance('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
            if int(balance) >0 :
                print 'private_key %s has %s BTC' % (private_key,balance)
                add_query_address_has_btc(private_key,address)
                linestring = 'private_key %s has %s BTC !' % (private_key,balance)
                smtp.send_BTCmail(linestring)
        print "Check %s private_key %s " % (str(guessNum),private_key)
        if private_key==startkey + Num:
            add_query_address_has_btc(private_key,Num)
            break

def Check_address():
    print "##################"
    start_private_key = 26563230048437957592232553826663696440606756685920117476832299673293021166552
    while start_private_key < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
        print "Start check One million address"
        Check1000k_address(start_private_key,Num)
        start_private_key += 1000000
        print "has check One million address"

if __name__ == '__main__':
    #querybalainceV3('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
    Check_address()
    #querybalance('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')
    #querybalainceV3('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')

