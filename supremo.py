from Portais import Supremo, ONTEM


def load_supremo():
    supremo = Supremo(
        "Supremo Tribunal Federal",
        [f"http://portal.stf.jus.br/listagem/listarNoticias.asp?dataDe={ONTEM.strftime('%d%m%Y')}&dataA=&ori=1"],
        {
            "titulo": "#noticias a",
            "descricao": ".noticia-resumo",
            "link": "#noticias a"
        }
    )

    return supremo


def main():
    pass


if __name__ == "__main__":
    main()
