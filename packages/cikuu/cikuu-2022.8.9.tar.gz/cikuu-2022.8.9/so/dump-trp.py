# 2023.5.22
import requests, traceback,sys , fire,spacy,os,json
from elasticsearch import Elasticsearch,helpers
from collections import Counter 

save_csv	= lambda si, _sum, fw:  ( fw.write("word,count\n"), [fw.write(f"{s},{i}\n") for s,i in si.most_common()], fw.write(f"_wordsum,{_sum}\n") )
save_json	= lambda si, _sum, fw:  ( si.update({"_wordsum":_sum}), fw.write( json.dumps(si) + "\n") )
mapf = {"csv": save_csv, "json": save_json}

def run(index, rel:str='dobj', gov:str='VERB', dep:str='NOUN', suffix:str='csv', eshost:str='172.17.0.1:9200',  debug:bool=False):
	''' python dump-trp.py gzjc --pos VERB/LEX/LEM --sufix json/csv '''
	print ('[estrp] start to walk:', index, suffix, eshost, flush=True)
	es	= Elasticsearch([ f"http://{eshost}" ])   # {'_index': 'nju2020', '_type': '_doc', '_id': 'doc-8697:snt-0:tok-15', '_score': None, '_source': {'level': 'gsl1', 'i': 15, 'idf': 2.6, 'type': 'tok', 'rid': 10, 'dep': 'conj', 'govlem': 'be', 'govpos': 'VERB', 'uid': 3544545, 'lem': 'have', 'pos': 'VERB', 'tag': 'VBZ', 'sntid': 'doc-8697:snt-0', 'did': 8697, 'lex': 'has'}, 'sort': [32]}
	si	= Counter()
	_sum = 0 
	for doc in helpers.scan(client=es, query={"query" : {"match" : {"type":"tok"}} }, index=index): 
		try:
			item = doc['_source']
			_sum = _sum + 1
			if item['dep'] == rel and item['govpos'] == gov and item['pos'] == dep and item['lem'].isalpha() and item['govlem'].isalpha():
				si.update({item['govlem'] + " " + item['lem']:1})
		except Exception as ex:
			print(">>eswalk ex:", ex)
	
	# _sum = sum([i for s,i in si.items()])
	with open(f"{index}-{rel}-{gov}-{dep}.{suffix}", 'w') as fw : 
		mapf[suffix](si, _sum, fw)

	print ('finished estrp:', index, suffix, flush=True)

if __name__ == '__main__':
	fire.Fire(run)