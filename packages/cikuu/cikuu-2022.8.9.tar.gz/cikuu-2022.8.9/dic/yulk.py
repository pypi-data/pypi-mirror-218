# 2023.7.2  usage:  from dic import yulk ,     for doc in yulk.docs('gzjc') : print(doc) 
import json, traceback,sys, time,  fileinput, os, fire,pathlib, platform, redis, spacy

snthost = os.getenv('snthost', 'snt.jukuu.com:6206') #  snt => tx98
if not hasattr(spacy, 'nlp'):
	spacy.nlp		= spacy.load(os.getenv('spacy_model','en_core_web_sm')) # 3.4.1
	spacy.from_json = lambda arr: spacy.tokens.Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19

def rcon():
	if not hasattr(redis, 'r'): redis.r = redis.Redis(host=snthost.split(':')[0], port=int(snthost.split(':')[-1]), decode_responses=True, health_check_interval=30)
	return redis.r 

def keys(pattern:str): #f"snt-spacy:{name}:*"
	r = rcon()
	for k in r.keys(pattern):
		yield k 

def docs(name:str='gzjc'):
	if not hasattr(redis, 'r'): redis.r = redis.Redis(host=snthost.split(':')[0], port=int(snthost.split(':')[-1]), decode_responses=True, health_check_interval=30)
	for k in redis.r.keys(f"snt-spacy:{name}:*"):
		v = redis.r.get(k)  #redis.r.hget(k, 'spacy')
		if not v: continue 
		arr = json.loads(v.strip()) 
		doc = spacy.from_json(arr) 
		yield doc 

def txtdocs(name:str='spider'):
	if not hasattr(redis, 'r'): redis.r = redis.Redis(host=snthost.split(':')[0], port=int(snthost.split(':')[-1]), decode_responses=True, health_check_interval=30)
	for k in redis.r.keys(f"txt-spacy:{name}:*"):
		v = redis.r.hget(k, 'spacy')
		if not v: continue 
		arr = json.loads(v.strip()) 
		doc = spacy.from_json(arr) 
		yield doc 

class util(object): 
	def __init__(self, host='snt.jukuu.com', port=6206,):
		redis.r = redis.Redis(host=host, port=port, decode_responses=True)
		print ( redis.r, flush=True)
	
	def hello(self, name:str='gzjc'):
		for doc in docs(name): print(doc) 

	def sntspacy(self, infile):
		''' find . -name "*.4.1.gz" -exec python yulk.py sntspacy {} \;  '''
		name = infile.split('/')[-1].split('.')[0] # ./sci.jsonlg.3.4.1.gz
		print ("snt-spacy started:", name ,  ' -> ',  redis.r, flush=True)
		[ redis.r.delete(k) for k in redis.r.keys(f"snt-spacy:{name}:*")]
		start = time.time()

		redis.r.hset("snt-spacy", name, 0) 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #356317 docs of each doc file
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 
				snt = doc.text.strip()
				redis.r.hincrby("snt-spacy", name) 
				#redis.r.hset(f"snt-spacy:{name}:{snt}", 'spacy',line, {"sid":sid, "tc": len(doc)})    too slow 
				redis.r.setnx(f"snt-spacy:{name}:{snt}", line) #avoid a super large key 
			except Exception as e:
				print ("ex:", e, sid, line[0:30]) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)

		print(f"{infile} is finished, \t| using: ", time.time() - start) 

	def txtspacy(self, infile, refresh:bool=True):
		''' spider.ag.docjsonlg.3.4.1.gz,  info '''
		name = infile.split('/')[-1].split('.')[0] 
		print ("txt-spacy started:", name ,  ' -> ',  redis.r, flush=True)
		if refresh: [ redis.r.delete(k) for k in redis.r.keys(f"txt-spacy:{name}:*")]
		start = time.time()

		redis.r.hset("txt-spacy", name, 0) 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):
			try:
				arr = json.loads(line.strip()) 
				redis.r.hincrby("txt-spacy", name) 

				info = arr.get('info',{}) 
				did = info.get('did', 0) 
				redis.r.hset(f'txt-spacy:{name}:{did}', 'did', did , info ) 
				arr.pop("info", None)
				redis.r.hset(f'txt-spacy:{name}:{did}', 'spacy', json.dumps(arr))
			except Exception as e:
				print ("ex:", e, sid, line[0:30]) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
		print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(util)