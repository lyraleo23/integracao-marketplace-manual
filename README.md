# 🛒 Integração Marketplace Manual com Tiny ERP

## 📋 Descrição

Este projeto em Python foi desenvolvido para integrar pedidos da plataforma **MANUAL** à plataforma **Tiny ERP**.  
Ele consiste em dois scripts principais:  

1. **main.py**: Responsável por gerar uma planilha com os dados dos pedidos integrados.  
2. **download_links.py**: Utiliza a planilha gerada pelo `main.py` para baixar os anexos dos pedidos (como recibos e receitas).  

O objetivo é facilitar a comunicação e a gestão dos pedidos entre as duas plataformas.


## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.  
- **Bibliotecas Principais**:
  - `pandas`: Para manipulação e criação da planilha.  
  - `requests`: Para comunicação com as APIs das plataformas.  
  - `os`: Para gerenciar downloads e salvar arquivos localmente.  


## 🚀 Como Utilizar o Projeto

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/lyraleo23/integracao-marketplace-manual.git
cd integracao-marketplace-manual
```

### Passo 2: Configurar as Dependências
Certifique-se de ter o Python instalado. Instale as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Passo 3: Executar o Script `main.py`
Este script gera uma planilha com os pedidos integrados:
```bash
python main.py
```
A planilha gerada será salva no diretório do projeto.

### Passo 4: Executar o Script `download_links.py`
Após gerar a planilha, use-a para baixar os anexos dos pedidos:
```bash
python download_links.py
```
Os arquivos baixados (como recibos e receitas) serão salvos em uma pasta local.


## 📄 Estrutura do Projeto

📂 integracao-marketplace-manual  
 ├── main.py              # Script principal para integrar pedidos e gerar a planilha  
 ├── download_links.py    # Script para baixar os anexos dos pedidos  
 ├── requirements.txt     # Arquivo com as dependências do projeto  
 ├── README.md            # Documentação do projeto  
 └── output/              # Pasta onde a planilha e os downloads serão salvos  


## 🧠 Conceitos Aplicados

- **Integração de APIs**: Comunicação com as APIs da plataforma MANUAL e Tiny ERP.  
- **Manipulação de Dados**: Uso do `pandas` para gerar e manipular planilhas.  
- **Automação de Downloads**: Uso de links para baixar anexos de forma automática.  


## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.


## 📞 Contato

- **Autor**: Leonardo Lyra  
- **GitHub**: [lyraleo23](https://github.com/lyraleo23)  
- **LinkedIn**: [Leonardo Lyra](https://www.linkedin.com/in/leonardo-lyra/)  

