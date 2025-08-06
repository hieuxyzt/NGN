ROOT="/home/hieunn/containernet/examples/project"
cd $ROOT/client_server
docker build -t client -f Dockerfile.client .
docker build -t server -f Dockerfile.server .

cd $ROOT/nginx
docker build -t nginx -f Dockerfile.nginx .
