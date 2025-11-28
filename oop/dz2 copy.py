import requests
from matplotlib import pyplot as plt


img = plt.imread('x.jpg')
plt.imshow(img)
plt.show()
url = 'https://cataas.com/cat/says/'
text = input()
response = plt.imread(requests.get(url=url + text))
plt.imshow(response)
plt.show()