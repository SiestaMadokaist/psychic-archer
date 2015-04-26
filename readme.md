### Manga Downloader
### Version: v-0.0.0

### Description:
Yet, another manga-downloader written in python.
Currently only support downloading from mangahere.

### Required-Library:
- pyquery
- requests

### How-to-use:
open
> mangahere.py.

on the:
```
if __name__ == '__main__':
  manga = Manga({manga-title})
  ...
```
replace __{manga-title}__, with the title of manga you want to download. for example if the mangahere url of the manga is:
http://www.mangahere.co/manga/nagato_yuki_chan_no_shoushitsu/

then, the __{manga-title}__ is __nagato_yuki_chan_no_shoushitsu__

### May come soon, may not:
- Updating chapters that wasn't downloaded.
- Concurrent-Downloads