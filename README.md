# 🧱 RL Brick-Breaker

 Ce projet utilise le **Reinforcement Learning** (RL) pour créer un jeu de casse-brique autonome. Il se base plus précisément sur [l'apprentissage par Q-valeurs](https://fr.wikipedia.org/wiki/Q-learning). 
 
 Projet réalisé par Nathan Wurpillot et Ryan Belaib dans le cadre du cours de Python de M.Zemali en deuxième année du cursus IR à Télécom Physique Strasbourg.

## 🚀 Fonctionnalités

- 🎮 Jeu de casse-brique classique
- 🧠 Intelligence artificielle utilisant l'apprentissage par renforcement
- 📊 Entraînement par exploration, jeu autonome

## 🛠️ Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Nathan-Wrpt/casse-brique-rl
    cd casse-brique-rl
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## 🎯 Utilisation

Pour entrainer le modèle avec 100 epochs et sauvegarder le modèle entrainé dans le répertoire spécifié :
```bash
python3 main.py train --epochs=100 --model=models/final_models.h
```
L'option ```train``` permet de spécifier que vous souhaitez **entrainer** le modèle, ```--epochs``` permet de préciser le nombre d'épochs d'entraînement et ```--model``` spécifie l'emplacement de sauvegarde du modèle entrainé.

Note : Les options ne sont pas nécessaires :
- --epochs a pour valeur 100 par défaut et model a par défaut models/model_300_epochs.h5
- -- model a par défaut models/model_300_epochs.h5 quand on est en mode play, et models/trainedmodel.h5 quand on est en mode train 

Lancer la commande :

```bash
python3 main.py
```
permet de lancer l'apprentissage avec les paramètres spécifiés plus haut.

Pour lancer une partie en autonomie complète depuis un modèle entrainé :

```bash
main.py play --model=models/model.h5
```
L'option ```--model``` permet de choisir le modèle à utiliser.

**Si vous ne disposez pas de temps pour entraîner un modèle complet, le modèle ```model_300_epochs.h5```vous permettra de tester le jeu de manière autonome. Il a été entraîné sur 300 epochs.**


## 📂 Structure du projet

- `main.py` : Point d'entrée du jeu
- `game/` : Contient la logique du jeu
- `models/` : Contient les modèles entrainés
- `rl_agent/`: Contient toutes les fonctions relatives à l'agent d'apprentissage par renforcement
- `requirements.txt`: Contient les dépendances à installer dans votre environnement pour exécuter le projet

