Feature: Editar Tópico
    Eu, como um usuário membro,
    Desejo editar meu tópico de discussão criado
    Para corrigir alguma informação incorreta

    Scenario Outline: Edição com sucesso
        Given Um usuário autenticado (membro)
        And Um tópico com id 1 criado pelo usuário autenticado
        And As categorias com ids <categories> já existem
        And Os arquivos com ids <files> já existem
        When O endpoint "PUT /topics/1/" é chamado com os dados <title>, <content>, <categories> e <files>.
        Then O status da resposta é "200"
        And O tópico é atualizado com os dados <title>, <content>, <categories> e <files>.
        Examples:
            | title            | content              | categories | files |
            | Título do tópico | Conteúdo do Tópico   | 1, 2, 3    |       |
            | Título do tópico | Tópico sem categoria |            | 1, 2  |

    Scenario Outline: Edição com permissão insuficiente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1 criado por outro usuário
        When O endpoint "PUT /topics/1/" é chamado com os dados <title>, <content>, <categories> e <files>.
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"
        Examples:
            | title            | content              | categories | files |
            | Título do tópico | Conteúdo do Tópico   | 1, 2, 3    | 1, 2  |
