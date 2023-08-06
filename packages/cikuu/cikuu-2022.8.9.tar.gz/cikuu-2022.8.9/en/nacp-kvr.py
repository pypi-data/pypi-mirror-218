# 2023.67.24, kvr version  # 2023.2.9 , cp from sntjson-naclite.py | VBN -> past participle -> e | t -> to, b -> be , g -> VBG, c-> Clause , d-> ADV
import json, traceback,sys, time,  fileinput, os, fire,pathlib, platform, redis, spacy
from spacy.matcher import Matcher #from __init__ import *
from dic.wordlist import wordlist 
from collections import Counter,defaultdict
add		= lambda *names: [fire.ssi[ name.split('|')[0] ].update({ name.split('|')[-1] : 1}) for name in names if  not '\t' in name and len(name) <= 80 ]
zsum	= lambda key: sum([i for s,i in redis.r.zrevrange(key, 0, -1, True)])
if not hasattr(spacy, 'nlp'):
	spacy.nlp		= spacy.load(os.getenv('spacy_model','en_core_web_sm')) 
	spacy.from_json = lambda arr: spacy.tokens.Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19

def docs(name:str='gzjc'):
	for sid, line in enumerate(fileinput.input(f"{name}.jsonlg.3.4.1.gz",openhook=fileinput.hook_compressed)): 
		arr = json.loads(line.strip()) 
		doc = spacy.from_json(arr) 
		yield doc

phrase_rules={
		"prmods":[[{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]], # could hardly wait to meet
		"VP":  [[{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}], [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ","TO","PART"]}, "OP": "*"},{"POS": 'VERB'}]], # wait to meet
		"PP":  [[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]],    
		"AP":  [[{"POS": {"IN": ["ADV"]}, "OP": "+"}, {"POS": 'ADJ'}]],  
		"vpn": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}}, {"POS":"ADP"} , {"TAG":"NN", "IS_LOWER":True}]],  # come into force 
		"bpn": [[{"LEMMA":"be"}, {"POS":"ADP"} , {"TAG":"NN"}]],  # be in force => vpn 
		"vnp": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}}, {"TAG":"NN"}, {"POS":"ADP"} ]],  # make use of, lay emphasis on
		"vp": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}}, {"POS":"ADP"} ]],  # abide by | distinguish from
		"vpp": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}}, {"POS":"ADP"}, {"POS":"ADP"} ]], # live up to
		"vpg": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}}, {"POS":"ADP"}, {"TAG":"VBG","DEP":"pcomp"} ]], # insisted on going
		"pn": [[{"POS":"ADP", "DEP":"prep"} , {"TAG":"NN", "DEP":"pobj"}]],  # by force
		"pnp": [[{"POS":"ADP", "DEP":"prep"} , {"TAG":"NN", "DEP":"pobj"}, {"POS":"ADP", "DEP":"prep"}]],  # on account of
		"bapv": [[{"LEMMA":"be"} , {"TAG":{"IN": ["JJ"]}}, {"POS":"ADP"}, {"POS":"VERB"}]],  # 
		"batv": [[{"LEMMA":"be"} , {"TAG":{"IN": ["JJ"]}}, {"LEMMA":"to"}, {"POS":"VERB"}]],  
		"bepv": [[{"LEMMA":"be"} , {"TAG":{"IN": ["VBN"]}}, {"POS":"ADP"}, {"POS":"VERB"}]],  # be forced of going / ? bepv? 
		"betv": [[{"LEMMA":"be"} , {"TAG":{"IN": ["VBN"]}}, {"LEMMA":"to"}, {"TAG":"VB"}]],  # be considered to be/go
		"bap": [[{"LEMMA":"be"} , {"TAG":{"IN": ["JJ"]}}, {"POS":"ADP"}]], #be ignorant of
		"bep": [[{"LEMMA":"be"} , {"TAG":{"IN": ["VBN"]}}, {"POS":"ADP"}]],  # be forced to
		"vop": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}} , {"TEXT": {"REGEX": "[a-z]+self$"}}, {"POS":"ADP"}]], #throw oneself into
		"vtv": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}}, {"LEMMA":"to"}, {"POS":"VERB", "DEP":"xcomp"} ]], 
		"vg": [[{"POS":"VERB","TAG": {"NOT_IN": ["VBN"]}},  {"TAG":"VBG", "DEP":"xcomp"} ]], 
		"vdpg": [[{"POS":"VERB"},  {"POS":"ADV"} ,  {"POS":"ADP"} ,  {"TAG":"VBG"} ]],  # look forward to seeing
		}

