# Homelab High Level Overview
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.generic.network import Router, Switch
from diagrams.onprem.container import Docker
from diagrams.digitalocean.storage import Folder

with Diagram(
    "Home Lab High Level Overview",
    show=False,
    filename="Homelab-high-level",
    direction="TB",
):
    router = Router("Router")

    with Cluster("HomeLab"):
        admin = Custom("Admin", "./custom-icons/admin.png")
        user = Custom("User", "./custom-icons/user.png")
        switch = Switch("5 Port Switch")
        router >> switch
        with Cluster("The Butler"):
            server_machine = Custom("The Butler", "./custom-icons/fedora.png")
            cockpit = Custom("Cockpit", "./custom-icons/cockpit.png")
            switch >> server_machine
            server_machine - cockpit
            cockpit >> admin
            with Cluster("Docker Services"):
                docker_directory = Docker("/srv/homelab/docker-services")
                server_machine >> docker_directory
                with Cluster("Media"):
                    media_directory = Folder("Media Directory")
                    with Cluster("Jellyfin"):
                        jellyfin = Custom("Jellyfin", "./custom-icons/jellyfin.png")
                        jellyseer = Custom("Jellyseer", "./custom-icons/jellyseerr.png")
                    with Cluster("automation"):
                        qbittorent = Custom(
                            "qBittorent", "./custom-icons/qbittorrent.png"
                        )
                        sonarr = Custom("Sonarr", "./custom-icons/sonarr.png")
                        radarr = Custom("Radarr", "./custom-icons/radarr.png")

                    jellyfin >> user
                    jellyfin >> media_directory
                    qbittorent >> media_directory
                    jellyseer >> radarr
                    jellyseer >> sonarr
                with Cluster("AI LLM"):

                    with Cluster("Open Web UI"):
                        open_web_ui = Custom(
                            "Open Web UI", "./custom-icons/open-webui.png"
                        )
                        ollama = Custom("Ollama", "./custom-icons/ollama.png")
                    with Cluster("Lite LLM"):
                        lite_LLM = Custom("Lite LLM", "./custom-icons/litellm.png")
                    open_web_ui >> user
                    lite_LLM >> open_web_ui

                with Cluster("Portainer"):
                    portainer = Custom("Portainer", "./custom-icons/portainer-v1.png")
                    portainer >> admin
