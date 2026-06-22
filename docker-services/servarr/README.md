# Servarr

## Table of contents

- Purpose
- Prerequisites
- Deployment
- Configuration
- Useful commands

### Purpose

This docker compose stack contains all the services required to run jellyfin and accompanying content retrieval automation. I use this technology to only obtain copyrighted material i have legal ownership of.

---

### Prerequisites

1. Docker installed and configured
2. Docker Compose
3. Mount any larger drives that you want to store the media on to `/srv/homelab/docker-services/servarr/data`
4. A file tree with the following layout in `/srv/homelab/docker-services/servarr`

```tree
data/
├── media
│   ├── movies
│   ├── music
│   └── tv
└── torrents
    ├── movies
    ├── music
    └── tv
```

#### Deployment

To deploy simply run:

```bash
docker compose up -d
```

**NOTE:** Unfortunately a limitation of this design requires that all containers be updated simultaneously, To do so run the below two commands

```bash
docker compose pull
docker compose up -d
```

---

## Configuration

Below are the steps needed to take in the GUI of each application for the configuration.

### qBittorrent

Check logs for qbittorrent container:
`sudo docker logs qbittorrent`
You will see in the logs something like:
_The WebUI administrator username is: admin
The WebUI administrator password was not set. A temporary password is provided for this session: <your-password-will-be-here>_
Now you can go to URL:
If you are on the host: `http://localhost:8080`
From other device on your network: `http://<host ip address>:8080`
and log on using details provided in container logs.
Go to `Tools - Options - WebUI` - you can change the user and password here but remember to scroll down and save it.

In left panel go to Categories - All - right click and 'add category':

For Radarr: `Category: movies`
`Save Path: movies` (this will be appended to '/data/torrents/ Default Save Path you set above)
For Sonarr: `Category: tv`
`Save Path: tv`
For Lidarr: `Category: music`
`Save Path: music`

Create categories first and only then configure the steps below, as doing it opposite way round caused the Categories to disappear :)