def phrase_matcher( rules ={'pp':[[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]] }):
	''' for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text) '''
	matcher = Matcher(spacy.nlp.vocab)
	[matcher.add(name, pats,  greedy ='LONGEST') for name, pats in rules.items()]
	return matcher

class util(object): 
	def __init__(self, host='172.17.0.1', port=6206, withsnt:bool=False) : 
		redis.r = redis.Redis(host=host, port=port, decode_responses=True, health_check_interval=30)
		redis.withsnt = withsnt 
		fire.start = time.time()

	def tok(self, name): 
		''' python nacp-kvr.py tok gzjc '''
		print ( 'tok started :', name, redis.r, flush=True)
		fire.ssi = defaultdict(Counter)
		for doc in docs(name):
			try:
				add("#|sntnum") 
				[add(f"pos:LEM|{t.lemma_}", f"pos:LEX|{t.text.lower()}") for t in doc]
				[add(f"pos|{t.pos_}", f"pos:{t.pos_}|{t.lemma_}", f"pos:{t.pos_}:tag|{t.tag_}", f"pos:{t.pos_}:{t.tag_}|{t.text.lower()}", 
						f"{t.pos_}:{t.lemma_}|TAG:{t.tag_}", f"{t.pos_}:{t.lemma_}|LEX:{t.text.lower()}",	) for t in doc if t.pos_ not in ('PROPN','X', 'PUNCT','NUM','CD','SPACE','SYM') and t.is_alpha  and t.lemma_ in wordlist]

				# gzjc:LEM:book
				[add(f"LEM:{t.lemma_}|LEM:{t.lemma_}", f"LEM:{t.lemma_}|LEX:{t.text.lower()}"
					, f"LEM:{t.lemma_}|POS:{t.pos_}", f"LEM:{t.lemma_}|{t.pos_}:{t.tag_}") for t in doc if t.pos_ not in ('PROPN','X', 'PUNCT','NUM','CD','SPACE','SYM') and t.is_alpha and t.lemma_ in wordlist] #and t.is_lower

				for sp in doc.noun_chunks: #gzjc:NOUN:NP:boy => a boy
					if  sp.end - sp.start > 1 and doc[sp.end-1].pos_ not in ("PROPN",'X'): 
						lem = doc[sp.end-1].lemma_
						if lem in wordlist and lem.isalpha():
							add(f"{doc[sp.end-1].pos_}:{lem}|NP",f"{doc[sp.end-1].pos_}:NP:{lem}|{sp.text.lower()}")
				if redis.withsnt: 
					[redis.r.hsetnx(f"{name}:lem-snt", t.lemma_, ''.join([ f"<b>{k.text_with_ws}</b>" if k.i == t.i else k.text_with_ws for k in doc]) ) for t in doc if t.pos_ not in ('PROPN','X', 'PUNCT','NUM','SPACE') and t.is_alpha] # add <b> later 
			except Exception as e:
				print ("tok ex:", e) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)

		print("walking finished:" ) 
		[redis.r.zadd(f"{name}:{k}", v)  for k, v in fire.ssi.items()] # if not k.startswith('lem-lex') 
		# after tok is run,  yulk:gzjc:pos:VERB
		redis.r.zadd(f"{name}:#", {"wordsum": sum([i for s,i in redis.r.zrevrange(f"{name}:pos:LEX",0,-1, True)])}) #"sntnum": redis.r.hlen(f"hsnt-spacy:{name}"),
		for pos in ('NOUN','ADJ','ADV','VERB'):
			for lem, cnt in redis.r.zrevrange(f"{name}:pos:{pos}",0,-1, True):
				if lem.isalpha(): 
					redis.r.zadd(f"{name}:{pos}:{lem}", {"_sum": cnt})
		print("dumping finished:" ) 

	def trp(self, name): 
		''' python nacp-kvr.py trp gzjc '''
		print ( 'started trp:', name, redis.r, flush=True)
		fire.ssi = defaultdict(Counter)
		for doc in docs(name): 
			try:
				for t in doc: 
					if t.dep_ not in ('punct') and t.is_alpha and t.head.is_alpha and t.pos_ not in ('PUNCT','PROPN','X','NUM') and t.head.pos_ not in ('PUNCT','PROPN','X','NUM')  and t.lemma_ in wordlist and t.head.lemma_ in wordlist:
						add(f"{t.head.pos_}:{t.dep_}:{t.pos_}:{t.head.lemma_}|{t.lemma_}") #gzjc:VERB:dobj:NOUN:abandon 
						add(f"{t.head.pos_}:{t.head.lemma_}|{t.dep_}") #gzjc:VERB:abandon   dobj
						add(f"{t.head.pos_}:{t.head.lemma_}|{t.dep_}:{t.pos_}") #gzjc:VERB:abandon   dobj:NOUN
						if t.dep_ not in ('ROOT'):
							add(f"{t.pos_}:~{t.dep_}:{t.head.pos_}:{t.lemma_}|{t.head.lemma_}") #gzjc:ADJ:~amod:NOUN:advanced
							add(f"{t.pos_}:{t.lemma_}|~{t.dep_}") #gzjc:ADJ:advanced   ~amod
							add(f"{t.pos_}:{t.lemma_}|~{t.dep_}:{t.head.pos_}") 

						if redis.withsnt and t.pos_ not in ('PROPN','NUM','PUNCT','SYM') :
							snt = ''.join([ f"<b>{k.text_with_ws}</b>" if k.i in (t.i, t.head.i) else k.text_with_ws for k in doc])
							redis.r.hsetnx(f"{name}:trp-snt:{t.head.pos_}:{t.dep_}:{t.pos_}", f"{t.head.lemma_} {t.lemma_}", snt) # add highlight later 

						if t.dep_ == 'nsubjpass' and t.head.tag_ == 'VBN' and t.pos_ not in ('NUM') : # the fate is sealed  / smiling is banned .
							rel = f"{t.tag_}-be-{t.head.tag_}"
							add(f"{t.pos_}:{rel}:{t.lemma_}|{t.head.text.lower()}", f"{t.pos_}:{t.lemma_}|{rel}",)   # Smoking is banned. /VBG
							#	    f"{t.tag_}:~{rel}:{t.head.text.lower()}|{t.lemma_}", f"{t.tag_}:{t.head.text.lower()}|~{rel}" )

						if t.dep_ == 'xcomp' and t.pos_ == 'VERB':
							add(f"{t.head.pos_}:{t.head.lemma_}|xcomp-{t.tag_}", f"{t.head.pos_}:xcomp:{t.tag_}:{t.head.lemma_}|{t.text.lower()}",
							  # f"{t.tag_}:{t.lemma_}|~xcomp:{t.head.pos_}", f"{t.tag_}:~xcomp:{t.head.pos_}:{t.lemma_}|{t.head.lemma_}", 
							   f"{t.pos_}:{t.lemma_}|~xcomp-{t.head.pos_}", f"{t.pos_}:~xcomp:{t.head.pos_}:{t.lemma_}|{t.head.lemma_}", )

						if t.dep_ == 'ccomp' and t.head.pos_ == 'VERB':
							add(f"{t.head.pos_}:{t.head.lemma_}|vc",) #/rel
			except Exception as e:
				print ("trp ex:", e) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
		print("walking finished:" ) 
		for k, v in fire.ssi.items():  redis.r.zadd(f"{name}:{k}", v) 
		print("trp dumping finished:" ) 

	def kp(self, name): 
		''' python nacp-kvr.py kp gzjc '''
		print ( 'started kp:', name, redis.r, flush=True)
		fire.ssi = defaultdict(Counter)
		matcher = phrase_matcher(phrase_rules) 
		for doc in docs(name): 
			try:
				for n, start, end in matcher(doc):
					try:
						if doc[start].lemma_ in wordlist: 
							tag = spacy.nlp.vocab[n].text
							add(f"{doc[start].pos_}:{doc[start].lemma_}|XP:{tag}")
							add(f"{doc[start].pos_}:{tag}:{doc[start].lemma_}|" + doc[start].lemma_ + ' ' + doc[start+1:end].text) 
					except Exception as e:
						print ("postag_match ex:", e, n, start, end) 

			except Exception as e:
				print ("kp ex:", e) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
		print("walking finished:" ) 
		for k, v in fire.ssi.items():  redis.r.zadd(f"{name}:{k}", v) 
		print("dumping finished:" ) 

	def all(self, name):
		start = time.time() 
		print ( 'start to delete:', name, flush=True) 
		[ redis.r.delete(k) for k in redis.r.keys(f"{name}:*")]
		self.tok(name)
		self.trp(name)
		self.kp(name)

		for pos in ('NOUN','VERB','ADJ','ADV', 'LEM','LEX','ADP','PRON','CCONJ','SCONJ','PART'):  #		gzjc:pos:LEX
			redis.r.zadd(f"{name}:pos:{pos}", {"_sum": zsum(f"{name}:pos:{pos}")})
		
		si = Counter() # add avg verb/NOUN 
		for pos in ('NOUN','VERB','ADJ','ADV'): 
			for word in redis.r.zrevrange(f"{name}:pos:{pos}", 0, -1):
				for s,i in redis.r.zrevrange(f"{name}:{pos}:{word}", 0, -1, True): 
					if not s.startswith( 'LEX:'):
						si.update({s:i}) 
			print ( f'{pos} avg si:', len(si), flush=True) 
			redis.r.delete(f"{name}:{pos}:_avg")
			redis.r.zadd(f"{name}:{pos}:_avg", dict(si)) 
		print ("all finished:", name, " using:", round( time.time() - start , 2), ' seconds' )

