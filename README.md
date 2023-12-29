![unbforum_logo](./assets/logo.png)

# UnBFórum

UnBFórum is an *online* discussion forum whose objective is to facilitate the search and sharing of academic information within the Faculdade do Gama (FGA) community.

To achieve this objective, the construction of the forum was guided by fundamental qualitative criteria for the creation of discussion forums. Furthermore, the application used Graph Theory to structure the relationship between topics and categories, through a bipartite graph.

## UnBForumBack

This repository consists of the development of the UnBFórum backend, using the Python programming language and the FastAPI framework.

Backend documentation is available at: https://unbforum-backend-4b05406a8bbf.herokuapp.com/docs or https://unbforum-backend-4b05406a8bbf.herokuapp.com/redoc

## How to execute the API

To run the project, you must have the following tools installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the project

1. Clone the repository
```bash
git clone https://github.com/UnBForum/UnBForumBack.git
```

2. Enter the project folder
```bash
cd UnBForumBack
```

3. Execute docker-compose
```bash
docker-compose -f docker-compose.yml up --build -d
```

4. Access the url http://localhost:8000/docs ou http://localhost:8000/redoc to see API documentation.

## How to execute the tests

To run the tests, run the following command, located inside the project folder:
```bash
sh scripts/run_tests.sh
```

## Authors

| ![Herick Portugues](https://github.com/herickport.png?size=96) | ![Lucas Boaventura](https://github.com/lboaventura25.png?size=96) |
|----------------------------------------------------------------|-------------------------------------------------------------------|
| Hérick Portugues                                               | Lucas Boaventura                                                  |

