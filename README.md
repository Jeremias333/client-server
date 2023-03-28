# client-server
Aplicação cliente-servidor capaz de, na camada de aplicação, fornecer uma comunicação confiável para os dados trocados entre os sistemas finais considerando um canal com perdas de dados e erros.


# Instalação
- Criar uma venv dentro do projeto com o nome .venv
- Ativar a venv

- Instalar as dependências do projeto
`pip install -r requirements.txt`

- Executar o servidor
`uvicorn server:app --reload`