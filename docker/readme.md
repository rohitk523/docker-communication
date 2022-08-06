cd {path to project}
git clone https://github.com/rohitk523/docker.git
cd docker
docker build -t myimage .
docker % docker run -d --name mycontainer -p 80:80 myimage
open docker desktop and run container in browser
