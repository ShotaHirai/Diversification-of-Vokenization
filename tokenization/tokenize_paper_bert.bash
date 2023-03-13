DATA_DIR=data/paper_valid
TOKENIZER=bert-base-uncased
python tokenization/tokenize_dataset.py $DATA_DIR test.raw $TOKENIZER
