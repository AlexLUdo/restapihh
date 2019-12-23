import requests
import json
import pprint

domain = 'https://api.hh.ru/'
url = f'{domain}vacancies'
params = {}
text_query = input('ENTER REQUEST (FOR EXAMPLE "Python or JAVA or Delphi etc..."): ')
params['text'] = text_query
area_query=int(input('WHERE WOULD YOU LIKE TO WORK? (1 - MOSCOW, 2 - SPb, 113 - RUSSIA): '))
params['area'] = str(area_query)
result=requests.get(url, params = params).json()
all_found_vac=result['found']
vse_stranitsy=result['found']//100+1 if result['found']//100 <= 20 else 20
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(f'FOR YOUR REQUEST: {params}, FIND {all_found_vac} VACANCY')
vse_skily = {}
for i in range(vse_stranitsy):
    params['page']=i
    result=requests.get(url, params = params).json()
    for j in result['items']:
        rez_tmp=requests.get(j['url']).json()
        for i in rez_tmp['key_skills']:
            if i['name'] in vse_skily:
                vse_skily[i['name']]+=1
            else:
                vse_skily.setdefault(i['name'], 1)
all_keys=0
for i in vse_skily:
    all_keys += vse_skily[i]
for i in vse_skily:
    vse_skily[i] = [vse_skily[i], str(round(vse_skily[i]/all_keys*100,2))+'%%']
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(f'NEEDS SKILL FOR THIS REQUEST {text_query}: ')
pprint.pprint(vse_skily)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
if input('SAVE REQUEST INTO FILE (y/n)? ') !='n':
    file_name=str(input('ENTER FILE NAME: ')) +'.json'
    with open(file_name, 'w') as f:
        json.dump({'params':params}, f)
        json.dump({'count':all_found_vac}, f)
        json.dump({'skills':vse_skily}, f)