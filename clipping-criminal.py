from Portais import *


supremo = Supremo(
    "Supremo Tribunal Federal",
    [f"http://portal.stf.jus.br/listagem/listarNoticias.asp?dataDe={ONTEM.strftime('%d%m%Y')}&dataA=&ori=1"],
    {
        "titulo": "#noticias a",
        "descricao": ".noticia-resumo",
        "link": "#noticias a"
    }
)

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
        "descricao": ".j-recent__excerpt",
        "link": ".j-recent__item h2 a",
        "nova_descricao": ".jota-article__lead"
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


def main():
    supremo.busca()
    print(supremo.formata_texto())
    valor.busca()
    print(valor.formata_texto())
    jota.busca()
    print(jota.formata_texto())
    ibccrim.busca()
    print(ibccrim.formata_texto())


if __name__ == "__main__":
    main()