With categories created - go to - `Tools - Options - Downloads` and in `Saving Management` make sure your settings match [THIS](https://trash-guides.info/Downloaders/qBittorrent/How-to-add-categories/)
So `Default Torrent Management Mode - Automatic`
`When Torrent Category changed - Relocate torrent`
`When Default Save Path Changed - Switch affected torrents to Manual Mode`
`When Category Save Path Changed - Switch affected torrents to Manual Mode`
Tick BOTH BOXES for `Use Subcategories` and `Use Category paths in Manual Mode` (NOT shown on Trash Guides)
Default Save Path: - set to `/data/torrents` (so it matches your folder structure) - then scroll down and `Save`.
On Trash Guides it shows `Copy .torrent files to` but its optional, you can leave it blank

If you still have problems with adding categories, you can use different image like the one below:

```yaml
  qbittorrent:
    <<: *common-keys
    container_name: qbittorrent
    image: ghcr.io/qbittorrent/docker-qbittorrent-nox:latest
    ports:
      - 8080:8080
      - 6881:6881
      - 6881:6881/udp
    environment:
      - QBT_LEGAL_NOTICE=confirm
      - WEBUI_PORT=8080
      - TORRENTING_PORT=6881
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /docker/appdata/qbittorrent:/config
      - /data:/data
```

Thats it for qBittorrent.

Now configure Prowlarr service (each of these services will require to set up user/pass):
Use 'Form (login page) authentication and set your user and pass for all.

### Prowlarr

`http://<host_ip>:9696`
Go to `Settings - Download Clients` - `+` symbol - Add download client - choose `qBittorrent` (unless you decided touse different download client)
UNTICK the `Use SSL` (unless you have SSL configured in qBittorrent - Tools - Options -WebUI but by default it is not used)
Host - use `qbittorrent` and port - put the port id matching the WebUI in docker-compose for qBittorrent (default is `8080`)
username and password - use the one that you configured for qBittorrent in previous step
Click little `Test` button at the bottom, make sure you get a green `tick` then `Save`.

### Radarr

`http://<host_ip>:7878`
Go to `Settings - Media Management - Add Root Folder` (scroll down to the bottom) - set `/data/media/movies` as your root folder
Still in `Settings - Media Management - click Show Advanced - Importing - Use Hardlinks instead of Copy` - make sure its 'ticked'

Optional - you can also tick `Rename Movies` and `Delete empty movie folders during disk scan` , and in `Import Extra Files` - make sure that box is ticked
and in `Import Extra files` field type `srt,sub,nfo` (those 3 changes are all optional)

Then `Settings- Download clients` - click `plus` symbol, choose `qBittorrent` etc - basically same steps as for Prowlarr
so Host `qbittorrent`, port `8080`, ,make sure SSL is unticked, username admin and password - one you configured for qBittorrent
and change the Category to `movies` (needs to match qbittorrent Category)
Now click the `Test` and if you have green 'tick' - `Save`.
Now go to `Settings - General` - scroll down to API key - Copy API key - go back to `Prowlarr - Settings - Apps` -click `+` - Radarr - paste API key.
Then change `Prowlarr Server` to `http://prowlarr:9696` and `Radarr Server` to `http://radarr:7878`
Click `Test` and if Green - Save

BTW - you can see how to configure each service for hardlinks [HERE](https://trash-guides.info/File-and-Folder-Structure/Examples/)
You need to configure SABnzbd / qbittorrent and any other services you run too, not only Radarr or Sonarr

### Sonarr

`http://<host_ip>:8989`
Go to `Settings - Media Management - Add Root Folder` - set `/data/media/tv` as your root folder
Still in `Settings - Media Management - Show Advanced - Importing - Use Hardlinks instead of Copy` - make sure its 'ticked'

Optional - you can also tick `Rename Episodes` and `Delete empty Folders - delete empty series and season folders during disk scan`
Then in `Import Extra Files` - make sure that box is ticked and in `Import Extra files` field type `srt,sub,nfo` (those 3 changes are all optional)

Then `Settings- Download clients` - click `plus` symbol, choose `qBittorrent` etc - basically same steps as for previous services
Host `qbittorrent`, port `8080`, ,make sure SSL is unticked, username admin and password - one you configured for qBittorrent
and change the Category to 'tv' (by default its 'tv-sonarr', but you need to match qbittorrent Category)
Now click the 'Test' and if you have green 'tick' - Save.
Now go to `Settings - General` - scroll down to API key - Copy API key - go back to Prowlarr - Settings - Apps -click '+' - Sonarr - paste API key.
Then change `Prowlarr Server` to `http://prowlarr:9696` and `Sonarr Server` to `http://sonarr:8989`
Click `Test` and if Green - `Save`

### Bazarr

`http://host_ip>:6767`
Languages: Go to Settings > Languages and create a "Language Profile" (e.g., "English" or "Any").
Providers: Go to Settings > Providers and add your subtitle sources (OpenSubtitles.org, Subscene, etc.). Most require a free account.
Sync: After connecting Radarr/Sonarr, go to the Series or Movies tab and click "Update" to pull in your existing library.

### Restart services

It might be a good idea to restart all services and see if they come up as expected:

```bash
sudo docker compose down
sudo docker compose up -d
```

### Remaining config

That should be it, you just need to add some indexers to Prowlarr.
You can add more indexers - just google for something like 'what are the best legal indexers for Prowlarr' or something similar.

It is a common misconception that the "Arr" stack is only for pirated content.
In reality, these are powerful automation tools for managing media, and there is a wealth of legal, copyright-free, and open-source content you can use them for.
In Radarr, you can download movies that have entered the Public Domain or are released under Creative Commons licenses.
Public Domain Classics: These are "Golden Age" movies where the copyright was not renewed like:
Night of the Living Dead (1968), His Girl Friday (1940), Charade (1963), and The General (1926).
Configure Prowlarr with The "Gold Standard" Indexer for legal media like The Internet Archive (Archive.org).
They host thousands of public domain movies.

---

### Jellyfin

`http://<host ip address>:8096`
To watch your movies, just log on to Jellyfin, create user and password and you can `Add Media Library`.
For Content Type - choose `Movies` and find folder `/data/media/movies`.
Add more content types like TV or Music accordingly, binding them to correct media folder.

---

## Troubleshooting

## DNS check

Test if your containers use CloudFlare DNS (configured in docker-compose.yml file):
`sudo docker exec -it radarr cat /etc/resolv.conf`

## Hardlinks check

Check if the hardlinks work as expected:
Go to `/data` folder on your host and run `tree` and `du -sch *` commands to see the folder structure.
Find the same file in torrents and media that you have just downloaded and run commands:
`ls -i /data/media/movies/<your video>` and check its inode id (in first column, like 3881112)
Then run again the same command but for the torrent folder:
`ls -i /data/torrents/movies/<your video>` and see if the inode id is the same as above.
If they are - your hardlinks work as expected.
If they don't - first go to logs to see what is the problem (for Radarr/Sonarr go to System - Log Files)
If you have issue where the file is copied rather than hardlinked, then the most probable cause
is the read/write permission on either source or destination, but that can all be found in those logs so start there.

## Files do not move from torrents to media folder

If the video does not move automatically from torrents to media, then check the Activity - Queue.
You might have a flag saying: 'Downloaded - Unable to Import Automatically'
Click the Manual Import (icon that looks like human head on the far right of the item row)
Confirm the Movie: In the popup, ensure the correct movie is selected in the dropdown. If it is correct, click 'Import'

## FlareSolverr

You might want to add FlareSolverr if you find Prowlarr is failing to index some sites due to "Cloudflare" blocks:

```yaml
####################################################
# FLARESOLVERR - Cloudflare Bypass
####################################################

  flaresolverr:
    <<: *common-keys
    container_name: flaresolverr
    image: ghcr.io/flaresolverr/flaresolverr:latest
    ports:
      - 8191:8191
    environment:
      - LOG_LEVEL=info
```

Once the container is running, you need to tell Prowlarr to use it:

- Open your Prowlarr Web UI (<http://localhost:9696>)
- Go to Settings > Indexers.
- Click the + (Add) button under Indexer Proxies and select FlareSolverr.
- Fill in the details:
- Name: FlareSolverr
- Host: <http://flaresolverr:8191> (Note: Using the service name flaresolverr works because they are on the same Docker network).
- Tags: Give it a tag like cloudflare (this is important).
- Save the proxy

---

## Jellyfin hardware acceleration

For Jellyfin hardware acceleration you might want to add bottom 2 lines:

```yaml
jellyfin:
    <<: *common-keys
    <...snip...>
    devices:
      - /dev/dri:/dev/dri # << container setting to pass through GPU (this requires more steps outside of docker compose though)
```

---

## Useful Commands

- Check how much space individual files are taking up

```bash
du -csh *
```
