
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

## Troubleshooting
#### Fixing an Enshrouded Version Mismatch

If the server is visible and running but the game reports Version Mismatch, SteamCMD may have failed to apply an update and left its manifest stuck.

Typical container logs include:
`Error! App '2278520' state is 0x6 after update job.`
Update procedure

#### Run these commands from this stack’s Compose directory.

Stop the server before changing its installed game files:
```bash
docker compose stop enshrouded
```
Start a temporary shell with the same mounted server data:"
```bash
docker compose run --rm --no-deps --entrypoint sh enshrouded
```
Inside the temporary container, back up and remove only SteamCMD’s active manifest:
```bash
cd /home/steam/enshrouded/steamapps

cp appmanifest_2278520.acf "appmanifest_2278520.acf.stuck-$(date +%F-%H%M%S)"
rm appmanifest_2278520.acf
```
| This does not delete the world, configuration, or Enshrouded server files. It removes only SteamCMD’s record of the installed version.
Update and validate the Windows server depot used by Proton:
```bash
/usr/games/steamcmd \
  +@sSteamCmdForcePlatformType windows \
  +force_install_dir /home/steam/enshrouded \
  +login anonymous \
  +app_update 2278520 validate \
  +quit
```
Wait for this success message:
`Success! App '2278520' fully installed.`
If SteamCMD first updates itself or reports Missing configuration, run the same command a second time.
Confirm the installed and target build IDs match:
```bash
grep -E '"(buildid|TargetBuildID|StateFlags|UpdateResult)"' \
  /home/steam/enshrouded/steamapps/appmanifest_2278520.acf
```
Start the server back 
```bash
docker compose up -d enshrouded
docker logs -f enshrouded
```
