docker-compose -f docker-compose-test.yml build
docker-compose -f docker-compose-test.yml up -d
docker-compose -f docker-compose-test.yml exec -it app-test alembic upgrade head
docker-compose -f docker-compose-test.yml exec -it app-test pytest .