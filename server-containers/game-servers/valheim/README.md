# Valheim Server

Docker Compose stack for a private Valheim dedicated server.

## Networking
The server attaches to the shared external `game-tunnel` Docker network.
The Playit agent reaches Valheim at `valheim:2456`; no Valheim ports are
published on the Fedora host or forwarded through the router.

Players join using the Playit endpoint or a Cloudflare DNS alias pinned in my discord server

    config/ contains worlds, configuration, logs, and backups.
    data/ contains the downloaded Valheim dedicated-server files.
    Both directories are ignored by Git.
    Backups run daily at 04:00 Adelaide time.
    The newest three backup archives are retained.

## Maintenance
Apply configuration changes or start the server:

`docker compose up -d`

The image checks for Valheim updates automatically every 15 minutes while no
players are connected. If an update is installed, the server restarts. Discord
notifications are sent for startup, restart, player connections, and updates.
World seed

The seed is stored as the second line of the world .fwl file config/worlds_local/forever_valheim.fwl

## Creating the Valheim 1.0 world
This current world is disposable. To generate a new random 1.0 world, change
WORLD_NAME in .env to a new identifier, then run:
`docker compose up -d`

Valheim creates a new world when no matching save exists. Keep the old world
files unless you are certain they are no longer needed.

## External documentation
The repo for the image is located at https://github.com/community-valheim-tools/valheim-server-docker
