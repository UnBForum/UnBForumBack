Feature: Criar Tópico
    Eu, como um usuário membro,
    Desejo criar um tópico de discussão
    Para que que eu possa compartilhar uma informação com a comunidade da FGA

    Scenario Outline: Criação com sucesso
        Given Um usuário autenticado (membro)
        And As categorias com ids <categories> já existem
        And Os arquivos com ids <files> já existem
        When O endpoint "POST /topics/" é chamado com os dados <title>, <content>, <categories> e <files>.
        Then O status da resposta é "201"
        And O tópico é criado com os dados <title>, <content>, <categories> e <files>.
        Examples:
            | title            | content              | categories | files |
            | Título do tópico | Conteúdo do Tópico   | 1, 2, 3    | 1     |
            | Título do tópico | Tópico sem categoria |            | 1, 2  |
            | Título do tópico | Tópico sem arquivo   | 1, 2, 3    |       |

    Scenario Outline: Criação com categoria inexistente
        Given Um usuário autenticado (membro)
        And Os arquivos com ids <files> já existem
        When O endpoint "POST /topics/" é chamado com os dados <title>, <content>, <categories> e <files>.
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Erro ao criar o tópico. Categoria não existe"
        Examples:
            | title            | content            | categories | files |
            | Título do tópico | Conteúdo do tópico | 1          | 1, 2  |
            | Título do tópico | Conteúdo do tópico | 1, 2, 3    | 1     |

    Scenario Outline: Criação com arquivo inexistente
        Given Um usuário autenticado (membro)
        And As categorias com ids <categories> já existem
        When O endpoint "POST /topics/" é chamado com os dados <title>, <content>, <categories> e <files>.
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Erro ao criar o tópico. Arquivo não existe"
        Examples:
            | title            | content            | categories | files |
            | Título do tópico | Conteúdo do tópico | 1          | 1, 2  |
            | Título do tópico | Conteúdo do tópico | 1, 2, 3    | 1     |
