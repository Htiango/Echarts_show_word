#coding=UTF-8
import io
import os
import argparse
import json

def get_relation(args):
    #  first we load the json corpus file
    corpus = load_json(args.input)
    vocab_dict = corpus['vocab']
    doc = corpus['docs']
    word_freq = corpus['word_freq']

    vocab_reverse_dict = dict((v,k) for k, v in vocab_dict.iteritems())

    disease_set = load_dict_set(args.vocab_dis)
    symptom_set = load_dict_set(args.vocab_symp)
    drug_set = load_dict_set(args.vocab_drug)

    print 'load data!!'

    line_sen_dict = {}
    with open(args.input_text, 'r') as f:
        count_doc = 0
        for line in f:
            count_doc += 1
            line_sen_dict[str(count_doc)] = line.strip().decode('utf-8')

    print 'load text!!'

    drug_count = 0
    disease_count = 0
    symptom_count = 0

    drug_freq_dict = {}
    disease_freq_dict = {}
    symptom_freq_dict = {}

    for word in vocab_dict.keys():
        if word in disease_set:
            # print 'disease:', word
            disease_freq_dict[word] = word_freq[str(vocab_dict[word])]
            disease_count += 1
        if word in symptom_set:
            # print 'symptom:', word
            symptom_freq_dict[word] = word_freq[str(vocab_dict[word])]
            symptom_count += 1
        if word in drug_set:
            # print 'drug:', word
            drug_freq_dict[word] = word_freq[str(vocab_dict[word])]
            drug_count += 1

    print 'disease count =', disease_count
    print 'symptom count =', symptom_count
    print 'drug count =', drug_count

    topn = args.topn

    disease_top_ls = sorted(disease_freq_dict, 
        key = disease_freq_dict.__getitem__, reverse = True)[:topn]
    symptom_top_ls = sorted(symptom_freq_dict, 
        key = symptom_freq_dict.__getitem__, reverse = True)[:topn]
    drug_top_ls = sorted(drug_freq_dict, 
        key = drug_freq_dict.__getitem__, reverse = True)[:topn]

    # define top words' relation (top)
    dis_symp = {}
    dis_dis = {}
    dis_drug = {}

    symp_symp = {}
    symp_dis = {}
    symp_drug = {}

    drug_symp = {}
    drug_dis = {}
    drug_drug = {}

    for dis_w in disease_top_ls:
        # print dis_w
        dis_dis[dis_w], dis_symp[dis_w], dis_drug[dis_w]= get_top_relation(dis_w, 
            doc, disease_set, symptom_set, drug_set, vocab_dict, vocab_reverse_dict, topn)
        # print_dict(dis_dis[dis_w])
    print 'Finish disease counting'

    for symp_w in symptom_top_ls:
        # print symp_w
        symp_dis[symp_w], symp_symp[symp_w], symp_drug[symp_w]= get_top_relation(symp_w, 
            doc, disease_set, symptom_set, drug_set, vocab_dict, vocab_reverse_dict, topn)
        # print_dict(symp_dis[symp_w])
    print 'Finish symptom counting'

    for drug_w in drug_top_ls:
        drug_dis[drug_w], drug_symp[drug_w], drug_drug[drug_w] = get_top_relation(drug_w,
            doc, disease_set, symptom_set, drug_set, vocab_dict, vocab_reverse_dict, topn)
    print 'Finish drug counting'


    
    # Now we should go through the doc again to get the top words relation's sentense:
    dis_symp_sen = {}
    dis_dis_sen = {}
    dis_drug_sen = {}

    symp_symp_sen = {}
    symp_dis_sen = {}
    symp_drug_sen = {}

    drug_symp_sen = {}
    drug_dis_sen = {}
    drug_drug_sen = {}

    for dis_w in disease_top_ls:
        # print dis_w
        dis_dis_sen[dis_w], dis_symp_sen[dis_w], dis_drug_sen[dis_w]= get_top_sentense(dis_w, 
            doc, dis_dis[dis_w].keys(), dis_symp[dis_w].keys(), dis_drug[dis_w].keys(), 
            vocab_dict, vocab_reverse_dict, line_sen_dict)
        # print_dict(dis_dis[dis_w])
    print 'Finish disease sentense adding'

    for symp_w in symptom_top_ls:
        # print symp_w
        symp_dis_sen[symp_w], symp_symp_sen[symp_w], symp_drug_sen[symp_w]= get_top_sentense(symp_w, 
            doc, symp_dis[symp_w].keys(), symp_symp[symp_w].keys(), symp_drug[symp_w].keys(), 
            vocab_dict, vocab_reverse_dict, line_sen_dict)
        # print_dict(symp_dis[symp_w])
    print 'Finish symptom sentense adding'

    for drug_w in drug_top_ls:
        drug_dis_sen[drug_w], drug_symp_sen[drug_w], drug_drug_sen[drug_w] = get_top_sentense(drug_w,
            doc, drug_dis[drug_w].keys(), drug_symp[drug_w].keys(), drug_drug[drug_w].keys(),
            vocab_dict, vocab_reverse_dict, line_sen_dict)
    print 'Finish drug sentense adding'
        

    output = {u'疾病间的关联': dis_dis_sen, u'疾病对应症状': dis_symp_sen, u'疾病对应用药': dis_drug_sen, \
        u'症状对应疾病': symp_dis_sen, u'症状间的关联': symp_symp_sen, u'症状对应用药': symp_drug_sen, \
        u'用药对应疾病': drug_dis_sen, u'用药对应症状': drug_symp_sen, u'用药间的关联': drug_drug_sen}
    with io.open(args.output, 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, ensure_ascii=False))

    print_ls(disease_top_ls, disease_freq_dict)
    print_ls(symptom_top_ls,symptom_freq_dict)
    print_ls(drug_top_ls, drug_freq_dict)


