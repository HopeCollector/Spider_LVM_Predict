import configparser

a = configparser.ConfigParser()
a['LDA'] = {
    'topics':20,
    'iter':500,
    'random_state':1
}
a['SVM'] = {
    'C':1.0,
    'kernel':'rbf'
}

with open('./module.ini', 'w', encoding='utf-8') as f:
    a.write(f)