# Homelab High Level Overview
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.generic.network import Router, Switch
from diagrams.onprem.container import Docker
from diagrams.digitalocean.storage import Folder

with Diagram(
    "Home Lab High Level Overview",
    show=False,
    filename="./output/Homelab-high-level",
    direction="TB",
):
    router = Router("Router")
    tunnel_access = Custom(
        "Cloudflare\ntunnel", "../custom-icons/cloudflare-zero-trust.png"
    )
    user = Custom("User", "../custom-icons/user.png")

    with Cluster("HomeLab"):
        switch = Switch("5 Port Switch")
        admin = Custom("Admin", "../custom-icons/admin.png")
        # Piping
        router >> switch

        with Cluster("The Butler"):
            server_machine = Custom("The Butler", "../custom-icons/fedora.png")
            cockpit = Custom("Cockpit", "../custom-icons/cockpit.png")
            # Piping
            switch >> server_machine
            admin >> cockpit

            with Cluster("Docker Services"):
                cloudflare_tunnel = Custom(
                    "cloudflare\ntunnel", "../custom-icons/cloudflare.png"
                )
                # Piping
                cloudflare_tunnel << tunnel_access << user
                docker_directory = Docker("/srv/homelab/\ndocker-services")
                server_machine >> docker_directory

                with Cluster("Media"):
                    media_directory = Folder("Media\nDirectory")
                    with Cluster("Jellyfin stack"):
                        jellyseer = Custom(
                            "Jellyseer", "../custom-icons/jellyseerr.png"
                        )
                        jellyfin = Custom("Jellyfin", "../custom-icons/jellyfin.png")
                    with Cluster("automation stack"):
                        qbittorent = Custom(
                            "qBittorent", "../custom-icons/qbittorrent.png"
                        )
                        sonarr = Custom("Sonarr", "../custom-icons/sonarr.png")
                        radarr = Custom("Radarr", "../custom-icons/radarr.png")
                        prowlarr = Custom("Prowlarr", "../custom-icons/prowlarr.png")
                    # Piping
                    jellyfin >> cloudflare_tunnel
                    jellyfin >> media_directory
                    qbittorent >> media_directory
                    jellyseer >> radarr
                    jellyseer >> sonarr

                with Cluster("AI LLM"):

                    with Cluster("Open Web UI stack"):
                        open_web_ui = Custom(
                            "Open Web UI", "../custom-icons/open-webui.png"
                        )
                        ollama = Custom("Ollama", "../custom-icons/ollama.png")
                    with Cluster("Lite LLM stack"):
                        lite_LLM = Custom("Lite LLM", "../custom-icons/litellm.png")
                    # Piping
                    open_web_ui >> cloudflare_tunnel
                    lite_LLM >> open_web_ui

                with Cluster("Portainer stack"):
                    portainer = Custom("Portainer", "../custom-icons/portainer-v1.png")
                    # Piping
                    portainer << admin

                with Cluster("Pi-hole stack"):
                    pi_hole = Custom("Pi hole", "../custom-icons/pi-hole.png")
                    # piping
                    router >> pi_hole >> router
                    admin >> pi_hole
