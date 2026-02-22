---
title: EducaRAG
emoji: 🦉
colorFrom: blue
colorTo: red
sdk: streamlit
app_file: main.py
pinned: false
---

# EducaRAG 🦉
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/huggingface-%23FFD21E.svg?style=for-the-badge&logo=huggingface&logoColor=white)

## O que a aplicação faz
A aplicação é um chatbot que auxilia educadores a construirem PEIs (Plano Educacional Individualizado), por meio de prompts a IA pode gerar modelos, sugestões e até tirar dúvidas sobre essa ferramenta pedagógica, sempre com respostas baseadas em documentos oficiais do governo. 

## Com o que foi construído
A linguagem da aplicação é em Python, para o front-end foi usado a biblioteca Streamlit e o back-end foi aplicado a tecnologia **RAG** com o uso da biblioteca Llama Index.

### O que é o RAG
O RAG (Retrieval-Augmented Generation), no português Geração Aumentada por Recuperação, é o processo de otimizar a saída de um Grande Modelo de Linguagem (LLM), fornecendo uma ou mais base de conhecimento confiável. Dessa forma além do grande volume de dados que a LLM é treinada, agora é possível usar dados específicos que desejar, como PDFs, planilhas, slides e etc. Assim aumentando a precisão e confiabilidade de suas respostas.

## Por que foi construído
- Com a aplicação do RAG, garantimos que os PEIs e as informações fornecidas são baseados em fontes de dados confiáveis, seguindo uma estrutura oficial usada em documentos educacionais brasileiros, conforme a legislação vigente (LDB, Constituição Federal, BNCC e Política Nacional de Educação Especial).
- Para ajudar os educadores a gerar PEIs com praticidade.

## Instruções de Instalação
Clonar repositório
```
git clone repositório
```
Dentro do diretório
```
pip install requirements.txt
```
## Instruções de uso
1. Abrir pasta .streamlit e criar arquivo .secrets; 

2. Setar as chaves: Qdrant Cloud para armazenamento dos dados com aplicação do RAG. Chave do Grok para uso da LLM;

3. Abrir terminal e iniciar aplicação:
```bash
streamlit run main.py
```

4. **Atenção!! Ao Rodar o programa na primeira vez irá demorar para carregar.**
