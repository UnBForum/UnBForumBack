Feature: Criar Comentário
    Eu, como um usuário membro,
    Desejo adicionar um comentário a um tópico de discussão
    Para contribuir com o debate do assunto

    Scenario Outline: Criação com sucesso
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/comments/" é chamado com o conteúdo <content>
        Then O status da resposta é "201"
        And O comentário é criado com o conteúdo <content>
        Examples:
            | content                |
            | Conteúdo do comentário |
            | Comentando comentário  |
