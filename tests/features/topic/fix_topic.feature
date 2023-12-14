Feature: Fixar Tópico
    Eu, como um usuário moderador,
    Desejo fixar um tópico de discussão
    Para que ele fique posicionado em destaque na página principal

    Scenario: Fixar tópico
        Given Um usuário autenticado (moderador)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/fix/" é chamado
        Then O status da resposta é "204"
        And O tópico com id 1 é fixado

    Scenario: Fixar tópico com permissão insuficiente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/fix/" é chamado
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"

    Scenario: Desafixar tópico
        Given Um usuário autenticado (moderador)
        And Um tópico com id 1
        And O tópico com id 1 está fixado
        When O endpoint "POST /topics/1/fix/" é chamado
        Then O status da resposta é "204"
        And O tópico com id 1 é desafixado
