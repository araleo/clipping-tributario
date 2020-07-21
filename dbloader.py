import os
from datetime import datetime

import psycopg2

ERROS = []


def generate_error_log(filepath):
    with open(filepath, "a") as f:
        for erro in ERROS:
            f.write(erro)
            f.write("\n")


def fill_search_vector(cur, conn):
    cur.execute("""
        "UPDATE noticias_noticia 
        SET search_vector = setweight(to_tsvector(coalesce(titulo, '')), 'A') 
        || setweight(to_tsvector(coalesce(descricao, '')), 'B')"
        """
    )
    try:
        conn.commit()
    except psycopg2.Error as e:
        ERROS.append(e)


def testa_sem_repetidos(cur, args):
    titulo, descricao, link = args
    cur.execute("""
        SELECT * FROM noticias_noticia
        WHERE titulo=%s AND descricao=%s AND link=%s""",
        (titulo, descricao, link)
    )
    return len(cur.fetchall()) == 0


def load_entries(filepath, cur, tipo):
    with open(filepath, "r") as f:
        for line in f.readlines():
            try:
                portal, data, titulo, descricao, link = line.split(";")
            except ValueError as e:
                ERROS.append(e)
            else:
                data = datetime.strptime(data, "%d/%m/%Y")
                if testa_sem_repetidos(cur, (titulo, descricao, link)):
                    try:
                        cur.execute("""
                            INSERT INTO noticias_noticia (portal, data, titulo, descricao, link, tipo)
                            VALUES (%s, %s, %s, %s, %s, %s);""",
                            (portal, data, titulo, descricao, link, tipo)
                        )
                    except psycopg2.Error as e:
                        ERROS.append((e, titulo))


def clear_temp_file(temppath, cachepath):
    with open(temppath) as f:
        conteudo = f.read()
        with open(cachepath, "a") as _f:
            _f.write(conteudo)
    os.remove(temppath)


def db_loader(tipo, filepath, cachepath, errorpath):

    # os.environ["DBCRED"] deve ser uma string no formato
    # "dbname= user= password= host= port="
    conn = psycopg2.connect(os.environ["DBCRED"])
    cur = conn.cursor()

    load_entries(filepath, cur, tipo)

    try:
        conn.commit()
    except psycopg2.Error as e:
        ERROS.append(e)
    else:
        clear_temp_file(filepath, cachepath)
        fill_search_vector(cur, conn)

    conn.close()
    generate_error_log(errorpath)


def main():
    pass


if __name__ == "__main__":
    main()