def get_top_relation(word, doc, class_set1, class_set2, class_set3, 
    vocab_dict, vocab_reverse_dict, topn):
    word_relation1 = {}
    word_relation2 = {}
    word_relation3 = {}
    word_id = str(vocab_dict[word])
    for doc_id in doc:
        doc_words_ls = doc[doc_id].keys()
        doc_words_set = set(doc_words_ls)
        if word_id in doc_words_set:
            for doc_word_id in doc_words_ls:
                doc_word = vocab_reverse_dict[int(doc_word_id)]
                if int(doc_word_id) != int(word_id):
                    if doc_word in class_set1:
                        try:
                            word_relation1[doc_word] += doc[doc_id][doc_word_id]
                        except:
                            word_relation1[doc_word] = doc[doc_id][doc_word_id]
                    if doc_word in class_set2:
                        try:
                            word_relation2[doc_word] += doc[doc_id][doc_word_id]
                        except:
                            word_relation2[doc_word] = doc[doc_id][doc_word_id]
                    if doc_word in class_set3:
                        try:
                            word_relation3[doc_word] += doc[doc_id][doc_word_id]
                        except:
                            word_relation3[doc_word] = doc[doc_id][doc_word_id]
    

    return sort_dict(word_relation1, topn), sort_dict(word_relation2, topn), sort_dict(word_relation3, topn)

def get_top_sentense(word, doc, ls1, ls2, ls3, 
    vocab_dict, vocab_reverse_dict, line_sen_dict):
    word_sentense1 = {}
    word_sentense2 = {}
    word_sentense3 = {}
    word_id = str(vocab_dict[word])
    set1 = set(ls1)
    set2 = set(ls2)
    set3 = set(ls3)

    for doc_id in doc:
        doc_words_ls = doc[doc_id].keys()
        doc_words_set = set(doc_words_ls)
        if word_id in doc_words_set:
            sentense = line_sen_dict[doc_id]
            ls = []
            ls.append(sentense)
            for doc_word_id in doc_words_ls:
                word = vocab_reverse_dict[int(doc_word_id)]
                if word in set1:
                    try:
                        word_sentense1[word].append(sentense)
                    except :
                        word_sentense1[word] = ls
                if word in set2:
                    try:
                        word_sentense2[word].append(sentense)
                    except :
                        word_sentense2[word] = ls
                if word in set3:
                    try:
                        word_sentense3[word].append(sentense)
                    except :
                        word_sentense3[word] = ls

    return word_sentense1, word_sentense2, word_sentense3

def sort_dict(relation_dict, topn):
    result = {}
    top_relation_ls = sorted(relation_dict, 
        key = relation_dict.__getitem__, reverse = True)[:topn]
    for relation in top_relation_ls:
        result[relation] = relation_dict[relation]
    return result

def print_dict(dic):
    for key in dic:
        print key, dic[key]

def print_ls(ls, ls_dict):
    print '\n'
    for ob in ls:
        print ob, ls_dict[ob]
    print '\n'

def load_json(file):
    try:
        with open(file, 'r') as datafile:
            data = json.load(datafile)
    except Exception as e:
        raise e
    return data

def load_dict_set(file):
    words = []
    try:
        with open(file, 'r') as f:
            for line in f:
                # print(line);
                words.append(line.strip().decode('utf-8'))
    except Exception as e:
        raise e
    words_set = set()
    for word in words:
        words_set.add(word)
    return words_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, 
        required=True, help='path of the input words freq json file')  
    parser.add_argument('-text', '--input_text', type=str, 
        required=True, help='path of the input sentense file') 
    parser.add_argument('-vocab_dis', '--vocab_dis', type=str, 
        required=True, help='path of the vocab of disease file')
    parser.add_argument('-vocab_symp', '--vocab_symp', type=str, 
        required=True, help='path of the vocab of symptom file')
    parser.add_argument('-vocab_drug', '--vocab_drug', type=str, 
        required=True, help='path of the vocab of drug file')
    parser.add_argument('-o', '--output', type=str, 
        required=True, help='path of the output word freq dict')
    parser.add_argument('-threshold', '--threshold', type=int, 
        default=3, help='the threshold of the least show times')
    parser.add_argument('-tn', '--topn', type=int, 
        default = 15, help = 'number of top words of a cluster')

    # parser.add_argument('-ov', '--output_vocab', type=str, 
    #     required=True, help='path of the output vocab')
    args = parser.parse_args()

    get_relation(args)

if __name__ == "__main__":
    main()