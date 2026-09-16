# 🤖 Confirmador de Inscrições EGOV

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-green?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Google Sheets API](https://img.shields.io/badge/Google_Sheets-OAuth_2.0-orange?style=flat-square&logo=google-sheets&logoColor=white)](https://developers.google.com/sheets/api)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-purple?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)

Ferramenta de automação desktop desenvolvida para otimizar a gestão de turmas, verificação de pendências de pré-inscrições/ouvintes e consolidação automática de dados no sistema institucional **EGOV** (Escola de Governo da Secretaria de Economia), integrado diretamente com planilhas oficiais via **Google Sheets API**.

---

## 🎯 Sobre o Projeto
O fluxo anterior exigia a verificação manual de dezenas de turmas e o preenchimento repetitivo de dados na planilha de controle do setor. Esta ferramenta foi criada para centralizar esse processo em uma interface gráfica amigável, reduzindo o tempo operacional da equipe, mitigando erros humanos e garantindo total independência de credenciais pessoais através de autenticação por OAuth 2.0 com uma conta de serviço/robô dedicada.

---

## 🚀 Principais Funcionalidades
* **Interface Gráfica (GUI):** Desenvolvida em CustomTkinter com seletores de data intuitivos e sistema de feedback visual.
* **Automação Web:** Utiliza o **Playwright** para navegação dinâmica, tratamento de turmas fantasmas e cliques simulados.
* **Integração em Nuvem via OAuth 2.0:** Comunicação segura com o **Google Sheets** (`gspread`) utilizando escopos restritos e isolados de contas pessoais.
* **Empacotamento Portátil (`.exe`):** Compilado via PyInstaller com suporte a diretórios portáteis para distribuição imediata em estações de trabalho corporativas sem dependência de ambiente Python instalado.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python
* **Automação Web:** Playwright for Python
* **Interface Gráfica:** CustomTkinter
* **Integração Cloud:** Google Sheets API (`gspread`) & Google Auth OAuth 2.0
* **Empacotamento:** PyInstaller

---

## ⚙️ Arquitetura e Estrutura do Projeto
```text
ConfirmadorEGOV/
│
├── app.py                 # Ponto de entrada da aplicação e interface gráfica (GUI)
├── automacao.py           # Núcleo da lógica de automação web (Playwright + Google Sheets)
├── credenciais.json       # Credenciais OAuth 2.0 do cliente Google Cloud (Robô)
├── token.json             # Token de sessão autenticado institucionalmente
└── README.md              # Documentação oficial do projeto
```

---

## 🚀 Como Executar o Projeto Localmente (Desenvolvimento)

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/automacao-egov.git](https://github.com/seu-usuario/automacao-egov.git)
   cd automacao-egov
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Credenciais:**
   * Insira os arquivos `credenciais.json` e `token.json` na raiz do projeto.

5. **Execute a aplicação:**
   ```bash
   python app.py
   ```

---

## 📦 Como Gerar o Executável (`.exe`) para Distribuição

Se você deseja compilar o projeto em um pacote executável portátil para uso em outras máquinas da equipe sem a necessidade de instalar o Python, siga os passos abaixo:

1. **Ative o ambiente virtual e instale o PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Gere a build em formato de diretório portável:**
   ```bash
   pyinstaller --noconsole --collect-all playwright --name "ConfirmadorEGOV" app.py
   ```

3. **Organize a Pasta Final:**
   * Vá até a pasta `dist/ConfirmadorEGOV/` gerada pelo PyInstaller.
   * Cole os arquivos **`credenciais.json`** e **`token.json`** autenticados da conta institucional do robô na mesma pasta onde está o arquivo `ConfirmadorEGOV.exe`.
   * Compacte a pasta inteira em `.zip` para facilitar a distribuição.

---

## 📖 Manual de Instruções para a Equipe

1. **Descompacte** a pasta recebida em qualquer local da estação de trabalho.
2. Certifique-se de que os arquivos de credenciais (`credenciais.json` e `token.json`) continuam na mesma pasta do executável.
3. Dê dois cliques no arquivo **`ConfirmadorEGOV.exe`**.
4. Selecione a data desejada na interface gráfica (Dia, Mês e Ano) e clique em **INICIAR SINCRONIZAÇÃO**.
5. **Atenção ao Login (⏰ 30 segundos):** O navegador abrirá automaticamente. O sistema possui uma pausa programada de segurança para que o operador realize o login no sistema EGOV caso necessário, antes que o robô inicie a varredura e a atualização automática na planilha oficial.

---

## 👨‍💻 Autor

Feito por **Maria Júlia Batista**.
