# client-server
Aplicação cliente-servidor capaz de, na camada de aplicação, fornecer uma comunicação confiável para os dados trocados entre os sistemas finais considerando um canal com perdas de dados e erros.


# Instalação
- Criar uma venv dentro do projeto com o nome .venv
- Ativar a venv

- Instalar as dependências do projeto
`pip install -r requirements.txt`

- Executar o servidor
`python server/server.py`

- Executar o cliente
`python client/client.py`


# Dinâmica do projeto
- O cliente envia uma mensagem para o servidor
- O servidor apenas responde quem enviou a mensagem
- Padrão de comunicação (protocolo):
  - Linguagem de comunicação: JSON
  - Tamanho máximo da mensagem de entrada: 1024 bytes
  - Atributos de entrada:
    - message:
      - text: string
      - error: boolean
      - lost: boolean
      - npackages: int
      - multpackages: boolean
    - passkey: string

  - Atributos de saída:
    - message:
      - id: string
      - text: string
      - error: boolean
      - lost: boolean
      - npackages: int
      - multpackages: boolean
    - passkey: string

- Opções:
  - Teste de conexão (instrução)
  - Enviar mensagem padrão
  - Enviar mensagem padrão com perdas
  - Enviar mensagem padrão com erros
  - Enviar mensagem por pacotes
  - Enviar mensagem por pacotes com perdas
  - Enviar mensagem por pacotes com erros
  - Enviar mensagem duplicada
  - Enviar mensagem com tamanho inválido
  - Enviar mensagem com tamanho inválido por pacotes
  - Sair