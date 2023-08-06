# 2023.7.5 cp from batch-sntspacy.py 
# 2023.5.12, one line one snt, spacy json result 
import requests,time, fire,json, fileinput ,traceback, dic
from dic import word_idf, yulk 
from __init__ import * 

def run(name, index:str=None, debug:bool=False, tok:bool=True, reset:bool=True, batch:int=100000):
	''' name=gzjc/clec '''
	if index is None : index = name.split('.')[0]
	if reset: drop(index)
	check(index) 
	word_level = dic.word_level()  
	print ( 'started:', index, batch, flush=True)

	start = time.time()
	for did, doc in enumerate(yulk.docs('gzjc')) : 
		try:
			sntid = f"snt-{did}"
			source = skenp(doc)
			source.update({"did":sntid, "type":"snt", "tc": len(doc),"snt":doc.text.strip()}) 
			addaction( {'_op_type':'index', '_index':index, '_id': sntid, '_source': source }, batch)
			
			if tok: 
				for t in doc:
					ar = {"did": sntid, 'i': t.i, 'type':'tok','lex': t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, 'glem': t.head.lemma_, 'gpos': t.head.pos_, 'gtag': t.head.tag_ }
					idf = word_idf.word_idf.get(t.text.lower(), 0)
					if idf : ar.update({"idf":idf})
					level = word_level.get(t.text.lower(), '') 
					if level: ar.update({"level":level})
					addaction( {'_op_type':'index', '_index':index, '_id': f"{sntid}:tok-{t.i}", '_source': ar } )

		except Exception as e:
			print("ex:", e)	

	submit_actions()
	print(f"indexing finished: {index}, \t| using: ", time.time() - start) 

if __name__ == '__main__': 	#run('testdoc', debug=True)
	fire.Fire(run)