
# Enshrouded Server

Docker Compose stack for a private Enshrouded dedicated server.

## Networking

The server attaches to the shared external `game-tunnel` Docker network.
Playit forwards traffic to the Enshrouded container; no game ports are published
on the Fedora host or forwarded through the router.

Two Playit UDP tunnels are required:

- Game: `enshrouded:15636`
- Query: `enshrouded:15637`

Players search for the server using the query endpoind pinned my discord channel:

## Data

data/ contains the Enshrouded server installation, configuration, logs, and
world save files. It is ignored by Git.

The migrated world save is located in:
`data/savegame/`

## Maintenance

The server uses the host ntsync device for improved Proton stability.
Ensure the ntsync module is loaded after host reboots:
ls -l /dev/ntsync

## Configuration

Server settings are configured through .env, including server name, player
slots, passwords, update schedule, restarts, and difficulty.

The server uses the official Relaxed difficulty preset:
`GAME_SETTINGS_PRESET=Relaxed`

## World migration

The original local world was copied from Steam Cloud to data/savegame/.
The previous hosted save is retained on the original machine as a backup.

Do not host the old local save again after migration; it will create a separate,
diverging version of the world.
