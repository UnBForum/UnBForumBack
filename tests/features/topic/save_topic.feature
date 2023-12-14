Feature: Salvar Tópico
    Eu, como um usuário membro,
    Desejo salvar um tópico de discussão como favorito
    Para conseguir acessá-lo de forma mais rápida

    Scenario: Salvar Tópico com Sucesso
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/save/" é chamado
        Then O status da resposta é "204"
        And O tópico com id 1 é salvo pelo usuário

    Scenario: Salvar Tópico Já Salvo
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And O tópico com id 1 está salvo pelo usuário
        When O endpoint "POST /topics/1/save/" é chamado
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Tópico já salvo"

    Scenario: Remover Tópico Salvo
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        And O tópico com id 1 está salvo pelo usuário
        When O endpoint "POST /topics/1/unsave/" é chamado
        Then O status da resposta é "204"
        And O tópico com id 1 é removido dos tópicos salvos pelo usuário

    Scenario: Remover Tópico Não Salvo
        Given Um usuário autenticado (membro)
        And Um tópico com id 1
        When O endpoint "POST /topics/1/unsave/" é chamado
        Then O status da resposta é "400"
        And A resposta contém a mensagem de erro "Erro ao deixar de salvar tópico"
