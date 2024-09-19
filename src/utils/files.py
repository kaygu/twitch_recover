def load_domains():
    '''
    Load domain hosts from txt file
    '''
    try:
        with open('domains.txt', 'r') as f:
            domains = f.read().splitlines()
    except:
        raise Exception('Something wrong happened while opening the file "domains.txt"')
    return domains