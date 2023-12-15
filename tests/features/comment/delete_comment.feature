Feature: Excluir Comentário
    Eu, como um usuário membro,
    Desejo excluir meu comentário
    Para removê-lo do fórum

    Eu, como um usuário moderador,
    Desejo excluir um comentário
    Para remover comentários indevidos do fórum

    Scenario: Deleção com sucesso
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1 pelo usuário autenticado
        When O endpoint "DELETE /topics/1/comments/1/" é chamado
        Then O status da resposta é "204"
        And O comentário com id 1 é apagado

    Scenario: Deleção com sucesso usuário moderador
        Given Um usuário autenticado (moderador)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1 por outro usuário
        When O endpoint "DELETE /topics/1/comments/1/" é chamado
        Then O status da resposta é "204"
        And O comentário com id 1 é apagado

    Scenario: Deleção com permissão insuficiente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1 por outro usuário
        When O endpoint "DELETE /topics/1/comments/1/" é chamado
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"
