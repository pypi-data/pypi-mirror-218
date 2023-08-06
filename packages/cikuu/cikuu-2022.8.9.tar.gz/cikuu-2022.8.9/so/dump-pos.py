# 2023.5.19
import requests, traceback,sys , fire,spacy,os,json
from elasticsearch import Elasticsearch,helpers
from collections import Counter 

save_csv	= lambda si, _sum, fw:  ( fw.write("word,count\n"), [fw.write(f"{s},{i}\n") for s,i in si.most_common()], fw.write(f"_wordsum,{_sum}\n") )
save_json	= lambda si, _sum, fw:  ( si.update({"_wordsum":_sum}), fw.write( json.dumps(si) + "\n") )
mapf = {"csv": save_csv, "json": save_json}

def run(index, pos:str='VERB', suffix:str='csv', eshost:str='172.17.0.1:9200',  debug:bool=False):
	''' python dump-pos.py nju2020 --pos VERB/LEX/LEM --sufix json/csv '''
	print ('[estok] start to walk:', index, pos, suffix, eshost, flush=True)
	es	= Elasticsearch([ f"http://{eshost}" ])   # {'_index': 'nju2020', '_type': '_doc', '_id': 'doc-8697:snt-0:tok-15', '_score': None, '_source': {'level': 'gsl1', 'i': 15, 'idf': 2.6, 'type': 'tok', 'rid': 10, 'dep': 'conj', 'govlem': 'be', 'govpos': 'VERB', 'uid': 3544545, 'lem': 'have', 'pos': 'VERB', 'tag': 'VBZ', 'sntid': 'doc-8697:snt-0', 'did': 8697, 'lex': 'has'}, 'sort': [32]}
	si	= Counter()
	for doc in helpers.scan(client=es, query={"query" : {"match" : {"type":"tok"}} }, index=index): #"pos":pos
		try:
			if pos =='LEX' and doc['_source']['lex'].isalpha() : si.update({doc['_source']['lex']:1})
			elif pos =='LEM' and doc['_source']['lem'].isalpha(): si.update({doc['_source']['lem']:1})
			elif doc['_source']['pos'] == pos and 'lem' in doc['_source'] and doc['_source']['lem'].isalpha():  si.update({doc['_source']['lem']:1})
		except Exception as ex:
			print(">>eswalk ex:", ex)
	
	_sum = sum([i for s,i in si.items()])
	with open(f"{index}-{pos}.{suffix}", 'w') as fw : 
		mapf[suffix](si, _sum, fw)

	print ('finished estok:', index, pos, suffix, flush=True)

if __name__ == '__main__':
	fire.Fire(run)