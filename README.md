


## 🇺🇸 English Documentation

### Features
* **Zero Hardcoded Configs:** URLs, endpoints, and HTTP methods are defined directly in the text files.
* **Batch Processing:** Scans the input folder and runs multiple requests sequentially.
* **Smart Error Handling (Self-Healing):** Failed requests or invalid syntax are automatically routed to an error folder. If fixed and re-run, old error files are cleaned up and replaced with successful outputs.
* **Containerized Execution:** Fully encapsulated using Docker.

### Project Structure
```text
.
├── payloads_entrada/     # Place your test .txt files here
├── payloads_saida/       # Successful test responses are saved here
├── payloads_erros/       # Validation or connection errors are saved here
├── Dockerfile
├── requirements.txt
└── runner.py
```

### Test Payload Format
Create a `.txt` file inside `payloads_entrada/` using the following formats:

* **For POST / PUT / DELETE (with JSON payload):**
  ```text
  POST https://reqres.in/api/users

  {
      "name": "Sarah",
      "job": "Software Engineer"
  }
  ```

* **For GET requests (no body required):**
  ```text
  GET https://reqres.in/api/users?page=2
  ```

### How to Run (Docker)
1. Build the Docker image:
   ```bash
   docker build -t api-txt-tester .
   ```
2. Run the container mapping your local directories:
   ```bash
   docker run --rm -v $(pwd)/payloads_entrada:/app/payloads_entrada -v $(pwd)/payloads_saida:/app/payloads_saida -v $(pwd)/payloads_erros:/app/payloads_erros api-txt-tester
   ```

---

## 🇧🇷 Documentação em Português

### Funcionalidades
* **Totalmente Desacoplado:** URLs, rotas e métodos HTTP são definidos exclusivamente nos arquivos de texto.
* **Processamento em Lote:** Varre a pasta de entrada e executa múltiplos cenários em sequência.
* **Tratamento de Erros Inteligente (Auto-cura):** Falhas de conexão ou sintaxe vão para a pasta de erros. Se você corrigir o arquivo e rodar de novo, o erro antigo é apagado e o sucesso é gerado na pasta correta.
* **Execução em Container:** Isola o ambiente utilizando Docker.

### Estrutura do Projeto
```text
.
├── payloads_entrada/     # Coloque seus arquivos .txt de teste aqui
├── payloads_saida/       # Respostas de testes bem-sucedidos
├── payloads_erros/       # Registro detalhado de falhas ou erros de sintaxe
├── Dockerfile
├── requirements.txt
└── runner.py
```

### Formato do Payload de Teste
Crie arquivos `.txt` dentro da pasta `payloads_entrada/` seguindo estes padrões:

* **Para POST / PUT / DELETE (com corpo JSON):**
  ```text
  POST https://reqres.in/api/users

  {
      "name": "Sarah",
      "job": "Software Engineer"
  }
  ```

* **Para requisições GET (sem corpo):**
  ```text
  GET https://reqres.in/api/users?page=2
  ```

### Como Rodar (Via Docker)
1. Construa a imagem Docker:
   ```bash
   docker build -t api-txt-tester .
   ```
2. Execute o container mapeando os volumes locais:
   ```bash
   docker run --rm -v $(pwd)/payloads_entrada:/app/payloads_entrada -v $(pwd)/payloads_saida:/app/payloads_saida -v $(pwd)/payloads_erros:/app/payloads_erros api-txt-tester
   ```
