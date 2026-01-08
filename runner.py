import json
import os
import requests

INPUT_DIR = "payloads_entrada"
SUCCESS_DIR = "payloads_saida"
ERROR_DIR = "payloads_erros"


def run_txt_tests():
  os.makedirs(INPUT_DIR, exist_ok=True)
  os.makedirs(SUCCESS_DIR, exist_ok=True)
  os.makedirs(ERROR_DIR, exist_ok=True)

  headers = {"Content-Type": "application/json"}

  arquivos = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
  if not arquivos:
    print(f"Nenhum arquivo .txt encontrado em '{INPUT_DIR}'.")
    return

  print(f"Processando {len(arquivos)} arquivos de teste...")

  for arquivo in arquivos:
    caminho_entrada = os.path.join(INPUT_DIR, arquivo)
    nome_saida = arquivo.replace(".txt", "_resposta.txt")

    caminho_sucesso = os.path.join(SUCCESS_DIR, nome_saida)
    caminho_erro = os.path.join(ERROR_DIR, nome_saida)

    with open(caminho_entrada, "r", encoding="utf-8") as f:
      conteudo_bruto = f.read().strip()

    if not conteudo_bruto:
      registrar_erro(
          caminho_erro,
          caminho_sucesso,
          arquivo,
          "O arquivo de entrada está vazio.",
      )
      continue

    conteudo_bruto = conteudo_bruto.replace("\r\n", "\n")

    partes_arquivo = conteudo_bruto.split("\n", 1)
    cabecalho_requisicao = partes_arquivo[0].strip()
    payload_conteudo = (
        partes_arquivo[1].strip() if len(partes_arquivo) > 1 else ""
    )

    try:
      partes_cabecalho = cabecalho_requisicao.split(" ", 1)
      metodo = partes_cabecalho[0].upper()
      url = partes_cabecalho[1].strip()
    except IndexError:
      registrar_erro(
          caminho_erro,
          caminho_sucesso,
          arquivo,
          (
              "Cabeçalho inválido. Certifique-se de usar o formato: 'METODO"
              " URL'."
          ),
      )
      continue

    payload_json = None
    if payload_conteudo:
      try:
        payload_json = json.loads(payload_conteudo)
      except json.JSONDecodeError as err:
        registrar_erro(
            caminho_erro,
            caminho_sucesso,
            arquivo,
            f"O payload enviado não é um JSON válido.\nDetalhe: {str(err)}",
        )
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
        registrar_erro(
            caminho_erro,
            caminho_sucesso,
            arquivo,
            f"Método HTTP '{metodo}' não suportado.",
        )
        continue

      resultado_texto = f"""=== RESULTADO DO TESTE DE CONTRATO ===
Arquivo de Origem: {arquivo}
Método HTTP: {metodo}
URL Testada: {url}
Status HTTP Retornado: {resp.status_code}

=== PAYLOAD ENVIADO ===
{payload_conteudo if payload_conteudo else "(Nenhum payload enviado)"}

=== RESPOSTA DA API ===
{resp.text}
"""
      with open(caminho_sucesso, "w", encoding="utf-8") as f_out:
        f_out.write(resultado_texto)

      if os.path.exists(caminho_erro):
        os.remove(caminho_erro)
        print(f"[LIMPEZA] {arquivo} corrigido! Removido da pasta de erros.")

    except requests.RequestException as err:
      resultado_erro = f"""=== ERRO NA REQUISIÇÃO ===
Arquivo de Origem: {arquivo}
URL Testada: {url}
Erro de Conexão: {str(err)}
"""
      with open(caminho_erro, "w", encoding="utf-8") as f_err:
        f_err.write(resultado_erro)

      if os.path.exists(caminho_sucesso):
        os.remove(caminho_sucesso)

      print(f"[FALHA] Erro registrado para {arquivo} na pasta 'payloads_erros'.")

  print(
      f"Testes finalizados! Sucessos em '{SUCCESS_DIR}' | Erros em"
      f" '{ERROR_DIR}'."
  )


def registrar_erro(caminho_erro, caminho_sucesso, arquivo, mensagem):
  print(f"[AVISO] {arquivo}: {mensagem}")
  conteudo = f"""=== ERRO DE VALIDAÇÃO DO CONTRATO ===
Arquivo de Origem: {arquivo}
Motivo: {mensagem}
"""
  with open(caminho_erro, "w", encoding="utf-8") as f:
    f.write(conteudo)

  if os.path.exists(caminho_sucesso):
    os.remove(caminho_sucesso)


if __name__ == "__main__":
  run_txt_tests()