if __name__	== '__main__':
	fire.Fire(util)

'''
2023.6.26: absorb dna (DNA)  dobj 

hyb:be able to _VERB|convince|72
could hardly wait to _VERB

root@172.17.0.1|nac>select *, round(count * 100 /per)  from clec where name = 'look:VERB:vpp';
+---------------+-------------------+-------+------+-------------------------+
| name          | attr              | count | per  | round(count * 100 /per) |
+---------------+-------------------+-------+------+-------------------------+
| look:VERB:vpp | look after in     |     1 |  2.7 |                      37 |
| look:VERB:vpp | look down on      |     3 |  8.1 |                      37 |

select * , keyness(cnt1, cnt2, sm1, sm2) kn from 
(select attr, count cnt1 , round(count * 100 /per) sm1 from gzjc where name = 'consider:VERB' and count > 3 ) a 
join 
(select attr, count cnt2, round(count * 100 /per) sm2 from gzjc where name = '*:VERB' and count > 10 ) b 
using (attr)
order by kn desc 

root@172.17.0.1|nac>select * from dic where name = 'book:NOUN:acl:VERB:call'; 
+-------------------------+----------------------------------------------------------------------------+-------+
| name                    | attr                                                                       | count |
+-------------------------+----------------------------------------------------------------------------+-------+
| book:NOUN:acl:VERB:call | By late 1983 I was putting the finishing touches on a book called Hackers. |     6 |
+-------------------------+----------------------------------------------------------------------------+-------+
1 row in set (0.005 sec)

def term(doc): 
	try:
		add( "SNTNUM|#")  
		for t in doc:
			lem,pos,tag,lex = t.lemma_, t.pos_, t.tag_, t.text.lower()
			add( "LEXSUM|#", f"#{pos}|#", f"#{tag}|#", f"#LEM|#", f"#LEX|#")
			if pos not in ('PROPN','X', 'PUNCT') : add(f"LEM|{lem}", f"{lem}:LEM|#", f"LEX|{lex}", f"{lem}:LEX|{lex}")
			if pos in ('VERB','NOUN','ADJ','ADV'): add(f"{pos}|{lem}", f"*|{pos}", f"{lem}|{pos}", f"{lem}:{pos}|{tag}", f"*:{pos}|{tag}", f"{tag}|{lex}") # VBD :  made , added 2022.12.10
	except Exception as e:
		print ("term ex:", e) 

				for kp, item in kp_born(doc).items(): # user_data 
					if 'nac' in item: 
						add(* item['nac'] ) 
				if (sid+1) % batch == 0 : 
					print (f"[{infile} -> {name}] sid = {sid}, \t| ", round(time.time() - start,1), flush=True)

				postag_match(doc, postag_func_kp) 
				trp3_match(doc, trp3_func_kp)
				merge_np(doc)  
				skenp_match(doc, skenp_func_kp)  #on_span(doc, skenp_func, 'skenp[')
				return doc.user_data

def docs(name:str='gzjc'):
	for k in redis.r.keys(f"snt-spacy:{name}:*"):
		v = redis.r.get(k)
		if not v: continue 
		arr = json.loads(v.strip()) 
		doc = spacy.from_json(arr) 
		yield doc 

ubuntu@ubuntu:/data/t/sntspacy$ time python3.8 nacp-kvr.py all sino
tok started : sino Redis<ConnectionPool<Connection<host=172.17.0.1,port=6206,db=0>>>
real	381m54.015s
user	224m25.334s
sys	36m22.697s

ubuntu@ubuntu:/data/t/sntspacy$ time python3.8 nacp-kvr.py all dic
real	72m34.839s
user	43m22.475s
sys	7m14.620s
	
'''