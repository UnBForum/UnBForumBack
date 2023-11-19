Feature: Usuário autenticado
    Eu, como um usuário membro,
    Desejo editar informações da minha conta,
    Para que eu possa corrigir alguma informação incorreta.

    Eu, como um usuário membro,
    Desejo excluir minha conta,
    Para que eu possa me desvincular da aplicação.

    Scenario: Obter usuário autenticado
        Given Um usuário autenticado (membro)
        When O endpoint "GET /users/me" é chamado com o token de autenticação
        Then O status da resposta é "200"
        And A resposta contém os dados do usuário

    Scenario: Erro ao obter usuário autenticado
        Given Um usuário autenticado (membro)
        When O endpoint "GET /users/me" é chamado com o token de autenticação incorreto
        Then O status da resposta é "401"
        And A resposta contém a mensagem de erro "Token inválido"

    Scenario: Editar usuário autenticado
        Given Um usuário autenticado (membro)
        When O endpoint "PATCH /users/me" é chamado com o token de autenticação
        Then O status da resposta é "200"
        And A resposta contém os dados atualizados do usuário

    Scenario: Deletar usuário autenticado
        Given Um usuário autenticado (membro)
        When O endpoint "DELETE /users/me" é chamado com o token de autenticação
        Then O status da resposta é "204"
