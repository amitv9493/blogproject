import random 
import string

chars = string.ascii_letters + string.digits + string.punctuation

password = "".join(random.choices(chars, k=16))

print(password)