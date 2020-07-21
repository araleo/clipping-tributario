from Portais import Jota, Sacha, Valor


def load_tributario():
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

    return [sacha, valor, jota]


def main():
    pass


if __name__ == "__main__":
    main()
