# Python Demo to make a Sanitized Wordlist

 - iterators
 - parallelism
 - `pathlib.Path`
 - context managers
 - `bytes` and `str` types
 - hanging indent style
 - downloading from https
 - `if __name__ == '__main__'`

---
```
    alpine:~$ time python get_sanitized_wordlist.py 
    Loading https://github.com/dwyl/english-words/raw/master/words_alpha.txt...
    Loading https://www.cs.cmu.edu/~biglou/resources/bad-words.txt...
    sanitizing sublist of 37010 words words[0]='a'...
    sanitizing sublist of 37010 words words[0]='boatlip'...
    sanitizing sublist of 37010 words words[0]='crownband'...
    sanitizing sublist of 37010 words words[0]='immoderateness'...
    sanitizing sublist of 37010 words words[0]='felled'...
    sanitizing sublist of 37010 words words[0]='metathesize'...
    sanitizing sublist of 37010 words words[0]='owlet'...
    sanitizing sublist of 37010 words words[0]='quixotry'...
    sanitizing sublist of 37010 words words[0]='sobs'...
    sanitizing sublist of 37010 words words[0]='tutorages'...
    sanitizing sublist of 4 words words[0]='zwinglianist'...
    len(wordlist)=370104 len(sanitized)=306944

    real  0m7.550s
    user  0m34.583s
    sys   0m0.142s
```
---
### Notes:
 - The _time_ command shows that Python used more CPU (_user_ + _sys_) than _real_ time, which means this used multiple cores.

 - Quixotry is a famous word due to this [record-setting game](https://www.cross-tables.com/annotated.php?a=6517#36#)! 🤯

 - Instead of `pathlib`, try `import sys` and `print`:
 ```Python
print(text, file=sys.stderr)  # for diagnostics
print('\n'.join(sanitized))  # for the final list
```
```bash
time python get_sanitized_wordlist.py > sanitized_words.out
```
