import random

import redis as s

redis_config = {'host': 'redis.pythonweekend.skypicker.com', 'port': 6379,
                'decode_responses': True, 'charset': 'utf-8'}
redis = s.Redis(**redis_config)

x = """Gentlemen!

Your business is at serious risk. There is a significant hole in the 
security system of your company. we've easily penetrated your network.
You should thank the Lord for being hacked by serious people 
not some stupid schoolboys or dangerous punks. 
They can damage all your important data just for fun. Now 
your files are crypted with the strongest millitary 
algorithms RSA4096 and AES-256.
No one can help you to restore files without our special decoder. 
Photorec, RannohDecryptor etc. repair tools are useless and can destroy your files irreversibly.
If you want to restore your files write to emails (contacts are at the 
bottom of the sheet) (Less than 5 Mb each, non-archived and your files should not contain 
valuable information and attach 2-3 encrypted files

You have to pay for decryption in Bitcoins.
The final price depends on how fast you write to us.
Every day of delay will cost you additional +0.5 BTC Nothing personal just business
As soon as we get bitcoins you'll get all your decrypted data back.
Moreover you will get instructions how to close the hole in security and how to avoid such problems in the future
we will recommend you special software that makes the most problems to hackers.


Do not rename encrypted files.
Do not try to decrypt your data using third party software.
P.S. Remember, we are not scanners. we don't need your files and your information. But after 2 weeks all your files and keys will be deleted automatically.

Just send a request immediately after infection.
All data will be restored absolutely. Your warranty - decrypted samples. contact emails elfasmarco@tutanota.com
or CamdenScott@protonmail.com

BTC wallet:
15RLWdvny5n1n7mTvU1zjg67wt86dhYqNj

NO system is safe"""

while True:
    for y in x.split("\n"):
        redis.set(y, random.randint(1, 100))
        redis.delete(y)
