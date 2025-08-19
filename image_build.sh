ROOT="/home/hieunn/NGN"
cd $ROOT
mvn clean install -DskipTests

cd $ROOT/client
docker build -t client -f Dockerfile.client .

cd $ROOT/nginx/master
docker build -t nginx -f Dockerfile.nginx .

cd $ROOT/nginx/backup
docker build -t nginx_backup -f Dockerfile.nginx .

cd $ROOT/server
docker build -t server -f Dockerfile .

cd $ROOT/eureka_server
docker build -t eureka -f Dockerfile .

cd $ROOT/cloud_gateway
docker build -t gateway -f Dockerfile .

cd $ROOT/prometheus
docker build -t my_prometheus -f Dockerfile .

cd $ROOT/scaling_server
docker build -t scaling_server -f Dockerfile .
