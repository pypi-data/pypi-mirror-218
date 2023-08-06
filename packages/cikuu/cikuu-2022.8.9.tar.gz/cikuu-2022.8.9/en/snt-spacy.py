# 2023.67.24, kvr version  # 2023.2.9 , cp from sntjson-naclite.py | VBN -> past participle -> e | t -> to, b -> be , g -> VBG, c-> Clause , d-> ADV
import json, traceback,sys, time,  fileinput, os, fire,pathlib, platform, redis, spacy

if not hasattr(spacy, 'nlp'):
	spacy.nlp		= spacy.load(os.getenv('spacy_model','en_core_web_sm')) # 3.4.1
	spacy.from_json = lambda arr: spacy.tokens.Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19

def run(infile, host='172.17.0.1', port=6206, ):
	''' in tx98, 6206 '''
	name = infile.split('/')[-1].split('.')[0] # gzjc 
	redis.r = redis.Redis(host=host, port=port, decode_responses=True)
	print ("snt-spacy started:", name ,  ' -> ',  redis.r, flush=True)
	start = time.time()

	redis.r.hset("snt-spacy", name, 0) 
	for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #356317 docs of each doc file
		try:
			arr = json.loads(line.strip()) 
			doc = spacy.from_json(arr) 
			snt = doc.text.strip()
			redis.r.hincrby("snt-spacy", name) 
			redis.r.setnx(f"snt-spacy:{name}:{snt}", line) #avoid a super large key 
		except Exception as e:
			print ("ex:", e, sid, line[0:30]) 
			exc_type, exc_value, exc_traceback_obj = sys.exc_info()
			traceback.print_tb(exc_traceback_obj)

	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(run)