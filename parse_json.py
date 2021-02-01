import re


def parse_providers(data):
    p = []
    for i in data:
        # ottengo tutte le chiavi
        k = i.keys()
        for j in k:
            if j != 'category' and j != "service":
                p.append(j)
    # rimuovo i duplicati
    return list(dict.fromkeys(p))


def parse_categories(data):
    c = []
    for i in data:
        c.append(i['category']['name'])
    return list(dict.fromkeys(c))


def parse_services_by_category(category, data):
    s = []
    for i in data:
        if i['category']['name'] == category:
            s.append(i['service'])
    return s


def parse_services(data):
    s = []
    cname = []
    for i in data:
        cname.append(i['category']['name'])
    cname = list(dict.fromkeys(cname))
    for i in cname:
        s.append({i: parse_services_by_category(i, data)})
    return s


def parse_data_properties(data):
    dp = []
    for i in data:
        v = i['service']['Properties']
        if v:
            dp.extend(v)
    return list(dict.fromkeys(dp))


def parse_data_properties_by_category_service(data, onto):
    dpc = []
    for i in data:
        cn = i['category']['name']
        cn = re.sub('[^A-Za-z0-9]+', '', cn)
        cn = cn.replace(' ', '')
        sn = i['service']['name']
        sn = 'S' + sn.title().replace(' ', '')
        sp = i['service']['Properties']
        sp = list(map(lambda s: s.title().replace(' ', ''), sp))
        v = []
        for k in sp:
            v.append(onto[k].some(str))
        dpc.append({'class': cn, 'name': sn, 'properties': v})
    return dpc
