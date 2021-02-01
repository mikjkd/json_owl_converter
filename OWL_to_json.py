from owlready2 import *
import json


def owl_to_json(all, f, s):
    data = []
    for index, elem in enumerate(f):
        for i in all:
            if str(i.is_a[0]) == elem:
                s.append(str(i))
        if s:
            data.append({elem: owl_to_json(all, s, [])})
            s = []
        else:
            data.append({elem: []})
    return data


if __name__ == "__main__":
    onto = get_ontology('data/CSOntology.owl').load()
    v = list(onto.classes())
    print(v)
    data = owl_to_json(v, ["CSOntology.ServiceCategory"], [])
    with open("ontology.json", "w") as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '))
