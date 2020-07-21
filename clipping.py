from criminal import load_criminal
from tributario import load_tributario
from supremo import load_supremo


def clipping():
    portais_criminal = load_criminal()
    portais_tributario = load_tributario()
    supremo = load_supremo()

    for portal in portais_criminal:
        portal.generate_csv("tempCriminal.txt")

    for portal in portais_tributario:
        portal.generate_csv("tempTributario.txt")

    supremo.generate_csv("tempSupremo.txt")


def main():
    pass


if __name__ == "__main__":
    main()
