Feature: Avaliar Tópico
    Eu, como um usuário membro,
    Desejo avaliar um tópico de discussão
    Para destacar sua relevância

    Scenario: Avaliar positivamente um tópico
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/upvote/" é chamado
        Then O status da resposta é "200"
        And O tópico com id 1 possui rating 1

    Scenario: Avaliar positivamente um tópico já avaliado positivamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And O tópico com id 1 já foi avaliado positivamente pelo usuário
        When O endpoint "POST /topics/1/upvote/" é chamado
        Then O status da resposta é "200"
        And O tópico com id 1 possui rating 0

    Scenario: Avaliar positivamente um tópico já avaliado negativamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And O tópico com id 1 já foi avaliado negativamente pelo usuário
        When O endpoint "POST /topics/1/upvote/" é chamado
        Then O status da resposta é "200"
        And O tópico com id 1 possui rating 1

    Scenario: Avaliar negativamente um tópico
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/downvote/" é chamado
        Then O status da resposta é "200"
        And O tópico com id 1 possui rating -1

    Scenario: Avaliar negativamente um tópico já avaliado positivamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And O tópico com id 1 já foi avaliado positivamente pelo usuário
        When O endpoint "POST /topics/1/downvote/" é chamado
        Then O status da resposta é "200"
        And O tópico com id 1 possui rating -1

    Scenario: Avaliar negativamente um tópico já avaliado negativamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And O tópico com id 1 já foi avaliado negativamente pelo usuário
        When O endpoint "POST /topics/1/downvote/" é chamado
        Then O status da resposta é "200"
        And O tópico com id 1 possui rating 0
