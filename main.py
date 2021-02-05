import json
from owlready2 import *
from parse_json import *
from OWL_to_json import *
import types
import re
from consts import *

if __name__ == "__main__":
    # apro json
    f = open(FILE_SERVICES)
    data = json.load(f)
    # apro ontologia
    onto = get_ontology(CSONTOLOGY).load()
    # aggiungo AgnosticCloudService sotto CloudService
    agnostic_class = types.new_class(AGNOSTIC_CS, (onto.CloudService,))
    # aggiungo VendorSpecificCloudService sotto CloudService
    vendor_class = types.new_class(VENDOR_CS, (onto.CloudService,))
    # inserisco individui CloudProvider
    providers = parse_providers(data)
    # new_providers = map(lambda i: onto.CloudProvider(i), providers)
    for i in providers:
        ni = onto.CloudProvider(i)
    categories = parse_categories(data)
    # creo le classi di ServiceCategory
    for i in categories:
        nc = types.new_class(i, (onto.ServiceCategory,))
    dp = parse_data_properties(data)
    # creo le datatype property
    with onto:

        # aggiungo dinamicamente le datatype property alle classi di service category
        for k in dp:
            e = re.sub('[^A-Za-z0-9]+', ' ', k).title().replace(' ', '')
            nc = type(e, (DatatypeProperty,), {DOMAIN: [onto.ServiceCategory], RANGE: [str]})

        # aggiungo le restrizioni alla classe
        for d in parse_data_properties_by_category_service(data, onto):
            # classe da ereditare
            service = d[SERVICE]
            category = d[CATEGORY]
            attr = d[PROPERTIES]
            attr.append(onto.offeredBy.exactly(1, onto.CloudProvider))
            nr = type(service, (onto[category],), {ISA: attr})
            # creazione individuo agnostic

        # inserisco individui
        indlist = list(onto.individuals())

        for ind in parse_individuals(data):
            sname = ind[SERVICE]
            agnostic_ind = onto[service]('Agnostic_' + sname)
            agnostic_ind.is_a = [onto[AGNOSTIC_CS], onto[sname]]
            new_ind_list = []
            for i in ind[INDIVIDUALS]:
                indname = i[INDIVIDUAL_NAME]
                new_ind = onto[sname](indname)
                # creazione individuo collocato in VendorSpecificCloudService e nella classe Service corretta
                new_ind.is_a = [onto[VENDOR_CS], onto[sname]]
                new_ind.offeredBy = [onto[i[VENDOR]]]
                for pos, p in enumerate(ind[SERVICE_PROPERTIES]):
                    if p == 'Ref':
                        setattr(new_ind, 'Ref', [i[REF]])
                    else:
                        try:
                            str_p = i[PROPERTIES][pos]
                            string_encode = str_p.encode("ascii", "ignore")
                            string_decode = string_encode.decode()
                            setattr(new_ind, p, [string_decode])
                        except IndexError:
                            setattr(new_ind, p, [TO_BE_ADDED])
                new_ind_list.append(new_ind)
            # dico che individuo agnostico è equivalente a lista individui vendor specific
            agnostic_ind.isServiceEquivalent = new_ind_list
    onto.save(file=CSONTOLOGYEXTENDED)
