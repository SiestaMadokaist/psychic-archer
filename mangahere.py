from pyquery import PyQuery as pq
import requests
import operator as op
import re
import os

def lazy(function):
  memo = {function : None}
  def aply(args):
    if not memo.get((function, args)):
      memo[(function, args)] = function(args)
      return memo[(function, args)]
    else:
      return memo[(function, args)]
  return aply

class URL(str):
  def __init__(self, url):
    self.url = url

class Page(object):
  def __init__(self, url, parent):
    self.url = url
    self.parent = parent

  @lazy
  def imageURL(self):
    html = pq(requests.get(self.url).text)
    return html("img#image")[0].get("src")

class Chapter(object):
  @classmethod
  def sorter(cls, url_string):
    value = re.findall(r".+/(.+).html", url_string)
    if not value: return 0
    else: return int(value[0])

  def __init__(self, url, parent):
    self.url = url
    self.parent = parent
    self.mkdir()

  def mkdir(self):
    try:
      os.mkdir(self.defaultDirectory)
    except Exception as e:
      if e.__class__ in [IOError, OSError]:
        pass
      else:
        raise e

  @property
  def chapterID(self):
    return re.findall(r"/c([0-9]{3})/", self.url)[0]

  @property
  def defaultDirectory(self):
    fdir = self.manga.directory
    return "{0}/{1}".format(fdir, self.chapterID)

  @property
  def manga(self):
    return self.parent

  @lazy
  def pages(self):
    html = pq(requests.get(self.url).text)
    dom = html("option")
    mPages = sorted(list(set(map(op.methodcaller("get", "value"), dom))), key=Chapter.sorter)
    return [Page(URL(p), self) for p in mPages]

  def download(self, directory=None):
    if directory is None: directory = self.defaultDirectory
    for i, page in enumerate(self.pages()):
      target = page.imageURL()
      fmt = re.findall(r".+\.([A-z]{2,3})\?{0,1}", target)[0]
      page_number = "%03i" % i
      fout = "{0}/{1}.{2}".format(directory, page_number, fmt)
      print("{0} => {1}".format(target, fout))
      with open(fout, 'wb') as out:
        out.write(requests.get(target).content)

class Manga(object):
  def __init__(self, title):
    self.title = title
    self.url = URL("http://www.mangahere.co/manga/{0}".format(title))
    self.mkdir()

  def mkdir(self):
    try:
      os.mkdir(self.directory)
    except Exception as e:
      if e.__class__ in [IOError, OSError]:
        pass
      else:
        raise e

  @property
  def directory(self):
    return "manga/{0}".format(self.title)

  @lazy
  def chapters(self):
    html = pq(requests.get(self.url).text)
    dom = html("div.detail_list li a")
    links = map(op.methodcaller("get", "href"), dom)
    links.reverse() # because it start from the latest chapters, to the oldest
    return [Chapter(URL(url), self) for url in links]

if __name__ == '__main__':
  manga = Manga("nagato_yuki_chan_no_shoushitsu")
  for chapter in manga.chapters():
    chapter.download()