pipreqs . --encoding=utf-8 --force --debug 
sort requirements.txt /O reqs.tmp
del requirements.txt
ren reqs.tmp requirements.txt

