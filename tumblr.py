#-*- coding:utf-8 -*-
from xml.dom import minidom
import urllib
from PIL import Image

class Tumblr:
    def __init__(self, site="http://bonjourmadame.fr/api/read", pasta="/Users/rafael/tumblr/"):
        import glob
        self.site = site
        self.pasta = pasta
        self.counter = len(glob.glob(pasta+"*"))
        self.paginador = 20
        self.page = ""
        self.links = []
    
    def abrir(self):
        raw_xml = urllib.urlretrieve((self.site+self.page))
        print raw_xml
        print raw_xml[0]
        print raw_xml[1]
        xml = minidom.parse(raw_xml[0])
        posts = xml.getElementsByTagName("posts")[0]
        for post in posts.childNodes:
            link = [x for x in post.childNodes if x.tagName == u'photo-url' 
                                 and int(x.getAttribute("max-width"))>=500]
            if link:
                self.links.append(link[0].childNodes[0].wholeText)
    
    def salvar(self):
        for link in self.links:
            data = urllib.urlretrieve(link)
            img = Image.open(data[0])
            print "Salvando: "+self.pasta+str(self.counter)+"."+img.format.lower()
            self.counter += 1
            img.save(self.pasta+str(self.counter)+"."+img.format.lower())
        self.links = []
    
    def proximo_set_de_posts(self):
        self.page = "?start="+str(self.paginador)
        print self.site+self.page
        self.paginador += 20
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        t = Tumblr(site = sys.argv[1])
    elif len(sys.argv) == 3:
        t = Tumblr(site = sys.argv[1], pasta = sys.argv[2])
    else:
        t = Tumblr(pasta="/home/rafael/tumblr/")
    while True:
        try:
            t.abrir()
            t.salvar()
            t.proximo_set_de_posts()
        except Exception as e: 
            print e
            break
    print "Download concluido"
