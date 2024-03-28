from datasketch import MinHashLSH, MinHash
from nltk import ngrams

df = train_dataset

def remove_duplicates_minhash(df):

    lsh = MinHashLSH(threshold=0.85, num_perm=128)

    for i, text in enumerate(df['text']):
        minhash = MinHash(num_perm=128)
        for word in text.split():
            minhash.update(word.encode('utf-8'))
        lsh.insert(str(i), minhash)

    unique_documents = set()

    for i, text in enumerate(df['text']):
        query_minhash = MinHash(num_perm=128)
        for word in text.split():
            query_minhash.update(word.encode('utf-8'))
        results = lsh.query(query_minhash)
        unique_documents.add(results[0])

    total_unique_documents = len(unique_documents)
    total_documents = len(df)
    duplication_ratio = (total_documents - total_unique_documents) / total_documents
    return duplication_ratio


def process_data(df):
    minhashes = {}
    for idx, text in enumerate(df['text']):
        minhash = MinHash(num_perm=128)
        for d in ngrams(text, 13):
            s = "".join(d).encode('utf-8')
            minhash.update(s)
        minhashes[idx] = minhash
    return minhashes

def identify_test_set(train_dataset,test_dataset):

    train_minhashes = process_data(train_dataset)
    test_minhashes = process_data(test_dataset)

    lsh = MinHashLSH(threshold=0.8, num_perm=128)

    for idx, minhash in train_minhashes.items():
        lsh.insert(idx, minhash)

    duplicates_count = 0
    for idx, minhash in test_minhashes.items():
        result = lsh.query(minhash)
        if len(result) > 0:
            duplicates_count += 1

    contamination_ratio = duplicates_count / len(test_dataset)
    return contamination_ratio
