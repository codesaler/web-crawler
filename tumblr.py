#-*- coding:utf-8 -*-

import urllib
import sys
from xml.dom import minidom
import Image
from glob import glob

class Tumblr(object):
    def __init__(self, site="http://bonjourmadame.fr/api/read", pasta="/Users/rafael/Dropbox/Bonjour/"):
        self.site = site
        self.pasta = pasta
        self.links = {}
        self.pagina_atual = '?type=photo'
        import os
        os.chdir(pasta)
        self._total_posts()
    
    def _open(self):
        raw_xml = urllib.urlretrieve(self.site+self.pagina_atual)
        xml = minidom.parse(raw_xml[0])
        self.data = xml.getElementsByTagName('posts')[0]
    
    def _total_posts(self):
        self._open()
        self.total_posts = int(self.data.getAttribute("total"))
        self.original_posts = int(self.data.getAttribute("total"))
        self._nova_pagina()
    
    def _process_links(self):
        self._open()
        for post in self.data.childNodes:
            for tag in post.childNodes:
                if tag.tagName == u'photo-url' and \
                    int(tag.getAttribute('max-width')) >= 500 and \
                        post.getAttribute('id') not in self.links.keys():
                    self.links[post.getAttribute('id')] = tag.firstChild.wholeText
                    break
        self._nova_pagina()
    
    def _nova_pagina(self):
        self.pagina_atual = '?start=%d&type=photo' % (self.total_posts-20)
        if self.total_posts > 0:
            self.total_posts -= 20
        else:
            self.total_posts = 0
    
    def process_all_links(self):
        print 'This might take a while'
        while len(set(self.links.keys())) < self.original_posts:
            self._process_links()
            sys.stdout.flush()
            print 'Current status: %d of %d' % (len(set(self.links.keys())), self.original_posts)
    
    def save_all_images(self):
        counter = 1
        for name,link in self.links.items():
            if len(glob(str(name)+'.*')):
                print "Image with id:%s already saved." % (str(name))
            else:
                data = urllib.urlretrieve(link)
                img = Image.open(data[0])
                print "Saving: %d of %d images." % (counter, self.original_posts)
                img.save(self.pasta+name+"."+img.format.lower())
            counter += 1
        print counter
    
if __name__ == '__main__':
    t = Tumblr()
    t.process_all_links()
    t.save_all_images()
