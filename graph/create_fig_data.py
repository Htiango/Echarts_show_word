import json

class Graph:
    def __init__(self, title):
        self.nodes = []
        self.links = []
        self.categories = []
        self.title = title

    def add_node(self, **kwargs):
        self.nodes.append(Node(**kwargs))

    def add_link(self, **kwargs):
        self.links.append(Link(**kwargs))

    def add_categories(self, name):
        self.categories.append(name)

    def to_json_str(self):
        json_str = json.dumps(self, default=lambda o: o.__dict__)
        return json_str


class Node:
    def __init__(self, **kwargs):
        layer = kwargs.get('layer',3)
        index = kwargs.get('index', 0)
        factor = float(100 - index) / 100

        if layer == 1:
            kwargs['symbolSize'] = 20
            kwargs['focusNodeAdjacency'] = True
            kwargs['fontSize'] = 15
            kwargs['fontWeight'] = 'bold'
            kwargs['layer'] = 1
        elif layer == 2:
            kwargs['symbolSize'] = 15 * factor
            kwargs['focusNodeAdjacency'] = True
            kwargs['fontSize'] = 12
            kwargs['layer'] = 2
        elif layer == 3:
            kwargs['symbolSize'] = 10 * factor
            kwargs['fontSize'] = 8
            kwargs['focusNodeAdjacency'] = True
            kwargs['layer'] = 3 
        self.category = kwargs.get('category', 0)
        self.id = kwargs.get('id', 0)
        self.draggable = kwargs.get('draggable', True)
        self.name = kwargs.get('name', '')
        self.value = kwargs.get('value', '')
        self.symbol = kwargs.get('symbol','circle')
        self.symbolSize = kwargs.get('symbolSize', 15)
        self.itemStyle = kwargs.get('itemStyle', None)
        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)
        self.focusNodeAdjacency = kwargs.get('focusNodeAdjacency', False)
        self.txt = kwargs.get('txt','')
        label = kwargs.get('label', True)
        fontSize = kwargs.get('fontSize', 12)
        fontWeight = kwargs.get('fontWeight','normal')

        self.hoverAnimation = kwargs.get('hoverAnimation', True)
        self.legendHoverLink = kwargs.get('legendHoverLink', True)
        self.layer = kwargs.get('layer', 4)
        self.sentenseList = kwargs.get('sentenseList', [])
        self.topword = kwargs.get('topword', '')

        if label:
            self.label = {'normal':{'show':True,
                                    'position':'right',
                                    'formatter':'{c}',
                                    'textStyle':{'fontSize':fontSize, 'fontWeight':fontWeight}}}


class Link:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.name = kwargs.get('name', '')
        self.source = kwargs.get('source', 0)
        self.target = kwargs.get('target', 0)
        self.lineStyle = {'normal': {'width': '1.2', 'color': '#283039'}}
