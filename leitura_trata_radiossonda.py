import re
import csv

LARGURA_COL = 7
colunas   = []
linhas      = []
sep_cont = 0

with open(r"C:\Users\gabriel.pereira\Downloads\sondagens_manaus_2026\2026010112.txt", "r") as f:
    for linha_original in f:
        linha = linha_original.rstrip("\n")

        if re.match(r'^\s*-{5,}\s*$', linha):
            sep_cont += 1
            continue

        if sep_cont == 1 and not colunas and all(re.match(r'^[A-Z][A-Z0-9]*$', t) for t in linha.split()):
            colunas = linha.split()
            continue

        if sep_cont < 2:
            continue

        if not linha.strip() or re.match(r'^ {10,}\S', linha):
            break

        linhas.append([linha[i*LARGURA_COL:(i+1)*LARGURA_COL].strip() or "NaN" for i in range(len(colunas))])

with open(r"C:\Users\gabriel.pereira\Downloads\sondagens_manaus_2026\2026010112.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(colunas)
    writer.writerows(linhas)

