#!/bin/bash

# Fonction pour vérifier si RabbitMQ est prêt
wait_for_rabbitmq() {
  echo "Attente de la disponibilité de RabbitMQ..."
  while true; do
    echo "================================================================="
    echo "================================================================="
    docker logs rabbitmq 2>&1 | grep -q "Server startup complete; 5 plugins started."
    if [ $? -eq 0 ]; then
      echo "RabbitMQ est prêt !"
      break
    fi
    docker logs rabbitmq
    sleep 5
  done
}

# Étape 1 : Lancer RabbitMQ
echo "Démarrage de RabbitMQ..."
docker run -d --name rabbitmq --rm -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Étape 2 : Attendre que RabbitMQ soit prêt
wait_for_rabbitmq

# Étape 3 : Lancer le reste des services
echo "Démarrage des autres services..."

# SenderCapteurLumiere
docker run -d --name sender-capteur-lumiere --rm --net host sender-capteur-lumiere

# ReceiveVoletElectrique
docker run -d --name receive-volet-electrique --rm --net host receive-volet-electrique

# Conteneur
docker run -d --name conteneur --rm --net host conteneur

# Étape 4 : Vérification des conteneurs
echo "Services en cours d'exécution :"
docker ps -a
