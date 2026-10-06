# 🚀 Pipeline de Dados com IoT, Docker e Streamlit

E aí! Seja bem-vindo ao repositório do meu trabalho prático para a disciplina de **Disruptive Architectures: IoT, Big Data e IA** da UniFECAF[cite: 5, 6]. 

A ideia aqui foi colocar a mão na massa e construir um pipeline de dados completo do zero: pegando leituras de temperatura de dispositivos IoT, jogando para dentro de um banco relacional rodando em um container Docker, criando views inteligentes para consulta e, no final, exibindo tudo em um dashboard interativo super legal[cite: 1, 6].

---

## 🛠️ Tecnologias que usei
Para tirar esse projeto do papel, escolhi usar ferramentas modernas e muito comuns no mercado:
* **Python**: Para automatizar a leitura dos dados e rodar a aplicação[cite: 2, 6].
* **Docker**: Para subir o nosso banco de PostgreSQL de forma isolada e rápida[cite: 2, 6].
* **PostgreSQL**: O banco de dados onde os dados dos sensores ficam salvos e onde estruturei as views[cite: 2, 3, 6].
* **Pandas & SQLAlchemy**: Para fazer a ponte entre os arquivos, o Python e o banco[cite: 2, 3].
* **Streamlit & Plotly**: Para dar vida ao dashboard web e gerar gráficos dinâmicos[cite: 3, 4, 6].
* **GitHub Codespaces**: Meu ambiente de desenvolvimento em nuvem para rodar tudo sem dor de cabeça.

---

## 📂 Como o projeto está organizado
Deixei os arquivos bem divididos para ficar fácil de navegar:
```text
/
├── data/                  # Onde fica o arquivo CSV bruto (baixado lá do Kaggle)[cite: 2, 7]
├── src/                   # Scripts e códigos do projeto[cite: 7]
├── app.py                 # O arquivo principal que roda o Streamlit
└── README.md              # Este guia com a explicação de tudo