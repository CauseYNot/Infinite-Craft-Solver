
import csv
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        
        return json.JSONEncoder.default(self, obj)

with open('./base_recipes.csv') as file:
    reader = csv.reader(file, delimiter=',')
    label_to_id = {
        'ids': {
            'Water': '0',
            'Fire': '1',
            'Wind': '2',
            'Earth': '3'
        },
        'new_id': 4,
    }
    nodes = {
        '0': {
            'label': 'Water',
            'ingredient_one': '',
            'ingredient_two': '',
            'dependencies': set()
        },
        '1': {
            'label': 'Fire',
            'ingredient_one': '',
            'ingredient_two': '',
            'dependencies': set()
        },
        '2': {
            'label': 'Wind',
            'ingredient_one': '',
            'ingredient_two': '',
            'dependencies': set()
        },
        '3': {
            'label': 'Earth',
            'ingredient_one': '',
            'ingredient_two': '',
            'dependencies': set()
        },
    }
    new_id = 4
    for line in reader:
        if line == ['Component 1', 'Component 2', 'Product']:
            continue
            
        ingredient_one, ingredient_two, product = line
        if product not in label_to_id:
            label_to_id['ids'][product] = str(new_id)
            new_id += 1
        
        dependencies = set([ingredient_one, ingredient_two])
        if label_to_id['ids'].get(ingredient_one):
            dependencies.update(nodes[label_to_id['ids'][ingredient_one]]['dependencies'])
            
        if label_to_id['ids'].get(ingredient_two):
            dependencies.update(nodes[label_to_id['ids'][ingredient_two]]['dependencies'])
        
        nodes[label_to_id['ids'][product]] = {
            'label': product,
            'ingredient_one': ingredient_one,
            'ingredient_two': ingredient_two,
            'dependencies': dependencies
        }
    
    label_to_id['new_id'] = new_id

with open('nodes.json', 'w') as nodes_file, open('id.json', 'w') as id_file:
    nodes_file.write(json.dumps(nodes, indent=4, ensure_ascii=False, cls=SetEncoder))
    id_file.write(json.dumps(label_to_id, indent=4, ensure_ascii=False))