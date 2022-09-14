import random
import string
import requests

# Generate Random 10 char (uppercase and digits) string 
def generate_string():
    chars = string.ascii_uppercase + string.digits
    return (''.join(random.choice(chars) for _ in range(10)))

def generate_leters():
    chars =  string.digits 
    return (''.join(random.choice(chars) for _ in range(10)))

def generate_ip():
      first = ['1','2']
      second=['','0','1','2','3','4','5']
      port=['16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
      ip=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      ip+=''.join(random.choice(first))+''.join(random.choice(second)) +''.join(random.choice(second))+'.'
      ip+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      ip+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'/'
      ip+=''.join(random.choice(port))
      return ip     

def generate_gateway():
      first = ['1','2']
      second=['','0','1','2','3','4','5']
      gateway=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      gateway+=''.join(random.choice(first))+''.join(random.choice(second)) +''.join(random.choice(second))+'.'
      gateway+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      gateway+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))
      return gateway  

def generate_inavalid_ip():
      first = ['6','7','8','9']
      second=['6','7','8','9']
      port=random.randrange(0,15)
      ip=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      ip+=''.join(random.choice(first))+''.join(random.choice(second)) +''.join(random.choice(second))+'.'
      ip+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      ip+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'/'
      ip+=str(port)
      return ip

def generate_inavalid_gateway():
      first = ['6','7','8','9']
      second=['6','7','8','9']
      gateway=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      gateway+=''.join(random.choice(first))+''.join(random.choice(second)) +''.join(random.choice(second))+'.'
      gateway+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))+'.'
      gateway+=''.join(random.choice(first))+''.join(random.choice(second))+''.join(random.choice(second))
      return gateway

def valid_amount():
      decimal= ((random.randrange(1,99)))
      rational= (str(random.uniform(0.009,0.1)))
      sum = rational[0:5]
      list=[decimal,float(sum)]
      return(random.choice(list))
      
def invalid_amount():
      rational= (str(random.uniform(100,10000)))
      return rational

def invalid_amount_negtive():
      negative= (str(random.randrange(1,99)))
      negative='-'+negative
      return negative

def invalid_address():
      chars  =string.ascii_uppercase +string.digits
      begin='5'
      return (begin+''.join(random.choice(chars) for _ in range(47)))

def valid_address ():
      r = requests.get("https://gridproxy.test.grid.tf/twins?twin_id=224")
      output=r.json()
      return (output[0]['accountId'])

def invalid_exceed_balance():
      rational= (str(random.randrange(100,10000)))
      return rational
