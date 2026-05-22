import requests
import time
import win32print
import webbrowser
import threading

SERVIDOR = "http://192.168.0.129:8000"
NOME_TELA = "tela2"


def abrir_teclado_virtual():
    try:
        webbrowser.open(f"{SERVIDOR}/")
        print("Tela aberta no navegador.")
    except Exception as e:
        print("Erro ao abrir navegador:", e)


def imprimir_raw(nome_impressora, texto):
    dados = texto.encode("latin-1", errors="ignore")

    hPrinter = win32print.OpenPrinter(nome_impressora)

    try:
        win32print.StartDocPrinter(
            hPrinter,
            1,
            ("Ticket Sorteio", None, "RAW")
        )

        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, dados)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)

    finally:
        win32print.ClosePrinter(hPrinter)


threading.Thread(
    target=abrir_teclado_virtual,
    daemon=True
).start()


while True:
    try:
        print("Verificando:", NOME_TELA)

        resposta = requests.get(
            f"{SERVIDOR}/api-impressao/{NOME_TELA}/",
            timeout=5
        )

        dados = resposta.json()

        print(dados)

        if dados.get("imprimir"):
            texto = dados.get("texto", "")

            impressora = win32print.GetDefaultPrinter()
            print("Impressora padrão:", impressora)

            imprimir_raw(impressora, texto)

            print("IMPRESSÃO ENVIADA!")

        time.sleep(1)

    except Exception as e:
        print("ERRO:", e)
        time.sleep(1)