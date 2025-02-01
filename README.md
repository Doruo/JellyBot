# JellyBot - Jellyfin Discord Bot

Bot discord qui notifie le statut d'un serveur multimédia Jellyfin et de ses nouveaux contenus.

## Fonctionnalités

- Notification régulier de l'état du serveur
- Notification de nouveaux épisodes mis en ligne 

## Commandes Disponibles

- `/status` - Notifie l'état du serveur
- `/recents` - Notifie les nouveaux épisodes mis en ligne

## Idées d'ajouts futures

- Envoyer des recommendations au serveur
- Traduire en anglais la documentation et le README

## Installation

1. Cloner le repo

### Méthode HTTPS

```bash
git clone https://github.com/Doruo/JellyBot.git
```
### Méthode SSH 

#### (Il faut utiliser un mot de passe chiffré par une clé SSH publique)

```bash
git clone https://github.com/Doruo/JellyBot.git
```

2. Installer les dépendances nécessaires
```bash
pip install discord.py requests python-dotenv
```

3. Créer un fichier `.env` à la racine du projet et ajouter ces informations:
```
DISCORD_TOKEN=votre_token
JELLYFIN_API_KEY=votre_key
JELLYFIN_URL=votre_url
DISCORD_CHANNEL_ID=votre_channel
```

4. Lancer le bot
```bash
python jellybot.py
```

## Configuration Discord

1. Créer une application : Discord Developer Portal
2. Dans l'onglet "Bot", créer un bot
3. Cliquer sur "Reset Token" pour générer un nouveau token
4. Copier ce token et le coller dans votre fichier .env (DISCORD_TOKEN)
5. Inviter le bot sur votre serveur en utilisant le lien d'invitation généré dans l'onglet "OAuth2"

## Configuration Serveur Jellyfin

1. Dans Jellyfin, aller dans Dashboard > API Keys
2. Générer une nouvelle clé API
3. Copier cette clé dans votre fichier .env (JELLYFIN_API_KEY)
4. Ajouter l'URL de votre serveur dans .env (JELLYFIN_URL)

## Configuration du Channel Discord

1. Activer le mode développeur dans Discord (Paramètres > Avancés)
2. Faire clic droit sur le canal souhaité et "Copier l'identifiant"
3. Coller cet ID dans votre fichier .env (DISCORD_CHANNEL_ID)

## Contributeurs

- Marc Haye, contributeur principale.
- Yann Bodiguel, pour la configuration de python et de l'environnement d'execution local.

## Bibliothèques utilisés

- [Jellyfin - The Free Software Media System ](https://jellyfin.org/)

- [discord.py](https://discordpy.readthedocs.io/en/stable/)

- [requests - PyPI](https://pypi.org/project/requests/)