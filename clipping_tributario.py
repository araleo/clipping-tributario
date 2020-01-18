from datetime import date
import bs4, ezgmail, os, re, requests

valor_dados = {'nome': 'Valor Econômico', 'link': 'https://valor.globo.com/busca/?q=tributos&order=recent&from=now-1d'}
valor_seletores = {'titulo': '.widget--info__title', 'desc': '.widget--info__description', 'link': '.widget--info__text-container a'}

stf_dados = {'nome': 'Supremo Tribunal Federal', 'link': 'http://portal.stf.jus.br/listagem/listarNoticias.asp?dataDe=' + date.today().strftime('%d%m%Y') + '&dataA=&ori=1'}
stf_seletores = {'titulo': '#noticias a', 'desc': '.noticia-resumo', 'link': '#noticias a'}

jota_dados = {'nome': 'Jota', 'link': 'https://www.jota.info/tributos-e-empresas/tributario'}
jota_seletores = {'titulo': '.jota-cover__title a', 'desc': '.jota-cover__lead', 'link': '.jota-cover__title a'}

def captura_valor(link):
    valor_dic = {'link': '', 'desc': ''}

    res = requests.get(link)
    res.raise_for_status()
    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(sopa))

    res = requests.get(urls[0])
    res.raise_for_status()
    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_desc = sopa.select('.content-head__subtitle')

    valor_dic['link'] = urls[0]
    if sopa_desc:
        valor_dic['desc'] = sopa_desc[0].getText()

    return valor_dic

def formata(noticias, portal):
    outstring = ''
    if noticias['titulo']:
        outstring += '\n' + portal['nome'] + '\n'
        titulos = noticias['titulo']
        descricoes = noticias['desc']
        links = noticias['link']
        for i in range(len(titulos)):
            outstring += f"""

    {titulos[i]}

            {descricoes[i]}

            {links[i]}


"""

    return outstring

def busca(portal, seletores):
    res = requests.get(portal['link'])
    res.raise_for_status()

    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_titulo = sopa.select(seletores['titulo'])
    sopa_desc = sopa.select(seletores['desc'])
    sopa_link = sopa.select(seletores['link'])

    dicionario = {'titulo': [], 'desc': [], 'link': [], 'outstring': ''}

    for i in range(len(sopa_titulo)):

        dicionario['titulo'].append(sopa_titulo[i].getText().strip())

        if portal['nome'] == 'Valor Econômico':
            link_bruto = 'https:' + sopa_link[i].get('href')
            valor_dic = captura_valor(link_bruto)
            dicionario['link'].append(valor_dic['link'])
            dicionario['desc'].append(valor_dic['desc'].replace('\n',''))

        elif portal['nome'] == 'Supremo Tribunal Federal':
            dicionario['link'].append('http://portal.stf.jus.br' + sopa_link[i].get('href'))
            dicionario['desc'].append(sopa_desc[i].getText().replace('\n',''))

        elif portal['nome'] == 'Jota':
            dicionario['link'].append(sopa_link[i].get('href'))
            dicionario['desc'].append(sopa_desc[i].getText().replace('\n',''))

    dicionario['outstring'] = formata(dicionario, portal)

    return dicionario

def control(lista):
    noticias_string = f"Notícias tributárias de {date.today().strftime('%d/%m/%Y')}:" + '\n\n'
    for item in lista:
        noticias_string += item['outstring']

    return noticias_string

noticias_valor = busca(valor_dados, valor_seletores)
noticias_stf = busca(stf_dados, stf_seletores)
noticias_jota = busca(jota_dados, jota_seletores)

lista_noticias = [noticias_valor, noticias_stf, noticias_jota]

outstring = control(lista_noticias)

"""
print(outstring)
"""
ezgmail.send('mendes.lnr@gmail.com','Clipping Tributário',outstring)
ezgmail.send('barreto.isabelaa@gmail.com','Clipping Tributário',outstring)
