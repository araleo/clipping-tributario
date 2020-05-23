import locale
import re
from datetime import date, datetime, timedelta

import bs4
import requests

EXCEPTS = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.SSLError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.TooManyRedirects
)
ERROS = list()
ONTEM = date.today() - timedelta(days=1)

class Portal():

    def __init__(self, nome, links, seletores):
        self.nome = nome
        self.links = links
        self.seletores = seletores
        self.noticias = {
            "titulo": list(),
            "descricao": list(),
            "link": list()
        }

    def formata_texto(self):
        outstring = ""
        if self.noticias["titulo"]:
            outstring = "".join((self.nome))
            n = self.noticias
            for t, d, l in zip(n["titulo"], n["descricao"], n["link"]):
                outstring = "".join((outstring,
                f"""

    {t}

        {d}

        {l}

                """
                ))
        return outstring

    def get_request(self, url):
        try:
            res = requests.get(url)
            res.raise_for_status
        except EXCEPTS as err:
            ERROS.append(str(err))
            return False
        else:
            return res

    def listas_noticias(self):
        titulos = list()
        descricoes = list()
        links = list()

        for link in self.links:
            res = self.get_request(link)
            if res:
                res.encoding = "unicode"
                soup = bs4.BeautifulSoup(res.text, "html.parser")
                titulos += soup.select(self.seletores["titulo"])
                descricoes += soup.select(self.seletores["descricao"])
                links += soup.select(self.seletores["link"])

        return (titulos, descricoes, links)


class Supremo(Portal):

    def busca(self):
        titulos, descricoes, links = self.listas_noticias()
        for titulo, descricao, link in zip(titulos, descricoes, links):
            self.noticias["titulo"].append(
                titulo.getText().strip()
            )
            self.noticias["link"].append(
                f"http://portal.stf.jus.br{link.get('href')}"
            )
            self.noticias["descricao"].append(
                descricao.getText().replace("\n", "")
            )


class Valor(Portal):

    def busca(self):
        titulos, descricoes, links = self.listas_noticias()
        for titulo, link in zip(titulos, links):
            titulo = titulo.getText().strip()
            link = link.get("href")

            if titulo not in self.noticias["titulo"]:
                self.noticias["titulo"].append(titulo)
                link = "".join(("https:", link))

                # busca na pagina de cada noticia a descricao completa
                res = self.get_request(link)
                if res:
                    soup = bs4.BeautifulSoup(res.text, "html.parser")
                    urls = re.findall(
                        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                        str(soup)
                    )
                    res = self.get_request(urls[0])
                    if res:
                        self.noticias["link"].append(urls[0])
                        soup = bs4.BeautifulSoup(res.text, "html.parser")
                        descricao = soup.select(self.seletores["nova_descricao"])
                        if descricao:
                            self.noticias["descricao"].append(
                                descricao[0].getText().replace("\n", "")
                            )
                        else:
                            self.noticias["descricao"].append("")


class Jota(Portal):

    def busca(self):
        titulos, descricoes, links = self.listas_noticias()

        for titulo, link in zip(titulos, links):
            titulo = titulo.getText().strip()
            link = link.get("href")

            if titulo not in self.noticias["titulo"]:
                self.noticias["titulo"].append(titulo)
                self.noticias["link"].append(link)

                res = self.get_request(link)
                if res:
                    soup = bs4.BeautifulSoup(res.text, "html.parser")
                    descricao = soup.select(self.seletores["nova_descricao"])
                    if descricao:
                        self.noticias["descricao"].append(
                            descricao[0].getText().replace("\n", "")
                        )

                if not res or not descricao:
                    self.noticias["descricao"].append("")


class Ibccrim(Portal):

    def busca(self):
        res = self.get_request(self.links[0])
        if res:
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            datas = soup.select(".badge-warning")
            datas = [x.getText() for x in datas]
            datas = [x for x in datas if self.verifica_data(x)]
            datas.append("19 de Maio de 2020")

            if datas:
                titulos, descricoes, links = self.listas_noticias()
                for titulo, descricao, link, data \
                in zip(titulos, descricoes, links, datas):
                    self.noticias["titulo"].append(titulo.getText().strip())
                    self.noticias["descricao"].append(
                        descricao.getText().replace("\n", "")
                    )
                    self.noticias["link"].append(
                        "".join(
                            ("https://www.ibccrim.org.br", link.get("href"))
                        )
                    )

    def verifica_data(self, data):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        dt = datetime.strptime(data, "%d de %B de %Y")
        return dt.date() == date.today() or dt.date() == ONTEM
