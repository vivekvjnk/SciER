from collections import defaultdict
from data_loader import load_jsonl
import json
import yaml
import pandas as pd


def process_and_save_docs_to_md(data_list: list[dict]):
    """
    Processes a list of JSON-like dictionaries, extracts sentences,
    combines them by document ID, and saves the text to a Markdown file.

    Args:
        data_list: A list of dictionaries, where each dictionary
                   contains 'doc_id' and 'sentence' keys.
    """
    if not isinstance(data_list, list):
        print("Error: The input must be a list of dictionaries.")
        return

    # Use defaultdict to automatically create a list for each new doc_id
    grouped_sentences = defaultdict(list)

    # Group sentences by document ID
    for entry in data_list:
        try:
            doc_id = entry['doc_id']
            sentence = entry['sentence']
            grouped_sentences[doc_id].append(sentence)
        except KeyError as e:
            print(f"Skipping entry due to missing key: {e} in {entry}")

    # Process and save each document
    for doc_id, sentences in grouped_sentences.items():
        # Join all sentences into a single coherent text
        combined_text = ' '.join(sentences)

        # Create a filename using the document ID
        filename = f"extracted_srcs/doc_{doc_id}.md"

        try:
            # Open the file in write mode and save the text
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(combined_text)
            print(f"Successfully saved document with ID '{doc_id}' to {filename}")
        except IOError as e:
            print(f"Error: Could not save file {filename}. Reason: {e}")


def count_unique_ner_for_doc(data_list: list[dict], doc_id: str) -> int:
    """
    Counts the number of unique NER (Named Entity Recognition) elements for a
    specific document ID.

    The function iterates through a list of dictionaries, finds all entries
    that match the given doc_id, and collects all the NER elements from those
    entries. It uses a set to ensure that only unique elements are counted.

    Args:
        data_list: A list of dictionaries, where each dictionary contains
                   'doc_id', 'sentence', and 'ner' keys.
        doc_id: The document ID (as a string) to count unique NER elements for.

    Returns:
        The total count of unique NER elements for the specified document.
    """
    # Use a set to store unique NER elements. Tuples are used as set items
    # because lists (the default format of NER elements) are not hashable.
    unique_ners = set()

    # Iterate through each entry in the data list
    for entry in data_list:
        try:
            # Check if the current entry's doc_id matches the target doc_id
            if entry['doc_id'] == doc_id:
                # Iterate through the list of NER elements for this entry
                for ner_element in entry['ner']:
                    # Add the NER element (as a tuple) to the set
                    unique_ners.add(tuple(ner_element))
        except KeyError as e:
            # Print an error message if an entry is missing a required key
            print(f"Skipping an entry due to missing key: {e}")

    # Return the size of the set, which is the count of unique NER elements
    return len(unique_ners),unique_ners

def extract_entities(json_file, yaml_file, output_csv="entities.csv"):
    # --- Load JSON gold standard ---
    gold_entities = []
    with open(json_file, "r") as f:
        for line in f:
            data = json.loads(line.strip())
            doc_source = data.get("doc_id", "UnknownSource")  # keep document source
            for ent, etype in data.get("ner", []):
                gold_entities.append((
                    ent.strip(),
                    etype.strip(),
                    "Gold",
                    doc_source
                ))
    
    # Deduplicate JSON entities
    gold_entities = list({(e, t, s, d) for e, t, s, d in gold_entities})
    
    # --- Load YAML Bodhi output ---
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    
    bodhi_entities = []
    for node in data.get("nodes", []):
        ent_name = node["id"].strip()
        ent_type = node["type"].split(",")[0].strip()  # take first type if multiple
        bodhi_entities.append((
            ent_name,
            ent_type,
            "Bodhi",
            "Bodhi"  # no doc source for Bodhi
        ))
    
    # Deduplicate Bodhi entities
    bodhi_entities = list({(e, t, s, d) for e, t, s, d in bodhi_entities})
    
    # --- Combine ---
    entities = gold_entities + bodhi_entities
    df = pd.DataFrame(entities, columns=["Entity", "Type", "Source", "DocSource"])
    
    # Remove duplicates within same entity+source+doc
    df = df.drop_duplicates(subset=["Entity", "Source", "DocSource"])
    
    # Sort & group by DocSource
    df = df.sort_values(by=["DocSource", "Source", "Entity"]).reset_index(drop=True)
    
    # Save to CSV grouped by DocSource
    with open(output_csv, "w") as f:
        for doc_source, group in df.groupby("DocSource"):
            f.write(f"### DocSource: {doc_source}\n")
            group.to_csv(f, index=False)
            f.write("\n")
    
    return df

if __name__ == "__main__":
    dataset = load_jsonl('./SciER/LLM/test_ood.jsonl')
    # process_and_save_docs_to_md(data_list=dataset)
    number_of_entities,unique_entities = count_unique_ner_for_doc(data_list=dataset,doc_id="AAAI2024")
    print(f"Number of entities : {number_of_entities}\n{"*"*20}\n{unique_entities}")
    json_path = './SciER/LLM/test_ood.jsonl'
    yaml_path = '../../../infra/storage/Bodhi/doc_AAAI2024/doc_AAAI2024_graph.yml'
    extract_entities(json_file=json_path,yaml_file=yaml_path)

if __name__ == "__main__t":
    # Example usage with your provided JSON data
    # Note: The JSON provided is a string representation of multiple dictionaries.
    # We'll put them into a list for the function to process.
    json_data = [
        {
            "doc_id": "51923817",
            "sentence": "We propose CornerNet , a new approach to object detection where we detect an object bounding box as a pair of keypoints , the top - left corner and the bottom - right corner , using a single convolution neural network .",
            "ner": [["CornerNet", "Method"], ["object detection", "Task"], ["convolution neural network", "Method"]],
            "rel": [["convolution neural network", "Part-Of", "CornerNet"], ["CornerNet", "Used-For", "object detection"]],
            "rel_plus": [["convolution neural network:Method", "Part-Of", "CornerNet:Method"], ["CornerNet:Method", "Used-For", "object detection:Task"]]
        },
        {
            "doc_id": "51923817",
            "sentence": "Experiments show that CornerNet achieves a 4 2 . 2 % AP on MS COCO , outperforming all existing one - stage detectors .",
            "ner": [["CornerNet", "Method"], ["MS COCO", "Dataset"]],
            "rel": [["CornerNet", "Evaluated-With", "MS COCO"]],
            "rel_plus": [["CornerNet:Method", "Evaluated-With", "MS COCO:Dataset"]]
        },
        {
            "doc_id": "51923817",
            "sentence": "Object detectors based on convolutional neural networks ( ConvNets ) ( Krizhevsky et al. , 2 0 1 2 ; Simonyan and Zisserman , 2 0 1 4 ; He et al. , 2 0 1 6 ) have achieved state - of - the - art results on various challenging benchmarks ( Lin et al. , 2 0 1 4 ; Deng et al. , 2 0 0 9 ; Everingham et al. , 2 0 1 5 ) .",
            "ner": [["convolutional neural networks", "Method"], ["ConvNets", "Method"]],
            "rel": [["ConvNets", "Synonym-Of", "convolutional neural networks"]],
            "rel_plus": [["ConvNets:Method", "Synonym-Of", "convolutional neural networks:Method"]]
        }
    ]

    # Call the function with the example data
    process_and_save_docs_to_md(json_data)
