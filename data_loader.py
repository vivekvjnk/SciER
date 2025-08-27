import json
from data_structures import Dataset
import os

def load_jsonl(jsonl_path:str) -> list:
    data = []
    with open(jsonl_path) as f:
        for line in f:
            data.append(json.loads(line))
    return data



if __name__=="__main__":
    # ========= usage example for load_jsonl function with LLM input =======
    dataset = load_jsonl('./SciER/LLM/test_ood.jsonl')
    # sent = dataset[5]
    print(f"Size of dataset : {len(dataset)}")
    docs = set([doc['doc_id'] for doc in dataset])
    print(f"number of docs: {len(docs)}")
    for i in range(5):
        print(dataset[i]['sentence'])
    # print(sent.keys())
    # print(sent['sentence'])
    # print('----------------')
    # print(sent['ner'])
    # print('----------------')
    # print(sent['rel'])
    # print('----------------')
    # print(sent['rel_plus'])



    # ========= usage example for Dataset class when using supervised methods
    dev_path = './SciER/PLM/dev.jsonl'
    dataset = Dataset(dev_path)
    for c, doc in enumerate(dataset):
        for i, sent in enumerate(doc):
            print(sent.text) # list of tokens of one sentence
            print(sent.ner) # list of NERs in the sentence
            exit()