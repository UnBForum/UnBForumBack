Feature: Excluir Tópico
    Eu, como um usuário membro,
    Desejo excluir meu tópico de discussão criado
    Para retirá-lo do fórum

    Eu, como um usuário moderador,
    Desejo excluir um tópico de discussão
    Para remover tópicos indevidos do fórum

    Scenario: Deleção com sucesso
        Given Um usuário autenticado (membro)
        And Um tópico com id 1 criado pelo usuário autenticado
        When O endpoint "DELETE /topics/1/" é chamado
        Then O status da resposta é "204"
        And O tópico com id 1 é apagado

    Scenario: Deleção com sucesso usuário moderador
        Given Um usuário autenticado (moderador)
        And Um tópico com id 1 criado por outro usuário
        When O endpoint "DELETE /topics/1/" é chamado
        Then O status da resposta é "204"
        And O tópico com id 1 é apagado

    Scenario: Deleção com permissão insuficiente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1 criado por outro usuário
        When O endpoint "DELETE /topics/1/" é chamado
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"
