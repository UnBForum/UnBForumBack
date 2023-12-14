Feature: Fixar Comentário
    Eu, como um usuário moderador,
    Desejo fixar um comentário
    Para que ele fique posicionado em destaque no tópico de discussão

    Scenario: Fixar comentário
        Given Um usuário autenticado (moderador)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        When O endpoint "POST /topics/1/comments/1/fix/" é chamado
        Then O status da resposta é "204"
        And O comentário com id 1 é fixado

    Scenario: Fixar comentário com permissão insuficiente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        When O endpoint "POST /topics/1/comments/1/fix/" é chamado
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"

    Scenario: Desafixar comentário
        Given Um usuário autenticado (moderador)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        And O comentário com id 1 está fixado ao tópico 1
        When O endpoint "POST /topics/1/comments/1/fix/" é chamado
        Then O status da resposta é "204"
        And O comentário com id 1 é desafixado
