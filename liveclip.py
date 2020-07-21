from clipping import clipping
from dbloader import db_loader


def carrega_db():
    filepaths = [
        "/home/leonardo/clippings-juridicos/caches/tempTributario.txt",
        "/home/leonardo/clippings-juridicos/caches/tempCriminal.txt",
        "/home/leonardo/clippings-juridicos/caches/tempSupremo.txt",
    ]
    cachepaths = [
        "/home/leonardo/clippings-juridicos/caches/cacheTributario.txt",
        "/home/leonardo/clippings-juridicos/caches/cacheCriminal.txt",
        "/home/leonardo/clippings-juridicos/caches/cacheSupremo.txt",
    ]
    tipos = ["tributario", "criminal", "stf"]
    errorpath = "/home/leonardo/clippings-juridicos/caches/errorlog.txt"

    for file, cache, tipo in zip(filepaths, cachepaths, tipos):
        db_loader(tipo, file, cache, errorpath)


def main():
    clipping()
    carrega_db()


if __name__ == "__main__":
    main()