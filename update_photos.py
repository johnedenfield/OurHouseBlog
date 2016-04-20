__author__ = 'johnedenfield'

from app.house.models import Photo

for i in xrange(1,1000):
    p=Photo.find_by_id(i)
    if p:
        p.websize()
        print('Resized Photo')