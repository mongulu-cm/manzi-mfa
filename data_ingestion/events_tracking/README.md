# Events Tracking

Ce projet contient le code source et les fichiers de support pour une application serverless que vous pouvez déployer avec le SAM CLI. Il inclut les fichiers et dossiers suivants :

- `event-tracking` - Code pour la fonction Lambda de l'application.
- `events` - Événements d'invocation que vous pouvez utiliser pour invoquer la fonction.
- `tests` - Tests unitaires pour le code de l'application.
- `template.yaml` - Un modèle qui définit les ressources AWS de l'application.

L'application utilise plusieurs ressources AWS, y compris des fonctions Lambda et une API Gateway. Ces ressources sont définies dans le fichier `template.yaml` de ce projet. Vous pouvez mettre à jour le modèle pour ajouter des ressources AWS via le même processus de déploiement qui met à jour votre code d'application.

## Prérequis

Pour utiliser le SAM CLI, vous avez besoin des outils suivants :

- SAM CLI - [Installer le SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3 installé](https://www.python.org/downloads/)
- Docker - [Installer Docker Community Edition](https://hub.docker.com/search/?type=edition&offering=community)

## Déploiement de l'application

Pour construire et déployer votre application pour la première fois, exécutez les commandes suivantes dans votre terminal :

```bash
sam build --use-container
sam deploy --guided
```

