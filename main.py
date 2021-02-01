import json
from owlready2 import *
from parse_json import *
from OWL_to_json import *
import types
import re

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


        class hasProvider(ObjectProperty):
            domain = [onto.ServiceCategory]
            range = [onto.CloudProvider]


        # aggiungo le restrizioni alla classe
        for d in parse_data_properties_by_category_service(data, onto):
            # classe da ereditare
            name = d['name']
            name = re.sub('[^A-Za-z0-9]+', '', name)
            sclass = d['class']
            attr = d['properties']
            attr.append(onto.hasProvider.exactly(1,onto.CloudProvider))
            nr = type(name, (onto[sclass],), {'is_a': attr})
        #inserisco individui

        indlist = list(onto.individuals())

        for ind in parse_individuals(data):
            for i in ind['individuals']:
                indname = i['individualName']
                indname = re.sub('[^A-Za-z0-9]+', '', indname)
                indname = 'ind'+indname
                sname = ind['service']
                sname = re.sub('[^A-Za-z0-9]+', '', sname)

                new_ind = onto[sname](indname)
                new_ind.hasProvider = [onto[i['vendor']]]
                for pos,p in enumerate(ind['service_properties']):
                    if p == 'Ref':
                        setattr(new_ind, 'Ref', [i['ref']])
                    else:
                        try:
                            str_p = i['properties'][pos]
                            string_encode = str_p.encode("ascii", "ignore")
                            string_decode = string_encode.decode()
                            setattr(new_ind,p,[string_decode])
                        except IndexError:
                            setattr(new_ind,p,['To be added'])
    onto.save(file='data/CSOntologyExtended.owl')
