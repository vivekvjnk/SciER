## SciER

**We are working on the code and data clean now. This repo will be updated soon!!!**

The SciER dataset contains both entity annotation and relation annotation for scientific documents.


It covers three kinds of entity types:
- Dataset
- Method
- Task


In the './LLM' folder, each set/file has already been transfered to LLM friendly format.
Each row is a sentence and has following structure:

```json
"doc_id": // The document id of this sentence
"sentence": // The sentence text string
"ner": // A list of ner labels, each element contains the entity string and its entity type. E.g., ["Entity String", "Entity Type"] such as ['feature extraction mechanisms', 'Method']
"rel": // A list of relation labels, used for Relation Extraction. Each element is a triplet, e.g., [Subject Entity, Relation Type, Object Entity], such as ['attention', 'Part-Of', 'recurrent neural networks']
"rel_plus": // A list of strict relation labels, used for end-to-end Relation Extraction. Each element is a triplet, e.g., [Subject Entity:Entity Type, Relation Type, Object Entity:Entity Type], such as ['attention:Method', 'Part-Of', 'recurrent neural networks:Method']
```


In the './PLM' folder, each set/file is in the format to train supervised models. They are in the this format:

```json
{
  # document ID (please make sure doc_key can be used to identify a certain document)
  "doc_key": "CNN_ENG_20030306_083604.6",

  # sentences in the document, each sentence is a list of tokens
  "sentences": [
    [...],
    [...],
    ["tens", "of", "thousands", "of", "college", ...],
    ...
  ],

  # entities (boundaries and entity type) in each sentence
  "ner": [
    [...],
    [...],
    [[26, 26, "LOC"], [14, 14, "PER"], ...], #the boundary positions are indexed in the document level
    ...,
  ],

  # relations (two spans and relation type) in each sentence
  "relations": [
    [...],
    [...],
    [[14, 14, 10, 10, "ORG-AFF"], [14, 14, 12, 13, "ORG-AFF"], ...],
    ...
  ]
}

```
