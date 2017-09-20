import io
import os
import argparse
import jieba
import json
from collections import defaultdict

def get_word_freq(args):
    textfile = args.input_text
    dictionary_file = args.input_dict
    jieba.load_userdict(dictionary_file)
    stopwords_file = args.stop_words
    stop_words_set = load_stopwords(stopwords_file)
    print 'Finish loading the dictionary and the stopwords'

    word_freq = defaultdict(lambda: 0) # count the number of times a word appears in a corpus
    doc_word_freq = defaultdict(dict) # count the number of times a word appears in a doc

    with open(textfile, 'r') as f:
        count_doc = 0
        for line in f:
            count_doc += 1
            if count_doc % 10000 == 0:
                print 'line-', count_doc
            text = line.strip().decode('utf-8')
            words = tokenize(text, stop_words_set)
            for word in words:
                word = word
                # print isinstance(word, str)
                # print word
                try:
                    doc_word_freq[count_doc][word] += 1
                except:
                    doc_word_freq[count_doc][word] = 1
                word_freq[word] += 1

    print 'Finish building the words freq dict'

    vocab_dict = build_vocab(word_freq, threshold=args.threshold)
    docs = generate_bow(doc_word_freq, vocab_dict)
    new_word_freq = dict([(vocab_dict[word], freq) for word, freq in word_freq.iteritems() if word in vocab_dict])

    corpus = {'docs': docs, 'vocab': vocab_dict, 'word_freq': new_word_freq}
    with io.open(args.output, 'w', encoding='utf-8') as f:
        f.write(json.dumps(corpus, ensure_ascii=False))
    print 'Generate the corpus!'


def load_stopwords(file):
    stop_words = []
    try:
        with open(file, 'r') as f:
            for line in f:
                # print(line);
                stop_words.append(line.strip().decode('utf-8'))
    except Exception as e:
        raise e
    stop_words_set = set()
    for word in stop_words:
        stop_words_set.add(word)
    return stop_words_set

def tokenize(text, stop_words_set):
    words = []
    try:
        s_ls = jieba.lcut(text, cut_all = False)
        for token in s_ls:
            if not token.isdigit() and not token in stop_words_set:
                words.append(token)
        return words
    except Exception, e:
        print 'Error in tokenize words'
        raise e

def build_vocab(word_freq, threshold=5, topn=None, start_idx=0):
    """
    threshold only take effects when topn is None.
    words are indexed by overall frequency in the dataset.
    """
    word_freq = sorted(word_freq.iteritems(), key=lambda d:d[1], reverse=True)
    if topn:
        word_freq = zip(*word_freq[:topn])[0]
        vocab_dict = dict(zip(word_freq, range(start_idx, len(word_freq) + start_idx)))
    else:
        idx = start_idx
        vocab_dict = {}
        for word, freq in word_freq:
            if freq < threshold:
                return vocab_dict
            vocab_dict[word] = idx
            idx += 1
    return vocab_dict

def generate_bow(doc_word_freq, vocab_dict):
    docs = {}
    for key, val in doc_word_freq.iteritems():
        word_count = {}
        for word, freq in val.iteritems():
            try:
                word_count[vocab_dict[word]] = freq
            except: # word is not in vocab, i.e., this word should be discarded
                continue
        docs[key] = word_count

    return docs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_text', type=str, 
        required=True, help='path of the input text file')  
    parser.add_argument('-dict', '--input_dict', type=str, 
        required=True, help='path of the dictionary file')
    parser.add_argument('-st', '--stop_words', type=str, 
        required=True, help='path of the stopwords file')
    parser.add_argument('-o', '--output', type=str, 
        required=True, help='path of the output dict')
    parser.add_argument('-threshold', '--threshold', type=int, 
        default=3, help='the threshold of the word_freq')
    args = parser.parse_args()

    get_word_freq(args)

if __name__ == "__main__":
    main()