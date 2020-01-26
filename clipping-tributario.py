from datetime import date
import bs4, ezgmail, os, re, requests


valor_dados_1 = {'nome': 'Valor Econômico', 'link': 'https://valor.globo.com/busca/?q=tributo&order=recent&page=1&from=now-1d'}
valor_dados_2 = {'nome': 'Valor Econômico', 'link': 'https://valor.globo.com/busca/?q=tributos&order=recent&from=now-1d'}
valor_dados_3 = {'nome': 'Valor Econômico', 'link': 'https://valor.globo.com/busca/?q=tributario&order=recent&from=now-1d&page=1'}
valor_seletores = {'titulo': '.widget--info__title', 'desc': '.widget--info__description', 'link': '.widget--info__text-container a'}
lista_titulos_valor = []

stf_dados = {'nome': 'Supremo Tribunal Federal', 'link': 'http://portal.stf.jus.br/listagem/listarNoticias.asp?dataDe=' + date.today().strftime('%d%m%Y') + '&dataA=&ori=1'}
stf_seletores = {'titulo': '#noticias a', 'desc': '.noticia-resumo', 'link': '#noticias a'}

jota_dados = {'nome': 'Jota', 'link': 'https://www.jota.info/tributos-e-empresas/tributario'}
jota_seletores = {'titulo': '.jota-cover__title a', 'desc': '.jota-cover__lead', 'link': '.jota-cover__title a'}

sacha_dados = {'nome': 'Informativo Sacha Calmon', 'link': 'https://sachacalmon.com.br/categoria/resenha-tributaria'}
sacha_seletores = {'titulo': '.artigo-feed-archive h2', 'link': '.artigo-feed-archive a'}


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


def busca_sacha(portal, seletores):
    dicionario = {'titulo': [], 'desc': [], 'link': [], 'outstring': ''}

    res = requests.get(portal['link'])
    res.raise_for_status()

    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_titulo = sopa.select(seletores['titulo'])
    sopa_link = sopa.select(seletores['link'])

    titulo_materia = sopa_titulo[0].getText().strip()
    link_materia = sopa_link[0].get('href')

    res = requests.get(link_materia)
    res.raise_for_status()

    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_data = sopa.select('.data-artigo p')

    data_materia = sopa_data[0].getText()

    hoje = date.today().strftime('%d/%m/%Y')

    if data_materia == hoje:
        dicionario['titulo'].append('Novo Informativo')
        dicionario['desc'].append(titulo_materia)
        dicionario['link'].append(link_materia)

    dicionario['outstring'] = formata(dicionario, portal)

    return dicionario


def busca_jota(portal, seletores):
    dicionario = {'titulo': [], 'desc': [], 'link': [], 'outstring': ''}

    res = requests.get(portal['link'])
    res.raise_for_status()

    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_titulo = sopa.select(seletores['titulo'])
    sopa_desc = sopa.select(seletores['desc'])
    sopa_link = sopa.select(seletores['link'])

    for i in range(len(sopa_titulo)):
        res = requests.get(sopa_link[i].get('href'))
        res.raise_for_status()

        sopa = bs4.BeautifulSoup(res.text, 'html.parser')
        sopa_data = sopa.select('.jota-article__date-created')
        dia_noticia = sopa_data[0].getText().strip()[:10]

        if dia_noticia == date.today().strftime('%d/%m/%Y'):
            dicionario['titulo'].append(sopa_titulo[i].getText().strip())
            dicionario['desc'].append(sopa_desc[i].getText())
            dicionario['link'].append(sopa_link[i].get('href'))

    dicionario['outstring'] = formata(dicionario, portal)

    return dicionario


def busca_valor(portal, seletores):
    dicionario = {'titulo': [], 'desc': [], 'link': [], 'outstring': ''}
    lista_titulos = []

    res = requests.get(portal['link'])
    res.raise_for_status()

    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_titulo = sopa.select(seletores['titulo'])
    sopa_desc = sopa.select(seletores['desc'])
    sopa_link = sopa.select(seletores['link'])


    for i in range(len(sopa_titulo)):
        titulo_materia = sopa_titulo[i].getText().strip()
        link_materia = sopa_link[i].get('href')
        desc_materia = sopa_desc[i].getText().replace('\n','')

        if titulo_materia not in lista_titulos:
            lista_titulos.append(titulo_materia)
            dicionario['titulo'].append(titulo_materia)
            link_bruto = 'https:' + link_materia

            res = requests.get(link_bruto)
            res.raise_for_status()
            sopa = bs4.BeautifulSoup(res.text, 'html.parser')
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(sopa))

            res = requests.get(urls[0])
            res.raise_for_status()
            sopa = bs4.BeautifulSoup(res.text, 'html.parser')
            nova_desc = sopa.select('.content-head__subtitle')

            dicionario['link'].append(urls[0])
            if nova_desc:
                dicionario['desc'].append(nova_desc[0].getText().replace('\n',''))

            dicionario['outstring'] = formata(dicionario, portal)

    return dicionario


def busca_supremo(portal, seletores):
    dicionario = {'titulo': [], 'desc': [], 'link': [], 'outstring': ''}

    res = requests.get(portal['link'])
    res.raise_for_status()

    sopa = bs4.BeautifulSoup(res.text, 'html.parser')
    sopa_titulo = sopa.select(seletores['titulo'])
    sopa_desc = sopa.select(seletores['desc'])
    sopa_link = sopa.select(seletores['link'])

    for i in range(len(sopa_titulo)):
        titulo_materia = sopa_titulo[i].getText().strip()
        link_materia = sopa_link[i].get('href')
        desc_materia = sopa_desc[i].getText().replace('\n','')

        dicionario['titulo'].append(titulo_materia)
        dicionario['link'].append('http://portal.stf.jus.br' + link_materia)
        dicionario['desc'].append(desc_materia)

    dicionario['outstring'] = formata(dicionario, portal)

    return dicionario


def control(lista):
    noticias_string = f"Notícias tributárias de {date.today().strftime('%d/%m/%Y')}:" + '\n\n'
    for item in lista:
        noticias_string += item['outstring']

    return noticias_string


noticias_sacha = busca_sacha(sacha_dados, sacha_seletores)
noticias_valor = busca_valor(valor_dados_1, valor_seletores)
noticias_valor = {**busca_valor(valor_dados_2, valor_seletores), **noticias_valor}
noticias_valor = {**busca_valor(valor_dados_3, valor_seletores), **noticias_valor}
noticias_jota = busca_jota(jota_dados, jota_seletores)
noticias_stf = busca_supremo(stf_dados, stf_seletores)

lista_noticias = [noticias_sacha, noticias_valor, noticias_jota, noticias_stf]

outstring = control(lista_noticias)

print(outstring)

"""
ezgmail.send('mendes.lnr@gmail.com','Clipping Tributário',outstring)
ezgmail.send('barreto.isabelaa@gmail.com','Clipping Tributário',outstring)
"""