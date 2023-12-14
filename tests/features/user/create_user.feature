Feature: Criar usuário
    Eu, como um usuário visitante,
    Quero criar uma conta na aplicação,
    Para que eu possa interagir com os tópicos.

    Eu, como UnBFórum,
    Desejo validar o email institucional do usuário cadastrado,
    Para garantir a autenticidade do email e do domínio

    Scenario Outline: Criação com sucesso
        Given Um usuário visitante
        And As tags <tags> já existem
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>.
        Then O status da resposta é "201"
        And A resposta contém o usuário criado com o <email>
        Examples:
            | email                | password    | tags                              |
            | johndoe@unb.br       | teste_senha | Aluno, Engenharia de Software     |
            | johndoe@aluno.unb.br | teste_senha | Engenharia Aeroespacial           |

    Scenario Outline: Criação com tag inexistente
        Given Um usuário visitante
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>.
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Tag Tag Inexistente não existe"
        Examples:
            | email          | password    | tags            |
            | johndoe@unb.br | teste_senha | Tag Inexistente |

    Scenario Outline: Criação com email não institucional
        Given Um usuário visitante
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>.
        Then O status da resposta é "422"
        Examples:
            | email             | password    | tags      |
            | johndoe@gmail.com | teste_senha |           |

    Scenario Outline: Criação com email já cadastrado
        Given Um usuário visitante
        And Já existe um usuário cadastrado com o email <email>
        When O endpoint "POST /users" é chamado com os dados <email>, <password>, <tags>.
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Email já cadastrado"
        Examples:
            | email          | password    | tags      |
            | johndoe@unb.br | teste_senha |           |
