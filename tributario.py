#! /usr/bin/python3

from Portais import Jota, Sacha, Supremo, Valor, ONTEM


sacha = Sacha(
    "Resenha Tributária Sacha Calmon Misabel Derzi",
    ["https://sachacalmon.com.br/categoria/resenha-tributaria/"],
    {
        "titulo": ".artigo-feed-archive h2",
        "descricao": ".artigo-feed-archive p",
        "link": ".artigo-feed-archive a",
        "data": ".data-artigo p"
    }
)

valor = Valor(
    "Valor Econômico",
    [
        "https://valor.globo.com/busca/?q=tributo&order=recent&page=1&from=now-1d",
        "https://valor.globo.com/busca/?q=tributos&order=recent&from=now-1d",
        "https://valor.globo.com/busca/?q=tributario&order=recent&from=now-1d&page=1"
    ],
    {
        "titulo": ".widget--info__title",
        "descricao": ".widget--info__description",
        "link": ".widget--info__text-container a",
        "nova_descricao": ".content-head__subtitle"
    }
)

jota = Jota(
    "Jota",
    [
        "https://www.jota.info/?s=tributo%20-tag&orderby=relevance&after=-24%20hours&before=",
        "https://www.jota.info/?s=tributario%20-tag&orderby=relevance&after=-24%20hours&before=",
        "https://www.jota.info/?s=fazenda%20-tag&orderby=relevance&after=-24%20hours&before=",
        "https://www.jota.info/?s=fiscal%20-tag&orderby=relevance&after=-24%20hours&before="
    ],
    {
        "titulo": ".j-recent__item h2",
        "descricao": ".jota-article__lead", # ".j-recent__excerpt"
        "link": ".j-recent__item h2 a"
    }
)

supremo = Supremo(
    "Supremo Tribunal Federal",
    [f"http://portal.stf.jus.br/listagem/listarNoticias.asp?dataDe={ONTEM.strftime('%d%m%Y')}&dataA=&ori=1"],
    {
        "titulo": "#noticias a",
        "descricao": ".noticia-resumo",
        "link": "#noticias a"
    }
)


def main():
    portais = [sacha, valor, jota, supremo]
    for portal in portais:
        print(portal.formata_texto())
        portal.generate_csv("cacheTributario.txt")


if __name__ == "__main__":
    main()
