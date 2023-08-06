from hashlib import sha256,sha512
from pyappi.encoding.url import encode_url
import json


def SecureUser(user):
    h256 = sha256()
    h256.update(user + 'APPI-DOMAIN-06036F34-78A8-45A7-B96D-646BE001039C')

    return encode_url(h256.digest())

def SecureChallenge(challenge, user):
    h512 = sha512()
    h512.update(challenge + user + 'APPI-DOMAIN-C3A09828-1AEB-4486-9BDE-010A035FE92C')

    return encode_url(h512.digest())

def SessionChallenge(_user, _challenge):
    user = SecureUser(_user)
    challenge = SecureChallenge(_challenge)
    bin = json.dump({"user": user, "challenge": challenge})

    return encode_url(bin)