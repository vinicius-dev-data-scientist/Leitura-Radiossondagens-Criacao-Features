import os
import re
import csv
from datetime import datetime

PASTA_ENTRADA = r'C:\Users\gabriel.pereira\estagio_radiossondagens_calculovariaveis\sondagens_manaus_2026'
LARGURA_COL = 7


def extrair_data(filename):

    match = re.search(r'(\d{10})', filename)
    if not match:
        raise ValueError(f"Data não encontrada no nome do arquivo: {filename}")
    return datetime.strptime(match.group(1), "%Y%m%d%H")
    
    
def processar_txt(path_txt):

    colunas = []
    linhas = []
    sep_cont = 0
    
    data_arquivo = extrair_data(os.path.basename(path_txt))
    
    with open(path_txt, "r", encoding='utf-8') as f:
        for linha_original in f:
            linha = linha_original.rstrip("\n")

            if re.match(r'^\s*-{5,}\s*$', linha):
                sep_cont += 1
                continue

            if sep_cont == 1 and not colunas and all(re.match(r'^[A-Z][A-Z0-9]*$', t) for t in linha.split()):
                colunas = ["data"] + linha.split()
                continue

            if sep_cont < 2:
                continue

            if not linha.strip() or re.match(r'^ {10,}\S', linha):
                break

            dados = [
                linha[i*LARGURA_COL:(i+1)*LARGURA_COL].strip() or "NaN" for i in range(len(colunas))]
            linhas.append([data_arquivo] + dados)
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

