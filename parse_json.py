import re


def clean_category(c):
    c = c.title().replace(' ', '')
    c = re.sub('[^A-Za-z0-9]+', '', c)
    if 'Service' in c:
        return c.replace('Service', '')
    if 'Services' in c:
        return c.replace('Services', '')
    return c


def clean(i):
    i = i.title().replace(' ', '')
    i = re.sub('[^A-Za-z0-9]+', '', i)
    return i


def remove_duplicate(p):
    return list(dict.fromkeys(p))


def parse_providers(data):
    p = []
    for i in data:
        # ottengo tutte le chiavi
        k = i.keys()
        for j in k:
            if j != 'category' and j != "service":
                p.append(j)
    # rimuovo i duplicati
    return remove_duplicate(p)


def parse_categories(data):
    c = []
    for i in data:
        cat = i['category']['name']
        cat = clean_category(cat)
        c.append(cat)
    return remove_duplicate(c)


# not used
def parse_services_by_category(category, data):
    s = []
    for i in data:
        if i['category']['name'] == category:
            s.append(i['service'])
    return s


# not used
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
        v.append('ref')
        if v:
            dp.extend(v)
    return remove_duplicate(dp)


def parse_data_properties_by_category_service(data, onto):
    dpc = []
    for i in data:
        cn = i['category']['name']
        cn = clean_category(cn)
        sn = i['service']['name']
        sn = clean(sn)
        if cn == sn:
            sn = sn + 'Service'
        sp = i['service']['Properties']
        sp.append('ref')
        sp = list(map(lambda s: s.title().replace(' ', ''), sp))
        v = []
        for k in sp:
            v.append(onto[k].some(str))
        dpc.append({'category': cn, 'service': sn, 'properties': v})
    return dpc


def parse_individuals(data):
    ind = []
    for i in data:
        cn = i['category']['name']
        cn = clean_category(cn)
        sn = i['service']['name']
        sn = clean(sn)
        if cn == sn:
            sn = sn + 'Service'
        sp = i['service']['Properties']
        sp.append('ref')
        sp = list(map(lambda s: s.title().replace(' ', ''), sp))
        sp = remove_duplicate(sp)
        k = i.keys()
        v = []
        for j in k:
            if j != 'service' and j != 'category':
                for l in i[j]:
                    if l['name']:
                        lname = l['name']
                        lname = clean(lname)
                        # rendo minuscola prima lettera
                        lname = lname[0].lower() + lname[1:]
                        v.append({'vendor': j, 'individualName': lname, 'ref': l['ref'], 'properties': l['Properties']})
        ind.append({'service': sn, 'service_properties': sp, 'individuals': v})
    return ind
