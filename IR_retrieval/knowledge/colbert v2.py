# Indexing
# For fast retrieval, indexing precomputes the ColBERT representations of passages.
#
# Example usage:

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Indexer

if __name__=='__main__':
    with Run().context(RunConfig(nranks=1, experiment="msmarco")):

        config = ColBERTConfig(
            nbits=2,
            root="/path/to/experiments",
        )
        indexer = Indexer(checkpoint="/path/to/checkpoint", config=config)
        indexer.index(name="msmarco.nbits=2", collection="/path/to/MSMARCO/collection.tsv")

# Retrieval
# We typically recommend that you use ColBERT for end-to-end retrieval, where it directly finds its top-k passages from the full collection:

from colbert.data import Queries
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher

if __name__=='__main__':
    with Run().context(RunConfig(nranks=1, experiment="msmarco")):

        config = ColBERTConfig(
            root="/path/to/experiments",
        )
        searcher = Searcher(index="msmarco.nbits=2", config=config)
        queries = Queries("/path/to/MSMARCO/queries.dev.small.tsv")
        ranking = searcher.search_all(queries, k=100)
        ranking.save("msmarco.nbits=2.ranking.tsv")


# Training
# We provide a pre-trained model checkpoint, but we also detail how to train from scratch here. Note that this example
# demonstrates the ColBERTv1 style of training, but the provided checkpoint was trained with ColBERTv2.
# Training requires a JSONL triples file with a [qid, pid+, pid-] list per line. The query IDs and passage IDs
# correspond to the specified queries.tsv and collection.tsv files respectively.
# Example usage (training on 4 GPUs):

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Trainer

if __name__=='__main__':
    with Run().context(RunConfig(nranks=4, experiment="msmarco")):

        config = ColBERTConfig(
            bsize=32,
            root="/path/to/experiments",
        )
        trainer = Trainer(
            triples="/path/to/MSMARCO/triples.train.small.tsv",
            queries="/path/to/MSMARCO/queries.train.small.tsv",
            collection="/path/to/MSMARCO/collection.tsv",
            config=config,
        )

        checkpoint_path = trainer.train()

        print(f"Saved checkpoint to {checkpoint_path}...")


# Advanced Training (ColBERTv2-style)
from colbert.infra.run import Run
from colbert.infra.config import ColBERTConfig, RunConfig
from colbert import Trainer


def train():
    # use 4 gpus (e.g. four A100s, but you can use fewer by changing nway,accumsteps,bsize).
    with Run().context(RunConfig(nranks=4)):
        triples = '/path/to/examples.64.json'  # `wget https://huggingface.co/colbert-ir/colbertv2.0_msmarco_64way/resolve/main/examples.json?download=true` (26GB)
        queries = '/path/to/MSMARCO/queries.train.tsv'
        collection = '/path/to/MSMARCO/collection.tsv'

        config = ColBERTConfig(bsize=32, lr=1e-05, warmup=20_000, doc_maxlen=180, dim=128, attend_to_mask_tokens=False, nway=64, accumsteps=1, similarity='cosine', use_ib_negatives=True)
        trainer = Trainer(triples=triples, queries=queries, collection=collection, config=config)

        trainer.train(checkpoint='colbert-ir/colbertv1.9')  # or start from scratch, like `bert-base-uncased`


if __name__ == '__main__':
    train()