Feature: Editar Comentário
    Eu, como um usuário membro,
    Desejo editar meu comentário
    Para corrigir alguma informação incorreta

    Scenario Outline: Edição com sucesso
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1 pelo usuário autenticado
        When O endpoint "PUT /topics/1/comments/1/" é chamado com o conteúdo <content>
        Then O status da resposta é "200"
        And O comentário é atualizado com o conteúdo <content>
        Examples:
            | content                |
            | Conteúdo do comentário |

    Scenario Outline: Edição com permissão insuficiente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1 por outro usuário
        When O endpoint "PUT /topics/1/comments/1/" é chamado com o conteúdo <content>
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"
        Examples:
            | content                |
            | Conteúdo do comentário |
