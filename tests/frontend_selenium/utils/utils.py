import random
import string

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