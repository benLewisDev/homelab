# Homelab High Level Overview
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.generic.blank import Blank
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
                docker_directory = Folder("/srv/docker-services")
                server_machine >> docker_directory
                with Cluster("Media"):
                    media_directory = Folder("Media Directory")
                    with Cluster("Jellyfin"):
                        jellyfin = Docker("Jellyfin")
                        jellyseer = Docker("JellySeer")
                    with Cluster("automation"):
                        qbittorent = Docker("qBittorent")
                        sonarr = Docker("Sonarr")
                        radarr = Docker("Radarr")

                    jellyfin >> user
                    jellyfin >> media_directory
                    qbittorent >> media_directory
                    jellyseer >> radarr
                    jellyseer >> sonarr
                with Cluster("AI LLM"):

                    with Cluster("Open Web UI"):
                        open_web_ui = Docker("Open Web UI")
                        ollama = Custom("Ollama", "./custom-icons/ai-assistant.png")
                    with Cluster("Lite LLM"):
                        lite_LLM = Docker("")
                    open_web_ui >> user
                    lite_LLM >> open_web_ui

                with Cluster("Portainer"):
                    portainer = Docker("Portainer")
                    portainer >> admin
