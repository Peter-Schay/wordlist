"""Simple word sanitizer for Python 3.12

Download lists of words and bad words, and produce a sanitized list.
"""
import ssl
import certifi
import urllib.request
from pathlib import Path
from multiprocessing import Pool
from itertools import batched, chain

WORDS_URL = 'https://github.com/dwyl/english-words/raw/master/words_alpha.txt'
BAD_WORDS_URL = 'https://www.cs.cmu.edu/~biglou/resources/bad-words.txt'
TARGET = Path(Path.cwd(), 'words_alpha.sanitized.txt')
NPROCS=11

def load_text_from_url(url: str) -> str:
    """Read data from an https URL using a default SSL context."""
    # Use print to be friendly to the user while they are waiting,
    # and also to validate that the downloads are indeed parallel:
    print(f'Loading {url}...')

    # When there is something after the closing ')' or ']' or '}',
    # I put it on a new line, which is what most people do --
    # see the ") as f:", below:
    with (urllib.request.urlopen(
        url,
        context=ssl.create_default_context(cafile=certifi.where()))
    ) as f:
        return f.read().decode()

def sanitize(*words, badwords):
    """Return all the words except those that contain a bad word."""
    print(f'sanitizing sublist of {len(words)} words {words[0]=}...')
    # This part could certainly be optimized.
    # That's left as a fun puzzle for sadistic interviewers. 😉
    return [w for w in words if not any (
        (bad.strip() in w.strip().lower() for bad in badwords))]

if __name__ == '__main__':
    # Load the wordlists from their urls, in parallel.
    # Because the bad-words list is small, this is not going to speed
    # things up much; however it's a great example of multiprocessing for IO.
    # NOTE: This should work just as well with threads, since the thing to
    # break up here is the wait time, as opposed to CPU cycles, which require
    # multiprocessing to parallelize (for now, until Python 3.13 or 14).
    # Exercise: Try a thread pool here!
    with Pool(2) as p:
        # Unlike most people, I use Python's "hanging indent" style
        # when the closing ')' or ']' or '}' has nothing after it:
        jobs = [
            p.apply_async(load_text_from_url, [url])
            for url in (WORDS_URL, BAD_WORDS_URL)]
        wordlist, badwords = (job.get().split() for job in jobs)

    jobs = []
    with Pool(NPROCS) as p:
        for batch in batched(wordlist, n=len(wordlist)//(NPROCS-1)):
            jobs.append(p.apply_async(
                sanitize, batch, dict(badwords=badwords)))
        sanitized=list(chain(*[job.get() for job in jobs]))

    print(f'{len(wordlist)=} {len(sanitized)=}')
    TARGET.write_text('\n'.join(sanitized))
