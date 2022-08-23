import random
import string

# Generate Random 10 char (uppercase and digits) string 
def GenerateString():
    chars = string.ascii_uppercase + string.digits
    return (''.join(random.choice(chars) for _ in range(10)))