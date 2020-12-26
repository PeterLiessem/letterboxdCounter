import bs4 as bs
import urllib.request
import sys

class Boxd:

    def __init__(self, user):
        print(user)
        self.user = user
        self.link = f'https://letterboxd.com/{user}/films/page/'
        self.hoursWatched = -1
        
    def showHours(self):
        if self.hoursWatched == -1:
            self.calculateHours()
        if self.hoursWatched > -1: 
            print(f'{self.user} has watched: {self.hoursWatched} hours of movies.')

    def returnMinutes(self, link):
        source = urllib.request.urlopen('https://letterboxd.com'+link).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        title = soup.find('h1', 'headline-1').text
        text = soup.find('p', class_='text-link')
        ret = ''
        stop = False
        for i in text.text:
            if i.isnumeric():
                ret += i
        if ret == '':
            return 0
        print('{:<100s} {:<10s}'.format(f'{title}:', f'{ret}m'))
        return int(ret)

    def calculateHours(self):
        self.hoursWatched = 0
        totalhours = 0
        j = 1
        sum = 0
        while True:
            try:
                source = urllib.request.urlopen(self.link+f'{j}').read()
                soup = bs.BeautifulSoup(source, 'lxml')
                if soup.find('ul', class_='poster-list').text == '\n':
                    break
                thing = soup.find('ul', class_='film-list')
                
                for i in thing.findAll('li'):
                    link = i.find('div', class_='film-poster').get('data-target-link')
                    sum += self.returnMinutes(link)
                j+=1
            except:
                print('Must supply a valid usernme.')
                self.hoursWatched = -1
                return
        self.hoursWatched = sum/60

if len(sys.argv) > 1:
    box = Boxd(sys.argv[1])
    box.showHours()
else:
    print('Must supply a username.')