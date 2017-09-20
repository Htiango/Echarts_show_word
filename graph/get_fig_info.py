from django.db import connection
from collections import OrderedDict
from graph.create_fig_data import Graph
import json

from django.utils.safestring import mark_safe

class Fig_param:
    def __init__(self, data, title):
        
        self.data = data
        self.my_graph = Graph(title)
        self.node_id = 0
        self.link_id = 0
        self.label_word_node_ids= {}
        self.word_word_node_ids = {}

    def get(self):
        data = self.data
        for category in data:
            # print category
            self.add_layer1(category)
            top_words = sorted(data[category], key=data[category].__getitem__, reverse = True)
            for i in range(len(top_words)):
                top_word = top_words[i]
                # print top_word
                self.add_layer2(category, i, top_word)
                top_relations = sorted(data[category][top_word],
                    key=data[category][top_word].__getitem__, reverse = True)
                for j in range(len(top_relations)):
                    relation = top_relations[j]
                    self.add_layer3(category, j, top_word, relation, data[category][top_word][relation])
        json_str = self.my_graph.to_json_str()
        return json_str

    def add_layer1(self, label):
        self.my_graph.add_node(layer=1,
                                category=label,
                                node_id=self.node_id,
                                name='type',
                                value= label)
        self.label_word_node_ids[label] = self.node_id
        self.word_word_node_ids[label] = {}
        self.my_graph.add_categories(label)
        self.node_id += 1

    def add_layer2(self, label, index, word):
        self.my_graph.add_node(layer=2,
                               category=label,
                               node_id=self.node_id,
                               name=word,
                               index = index,
                               value= word)
        self.my_graph.add_link(node_id=self.link_id,
                               source=self.label_word_node_ids[label],
                               target=self.node_id)
        self.word_word_node_ids[label][word] = self.node_id
        self.node_id += 1
        self.link_id += 1
        

    def add_layer3(self, label, index, topword, word, sentenseList):
        self.my_graph.add_node(layer=3,
                               category=label,
                               node_id=self.node_id,
                               name=word,
                               value= word,
                               topword = topword,
                               sentenseList = sentenseList)
        self.my_graph.add_link(node_id=self.link_id,
                               source=self.word_word_node_ids[label][topword],
                               target=self.node_id)
        self.node_id += 1
        self.link_id += 1


if __name__ == '__main__':
    print 'Testing create_fig_data'