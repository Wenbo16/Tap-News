# Tap-News

### How do I get set up? ###

* Summary of set up for first Project: Collaborative Online Judge


 1. Install NodeJs:

    sudo apt-get update

    curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -

    sudo apt-get install -y nodejs

 2. Install Nodemon

    npm install -g nodemon

 3. Install git

    sudo apt-get install git

 4. Install Redis

    wget http://download.redis.io/releases/redis-3.2.6.tar.gz

    tar xzf redis-3.2.6.tar.gz

    cd redis-3.2.6

    make

    sudo make install

    cd utils

    sudo ./install_server.sh


 5. Install python 2.7: This is installed already in Ubuntu

 6. Install pip: 

    (sudo apt-get update)

    sudo apt install python-pip

    sudo pip install Flask

 7. Install Docker: 

    curl -fsSL https://get.docker.com/ | sh

 8. Setup docker permission: 

    sudo usermod -aG docker $(whoami)

   (you need to logout and login again after set permission)

   To start docker when the system boots: sudo systemctl enable docker

 9. Setup Elasticsearch:
    
    sudo docker pull elasticsearch
    
    mkdir /usr/share/elasticsearch/data/esdata
    
    docker run -d --name elasticsearch  -p 9200:9200 -p 9300:9300 -v /esdata:/usr/share/elasticsearch/data elasticsearch
    
    test elasticsearch container is running: curl -X GET http://localhost:9200
    
 10. Setup Logstash:
    
    sudo docker pull logstash
    
 11. Setup Kibana:
    
    sudo docker pull Kibana
    
  
 
