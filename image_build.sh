ROOT="/home/hieunn/NGN"

cd $ROOT/client_server
docker build -t server -f Dockerfile.server .
docker build -t client -f Dockerfile.client .

cd $ROOT/nginx/master
docker build -t nginx -f Dockerfile.nginx .

cd $ROOT/nginx/backup
docker build -t nginx_backup -f Dockerfile.nginx .
