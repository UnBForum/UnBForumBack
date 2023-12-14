Feature: Avaliar Comentário
    Eu, como um usuário membro,
    Desejo avaliar um comentário
    Para destacar sua relevância

    Scenario: Avaliar positivamente um comentário
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        When O endpoint "POST /topics/1/comments/1/upvote/" é chamado
        Then O status da resposta é "200"
        And O comentário com id 1 possui rating 1

    Scenario: Avaliar positivamente um comentário já avaliado positivamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        And O comentário com id 1 do tópico 1 já foi avaliado positivamente pelo usuário
        When O endpoint "POST /topics/1/comments/1/upvote/" é chamado
        Then O status da resposta é "200"
        And O comentário com id 1 possui rating 0

    Scenario: Avaliar positivamente um comentário já avaliado negativamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        And O comentário com id 1 do tópico 1 já foi avaliado negativamente pelo usuário
        When O endpoint "POST /topics/1/comments/1/upvote/" é chamado
        Then O status da resposta é "200"
        And O comentário com id 1 possui rating 1

    Scenario: Avaliar negativamente um comentário
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        When O endpoint "POST /topics/1/comments/1/downvote/" é chamado
        Then O status da resposta é "200"
        And O comentário com id 1 possui rating -1

    Scenario: Avaliar negativamente um comentário já avaliado positivamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        And O comentário com id 1 do tópico 1 já foi avaliado positivamente pelo usuário
        When O endpoint "POST /topics/1/comments/1/downvote/" é chamado
        Then O status da resposta é "200"
        And O comentário com id 1 possui rating -1

    Scenario: Avaliar negativamente um comentário já avaliado negativamente
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And Um comentário com id 1 adicionado ao tópico 1
        And O comentário com id 1 do tópico 1 já foi avaliado negativamente pelo usuário
        When O endpoint "POST /topics/1/comments/1/downvote/" é chamado
        Then O status da resposta é "200"
        And O comentário com id 1 possui rating 0
