import json
import os
import requests

INPUT_DIR = "payloads_entrada"
OUTPUT_DIR = "payloads_saida"


def run_txt_tests():
  os.makedirs(INPUT_DIR, exist_ok=True)
  os.makedirs(OUTPUT_DIR, exist_ok=True)

  headers = {"Content-Type": "application/json"}

  arquivos = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
  if not arquivos:
    print(f"Nenhum arquivo .txt encontrado em '{INPUT_DIR}'.")
    return

  print(f"Processando {len(arquivos)} arquivos de teste...")

  for arquivo in arquivos:
    caminho_entrada = os.path.join(INPUT_DIR, arquivo)
    with open(caminho_entrada, "r", encoding="utf-8") as f:
      conteudo_bruto = f.read().strip()

    conteudo_bruto = conteudo_bruto.replace("\r\n", "\n")

    partes_arquivo = conteudo_bruto.split("\n", 1)
    if len(partes_arquivo) < 2:
      print(f"[AVISO] {arquivo} não está no formato 'METODO URL'. Ignorando.")
      continue

    cabecalho_requisicao = partes_arquivo[0].strip()
    payload_conteudo = partes_arquivo[1].strip()

    try:
      partes_cabecalho = cabecalho_requisicao.split(" ", 1)
      metodo = partes_cabecalho[0].upper()
      url = partes_cabecalho[1].strip()
    except IndexError:
      print(f"[AVISO] Cabeçalho inválido em {arquivo}. Ignorando.")
      continue

    try:
      payload_json = json.loads(payload_conteudo) if payload_conteudo else None
    except json.JSONDecodeError:
      print(f"[AVISO] O payload em {arquivo} não é um JSON válido. Ignorando.")
      continue

    print(f"Testando -> [{metodo}] {url} (Origem: {arquivo})")

    try:
      if metodo == "GET":
        resp = requests.get(url, headers=headers, timeout=5)
      elif metodo == "POST":
        resp = requests.post(url, json=payload_json, headers=headers, timeout=5)
      elif metodo == "PUT":
        resp = requests.put(url, json=payload_json, headers=headers, timeout=5)
      elif metodo == "DELETE":
        resp = requests.delete(url, headers=headers, timeout=5)
      else:
        print(f"[AVISO] Método HTTP '{metodo}' não suportado.")
        continue

      resultado_texto = f"""=== RESULTADO DO TESTE DE CONTRATO ===
Arquivo de Origem: {arquivo}
Método HTTP: {metodo}
URL Testada: {url}
Status HTTP Retornado: {resp.status_code}

=== PAYLOAD ENVIADO ===
{payload_conteudo}

=== RESPOSTA DA API ===
{resp.text}
"""
    except requests.RequestException as err:
      resultado_texto = f"""=== ERRO NA REQUISIÇÃO ===
Arquivo de Origem: {arquivo}
URL Testada: {url}
Erro de Conexão: {str(err)}
"""

    caminho_saida = os.path.join(
        OUTPUT_DIR, arquivo.replace(".txt", "_resposta.txt")
    )
    with open(caminho_saida, "w", encoding="utf-8") as f_out:
      f_out.write(resultado_texto)

  print(f"Testes finalizados! Verifique a pasta '{OUTPUT_DIR}'.")


if __name__ == "__main__":
  run_txt_tests()