import json
from owlready2 import *
from parse_json import *
from OWL_to_json import *
import types
import re

global onto


def insert_individual(onto_class, individual_name):
    ni = onto_class(individual_name)
    return ni


if __name__ == "__main__":
    # apro json
    f = open("data/Services.json")
    data = json.load(f)
    # apro ontologia
    onto = get_ontology('data/CSOntology.owl').load()
    # inserisco individui CloudProvider
    providers = parse_providers(data)
    # new_providers = map(lambda i: onto.CloudProvider(i), providers)
    for i in providers:
        ni = onto.CloudProvider(i)
    categories = parse_categories(data)
    # creo le classi di ServiceCategory
    for i in categories:
        i = re.sub('[^A-Za-z0-9]+', '', i)
        nc = types.new_class(i, (onto.ServiceCategory,))
    dp = parse_data_properties(data)
    # creo le datatype property
    with onto:
        for k in dp:
            e = re.sub('[^A-Za-z0-9]+', ' ', k).title().replace(' ', '')
            nc = type(e, (DatatypeProperty,), {'domain': [onto.ServiceCategory], 'range': [str]})

        # aggiungo le restrizioni alla classe
        for d in parse_data_properties_by_category_service(data, onto):
            # classe da ereditare
            name = d['name']
            sclass = d['class']
            attr = d['properties']
            nr = type(name, (onto[sclass],), {'is_a': attr})
    onto.save(file="data/CSOntologyExtended.owl")
