import os
import re
import csv

PASTA_ENTRADA = r'C:\Users\gabriel.pereira\estagio_radiossondagens_calculovariaveis\sondagens_manaus_2026'
LARGURA_COL = 7

def processar_txt(path_txt):

    colunas = []
    linhas = []
    sep_cont = 0
    
    with open(path_txt, "r", encoding='utf-8') as f:
        for linha_original in f:
            linha = linha_original.rstrip("\n")

            if re.match(r'^\s*-{5,}\s*$', linha):
                sep_cont += 1
                continue

            if sep_cont == 1 and not colunas and all(re.match(r'^[A-Z][A-Z0-9]*$', t) for t in linha.split()):
                colunas = linha.split()
                n_colunas = len(colunas)
                continue

            if sep_cont < 2:
                continue

            if not linha.strip() or re.match(r'^ {10,}\S', linha):
                break

            dados = [
                 linha[i*LARGURA_COL:(i+1)*LARGURA_COL].strip() or "NaN" for i in range(n_colunas)]
            linhas.append(dados)
    return colunas, linhas

for arquivo in os.listdir(PASTA_ENTRADA):
    if arquivo.lower().endswith(".txt"):
        caminho_txt = os.path.join(PASTA_ENTRADA, arquivo)
        caminho_csv = caminho_txt.replace(".txt", ".csv")
        
        colunas, linhas = processar_txt(caminho_txt)
        
        if not linhas:
            continue
   
        with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(colunas)
            writer.writerows(linhas)
        print(f"Conversão realizada: {arquivo}")
