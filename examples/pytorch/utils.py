import os

def download(url, fname = None, cache = False):
    from urllib.parse import urlparse
    from urllib.request import urlretrieve

    if fname is None:
        p = urlparse(url)
        fname = os.path.basename(p.path)
    
    if os.path.exists(fname) and cache:
        return True

    try:
        urlretrieve(url, fname)
        return True
    except:
        return False