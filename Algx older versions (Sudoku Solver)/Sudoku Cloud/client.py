import requests
from time import time

st = time()

server = "84.22.96.202"
port = "5000"

unsolved = "xxx71x8xxx5xx6x1xx8x2xxxxxxxx914xxx3xxx9x64xxxxxx3721xx9x6xxx7x7xxxx3x5xxx5xxxxxx"
#unsolved = "x81x6xxx7xxx3x28xx6x7xx8xx97x4xxxx51x3xx59xxx95xxxxx4xxxxx2x194xxx7x43x54x5x3xxxx"

url = "http://" + server + ":" + port + "/?sudo=" + unsolved

request = requests.get(url)

solutions = request.text.split(";")[:-1]
for i in solutions:
	print i

print time() - st
