echo "Pulling..."
cd .. && git pull origin master
cd ~
echo "Stoping Old Container..."
DID=$(docker ps | cut -d ' ' -f 1 | tail -n1)
docker kill $DID
echo "Building..."
docker build -t crawlr/landing .
echo "Running Docker container!"
docker run -d -p 80:8080 -p 8000:8000 crawlr/landing
