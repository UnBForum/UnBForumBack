Feature: Login
    Eu, como um usuário já cadastrado,
    Quero fazer o login na minha conta,
    Para que eu possa iniciar uma sessão.

    Background:
        Given O usuário possui uma conta cadastrada com o email "johndoe@unb.br" e senha "teste_senha"

    Scenario: Login com sucesso
        When O endpoint "POST /auth/login" é chamado com o email "johndoe@unb.br" e senha "teste_senha"
        Then O status da resposta é "200"
        And O corpo da resposta contém o token de autenticação

    Scenario: Login com email inválido
        When O endpoint "POST /auth/login" é chamado com o email "invalid_email@unb.br" e senha "teste_senha"
        Then O status da resposta é "401"
        And A resposta contém a mensagem de erro "Email ou senha inválidos"

    Scenario: Login com senha inválida
        When O endpoint "POST /auth/login" é chamado com o email "joendoe@unb.br" e senha "senha_invalida"
        Then O status da resposta é "401"
        And A resposta contém a mensagem de erro "Email ou senha inválidos"
