import string
import random
import validators

BASE62_CHARS = string.ascii_letters + string.digits

def generate_short_code(length=6):
    """Generate a random short code using base62 characters"""
    return ''.join(random.choices(BASE62_CHARS, k=length))

def is_valid_url(url):
    """Validate if the provided string is a valid URL"""
    return validators.url(url)

def encode_id(num):
    """Convert a number to base62 string"""
    if num == 0:
        return BASE62_CHARS[0]
    
    result = []
    base = len(BASE62_CHARS)
    
    while num:
        result.append(BASE62_CHARS[num % base])
        num //= base
    
    return ''.join(reversed(result))

def decode_id(short_code):
    """Convert a base62 string back to number"""
    base = len(BASE62_CHARS)
    num = 0
    
    for char in short_code:
        num = num * base + BASE62_CHARS.index(char)
    
    return num
