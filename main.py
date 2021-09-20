import requests
import re
import json
import wget
import os

fabrics = [
    'paris'
]

def search_code(fab):
    '''if true returns search code else returns false'''
    search_url = 'https://www.elastrongroup.com/pt/?op=search&q=' # ={name of fabric}
    link_to_search = search_url + fab
    print('Searching by : ' + link_to_search)
    conn = requests.get(link_to_search)
    conn_result = conn.text
    search_result = re.findall(r"(Resultados da pesquisa para:  )([a-zA-Z]*)", conn_result)
    if search_result[0][1] == fab:
        fab_cod = re.findall(r"(true&co=)([0-9]*)", conn_result)[0][1]
        print('found code for ' + fab + ' : ' + fab_cod)
        print('---' * 5)
        print('\n')
        return fab_cod
    else:
        print('Fabric not found!')
        return False


def ajax_json(cod):
    '''return json file for collection cod'''
    url = "https://www.elastrongroup.com/pt/estofos/estofos-/?action=ajax"
    payload={'start': '0',
    'colecao': cod,
    'ordem': 'ordem_colecao'}
    files=[
    ]
    headers = {
    'Cookie': 'elastron=5folmnpba9uort3hgvkvvaads5; lang=pt'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    data = response.json()
    return data


def get_img_links(data:dict):
    '''return lint of dictionaries'''
    fav = ''
    link_buck = []

    if data:
        for i in data['produtos']:
            fav = i
        for x in data['produtos'][fav]['produtos']:
            link_buck.append(x)
    return link_buck


def save_imgs(fabrics):
    # save img (wget) - name - color
    for i in fabrics:
        colecao = i['colecao']
        cor = i['produto']
        link_img = i['imagem']

        img_name = colecao.strip() + '_' + cor.strip() + '.jpg'
        link_to_extract = link_img.replace('177X177', '744X734')
        
        is_created = os.path.exists(f'./imgs/{colecao}')

        if not is_created:
            os.mkdir(f'./imgs/{colecao}')

        file_to_save = f'./imgs/{colecao}/{img_name}'
        wget.download(link_to_extract, out=file_to_save)
        print(f'{file_to_save} -- Saved!')

        
def main():
    rev = 'bronx'
    cod = search_code(rev)
    data = None
    if cod:
        data = ajax_json(cod)
    links =  get_img_links(data)
    save_imgs(links)


if __name__ == '__main__':
    main()

