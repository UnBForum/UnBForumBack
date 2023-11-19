Feature: Criar usuário
    Eu, como um usuário visitante,
    Quero criar uma conta na aplicação,
    Para que eu possa interagir com os tópicos.

    Scenario Outline: Criação com sucesso
        Given Um usuário visitante
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>
        Then O status da resposta é "201"
        And A resposta contém o usuário criado com o <email>
        Examples:
            | email          | password    | tags                              |
            | johndoe@unb.br | teste_senha | Estudante, Engenharia de Software |

    Scenario Outline: Criação com tag inexistente
        Given Um usuário visitante
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Tag Tag Inexistente não existe"
        Examples:
            | email          | password    | tags            |
            | johndoe@unb.br | teste_senha | Tag Inexistente |

    Scenario Outline: Criação com email não institucional
        Given Um usuário visitante
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>
        Then O status da resposta é "422"
        Examples:
            | email             | password    | tags      |
            | johndoe@gmail.com | teste_senha | Estudante |

    Scenario Outline: Criação com email já cadastrado
        Given Um usuário visitante
        And Já existe um usuário cadastrado com o email <email>
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Email já cadastrado"
        Examples:
            | email          | password    | tags      |
            | johndoe@unb.br | teste_senha | Estudante |
