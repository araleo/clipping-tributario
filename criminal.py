from Portais import Ibccrim, Jota, Valor


def load_criminal():
    valor = Valor(
        "Valor Econômico",
        [
            "https://valor.globo.com/busca/?q=crime&order=recent&from=now-1d",
            "https://valor.globo.com/busca/?q=criminal&order=recent&from=now-1d&page=1"
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
            "https://www.jota.info/?s=crime-tag&orderby=relevance&after=-24%20hours&before=",
            "https://www.jota.info/?s=criminal-tag&orderby=relevance&after=-24%20hours&before=",
            "https://www.jota.info/?s=penal-tag&orderby=relevance&after=-24%20hours&before=",
            "https://www.jota.info/?s=penais-tag&orderby=relevance&after=-24%20hours&before="
        ],
        {
            "titulo": ".j-recent__item h2",
            "descricao": ".jota-article__lead", # ".j-recent__excerpt"
            "link": ".j-recent__item h2 a"
        }
    )

    ibccrim = Ibccrim(
        "IBCCRIM",
        [
            "https://www.ibccrim.org.br/noticias"
        ],
        {
                "titulo": ".titulo-noticia",
                "descricao": ".descricao-noticia",
                "link": "#items-noticias a",
                "data": ".badge-warning"
        }
    )

    return [ibccrim, valor, jota]


def main():
    pass


if __name__ == "__main__":
    main()
