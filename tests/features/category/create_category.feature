Feature: Criar Categoria
    Eu, como um usuário moderador,
    Desejo criar novas categorias
    Para aumentar as possibilidades de temas em um tópico de discussão

    Scenario Outline: Criação com sucesso
        Given Um usuário autenticado (moderador)
        When O endpoint "POST /categories" é chamado com o nome <name> e cor <color>
        Then O status da resposta é "201"
        And A resposta contém a categoria criada com <name> e <color>
        Examples:
            | name                   | color   |
            | TCC                    | #10B981 |
            | Estágio Supervisionado | #fff    |

    Scenario Outline: Criação com nome já existente
        Given Um usuário autenticado (moderador)
        And Uma categoria com o nome <name> já existe
        When O endpoint "POST /categories" é chamado com o nome <name> e cor <color>
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Erro ao criar a categoria"
        Examples:
            | name                   | color   |
            | Engenharia de Software | #000000 |


    Scenario Outline: Criação com cor inválida
        Given Um usuário autenticado (moderador)
        When O endpoint "POST /categories" é chamado com o nome <name> e cor <color>
        Then O status da resposta é "422"
        Examples:
            | name                   | color   |
            | TCC                    | #10B9   |
            | Estágio Supervisionado | 000000  |
            | Software               | #hahaha |

    Scenario Outline: Criação com permissão insuficiente
        Given Um usuário autenticado (membro)
        When O endpoint "POST /categories" é chamado com o nome <name> e cor <color>
        Then O status da resposta é "403"
        And A resposta contém a mensagem de erro "Você não tem permissão para realizar esta ação"
        Examples:
            | name                   | color   |
            | TCC                    | #10B981 |
