# Helper script to zip the project (not used by main)
import zipfile
import os

base = os.path.dirname(__file__)
with zipfile.ZipFile('funpay_cardinal_stars.zip', 'w') as z:
    for f in os.listdir(base):
        if f.endswith('.py') or f in ['README.md', 'requirements.txt', 'config.py']:
            z.write(os.path.join(base, f), arcname=f)
print('zipped')
