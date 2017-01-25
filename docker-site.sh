echo "Pulling..."
git pull origin master
echo "Stoping Old Container..."
DID=$(docker ps | cut -d ' ' -f 1 | tail -n1)
docker kill $DID
echo "Building..."
docker build -t crawlr/landing .
echo "Running Docker container!"
docker run -p 80:8002 -d crawlr/landing
