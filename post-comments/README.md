# Instruções

Este projeto implementa parte da API de uma plataforma de blogging. As
seguintes rotas foram implementadas:

- `GET /posts` - retorna uma lista contendo todos os posts da base de dados.
- `GET /posts/<post_id>` - retorna o post referenciado por `post_id`, caso exista.
- `GET /posts/<post_id>/comments` - retorna uma lista contendo os comentários do post referenciado por post_id.
- `GET /comments/<comment_id>` - retorna o comentário referenciado por `comment_id`, caso exista.

Na demonstração desta API para os stakeholders, dois requisitos adicionais foram
levantados:

1. O formato de retorno da rota `GET /posts/<post_id>/comments` não é compatível
   com o esperado pelo front-end da aplicação. Em vez de uma lista com todos os
   comentários de um post, é necessário que estes tragam suas respostas
   aninhadas. Por exemplo, se a rota antes retornava a seguinte lista
   (com algumas propriedades omitidas):

   ``` json
   [
       {
           "id": 1,
           "parent": null,
           "content": "Este comentário não responde a ninguém, mas possui o comentário 3 como resposta."
       },
       {
           "id": 2,
           "parent": null,
           "content": "Este comentário também não responde a ninguém e não possui respostas."
       },
       {
           "id": 3,
           "parent": {
               "id": 1
           },
           "content": "Este comentário é uma resposta ao comentário 1 e possui o comentário 4 como resposta."
       },
       {
           "id": 4,
           "parent": {
               "id": 3
           },
           "content": "Este comentário é uma resposta ao comentário 3 e não possui respostas."
       }
   ]
   ```

   , a resposta agora deverá ser:
   ``` json
   [
       {
           "id": 1,
           "content": "Este comentário não responde a ninguém, mas possui o comentário 3 como resposta.",
           "children": [
               {
                   "id": 3,
                   "content": "Este comentário é uma resposta ao comentário 1 e possui o comentário 4 como resposta.",
                   "children": [
                       {
                           "id": 4,
                           "content": "Este comentário é uma resposta ao comentário 3 e não possui respostas.",
                           "children": []
                       }
                   ]
               }
           ]
       },
       {
           "id": 2,
           "content": "Este comentário também não responde a ninguém e não possui respostas.",
           "children": []
       }
   ]
   ```

   . O primeiro nível da lista deve conter apenas os comentários "raiz", que não
   respondem a um outro comentário. Cada comentário, independente do quão aninhado, deverá ter as seguintes
   propriedades:

   - `id` - id do comentário.
   - `timestamp` - o momento em que o comentário foi criado (propriedade do
     modelo: `created_at`)
   - `author` - um dicionário contendo o `id` e o `username` do autor do
     comentário.
   - `post` - um dicionário contendo o `id` e o `title` do post em que o
     comentário foi criado.
   - `content` - string contendo o texto do comentário.
   - `children` - lista das respostas a esse comentário, aninhadas.

    **Observação**: O retorno da função `get_post_comments` deve ser utilizado, inalterado, para montar a árvore.
    Não devem ser feitas outras consultas ao banco de dados.

2. A API deve oferecer uma forma de consultar as _threads_ em que um usuário
   comentou. Para isso, deve ser implementada uma nova rota
   `GET /users/<user_id>/comments`. Esta deve retornar uma lista de objetos
   contendo as porções das árvores de comentários de cada post em que o usuário
   participou, da seguinte maneira:

   - O comentário do usuário sempre deve fazer parte da árvore trazida.
   - Se o usuário respondeu a algum comentário, **todos os comentários "pais"
     devem ser trazidos**, até o comentário "raiz" da árvore.
   - Se alguém respondeu ao comentário do usuário, **toda a sub-árvore contendo as
     repostas deve ser trazida**.

   O diagrama abaixo ilustra, para uma determinada árvore de comentários, quais
   devem ou não ser trazidos:

   ![Exemplo da porção relacionada a um usuário de uma árvore de comentários.](./diagrama.png)

   O formato dos objetos trazidos deve ser o seguinte:

   - `post_id`: id do post
   - `timestamp`: data de publicação do post.
   - `author`: um dicionário contendo o `id` e o `username` do autor do post.
   - `comments`: uma lista de árvores de comentários, no modelo do item (1).
     Devem ser retornadas somente árvores nais quais o usuário referenciado foi
     o autor de um ou mais comentários. Os comentários devem ter as mesmas
     propriedades que as descritas no item (1).

    Um exemplo de resposta correta a `GET /users/23/comments`:

    ``` jsonc
    [
        {
            "post_id": 7,
            "author": {
                "id": 37,
                "username": "James Johnson"
            },
            "timestamp": "Sun, 13 Jun 2021 00:56:03 GMT",
            "comments": [
                {
                    "id": 54,
                    "author": {
                        "id": 65,
                        "username": "John Boswell"
                    },
                    "children": [{
                        "id": 57,
                        "author": {
                            "id": 23, // comentário do usuário solicitado
                            "username": "William M. Buchanan"
                        },
                        "children": []
                    }]
                },
                {
                    "id": 87,
                    "author": {
                        "id": 23, // comentário do usuário solicitado
                        "username": "William M. Buchanan"
                    },
                    "children": [
                        {
                            "id": 94,
                            "author": {
                                "id": 8,
                                "username": "Mary Boaz"
                            },
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
    ```
Note que a funcionalidade implementada em (1) não deve ser afetada de nenhuma maneira.

Sua tarefa é implementar estas novas funcionalidades. As funções que implementam a
construção das árvores devem ser cobertas por testes.

## Estrutura do projeto

A estrutura do projeto divide as funcionalidades da seguinte maneira:

* Funcionalidades relacionadas à **persistência** das várias entidades no banco
  de dados (posts, usuários, etc) se encontram nos **repositórios**
  (`/respositories/*.py`).

* As **definições de rotas**, bem como o tratamento de exceções, se encontram no
  `__init__.py` dos módulos dos controladores (`/controllers/**/__init__.py`).

* Funcionalidades que dizem respeito à **forma de apresentação** dos dados
  (conversões para dicionário, etc) se encontram nos submódulos de utilidades
  dos controladores (`/controllers/**/utils.py`).

Esta estrutura deve ser preservada. Por exemplo, suponhamos que, na
implementação das tarefas, você julgue necessária uma nova consulta ao banco que
retorne os comentários de todos os posts nos quais um usuário fez um ou mais
comentários. Esta função diz respeito à **persistência** dos **comentários** e
deverá, portanto, estar no módulo `app.repositories.comments`. Da mesma forma,
uma função que constrói uma árvore a partir da lista de todos os comentários de
um post trata da **apresentação** dos dados, e deverá estar no submódulo de
utilidades apropriado (neste caso, `app.controllers.posts.utils`).

### Testes

As suítes de teste devem se encontrar em módulos dentro da pasta `/tests`. A
estrutura de pastas é similar à descrita anteriormente para o restante da
aplicação.

Para simplificar a execução dos testes, foi criado o script `run_tests.sh`,
dentro da pasta principal do projeto (a mesma que contém este arquivo). É
necessário que o container do [servidor de
desenvolvimento](#instruções-de-execução) esteja em execução.

## Instruções de execução

O projeto possui um ambiente de desenvolvimento implementado em um container
[Docker](https://www.docker.com). Para executar o servidor de desenvolvimento, é
necessário ter o executável do docker instalado e acessível pelo $PATH da sua
shell. Também é importante que seu usuário tenha sido adicionado ao grupo
`docker`.

Satisfeitos estes requisitos, o servidor pode ser executado a partir da pasta
principal do projeto (isto é, a que contém este README) através do script
`run_server.sh`. Este constrói o container caso necessário e expõe o servidor na
porta 5000<sup id="ref1">[1](#footnote-1)</sup>.

## Critérios de avaliação

A solução recebida será avaliada nas seguintes dimensões, em ordem de importância:

* Correção da implementação.
* Clareza e concisão do código, sem repetições desnecessárias.
* Desempenho, especialmente no número de consultas ao banco de dados.
* Código limpo e legível, seguindo o estilo dos arquivos pré-existentes.
* Testes úteis e descritivos do comportamento esperado.

## Instruções de entrega

Após ter realizado as tarefas, exclua a pasta '.poetry_envs'<sup id="ref2">[2](#footnote-2)</sup>
(na raiz do projeto) e compacte a pasta do projeto em um arquivo (formato
.tar ou .zip). Este arquivo deve ser submetido para análise através deste
[link](https://www.dropbox.com/request/qEiESP6aRmMm6M69uRUA), nomeado da
seguinte forma: `<seu_nome_completo>_backend_test.zip`.

---

<b id="footnote-1">[1]</b>: Caso deseje, é possível alterar a porta por meio da variável
`LOCAL_PORT`. Por exemplo, `LOCAL_PORT=5001 ./run_server.sh` expuserá o servidor
na porta 5001 do seu computador. Observe, no entanto, que o Flask continuará
exibindo a mensagem 'Running on http://0.0.0.0:5000/', indicando a porta interna
do container. [↩](#ref1)

<b id="footnote-2">[2]</b>: A pasta `.poetry_envs` é criada dentro do container
do Docker. Dessa forma, a depender de suas configurações de sistema, pode ser
necessário o uso de `sudo` para removê-la. [↩](#ref2)
