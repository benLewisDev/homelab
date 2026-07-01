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
    admin = Custom("Admin", "../custom-icons/admin.png")

    with Cluster("HomeLab"):
        switch = Switch("5 Port Switch")
        # Piping
        router >> switch

        with Cluster("The Butler"):
            server_machine = Custom("The Butler", "../custom-icons/fedora.png")
            cockpit = Custom("Cockpit", "../custom-icons/cockpit.png")
            tailscale = Custom("Tailscale", "../custom-icons/tailscale.png")
            # Piping
            switch >> server_machine
            admin >> tailscale

            with Cluster("Docker Services"):
                cloudflare_tunnel = Custom(
                    "cloudflare\ntunnel", "../custom-icons/cloudflare.png"
                )
                # Piping
                cloudflare_tunnel << tunnel_access << user
                docker_directory = Docker("/srv/homelab/\ndocker-services")
                server_machine >> docker_directory
                cockpit >> cloudflare_tunnel

                with Cluster("Servarr"):
                    media_directory = Folder("Media\nDirectory")
                    # with Cluster("Jellyfin stack"):
                    #     jellyseer = Custom(
                    #         "Jellyseer", "../custom-icons/jellyseerr.png"
                    #     )
                    #     jellyfin = Custom("Jellyfin", "../custom-icons/jellyfin.png")
                    with Cluster("Servarr stack"):
                        jellyseer = Custom(
                            "Jellyseer", "../custom-icons/jellyseerr.png"
                        )
                        jellyfin = Custom("Jellyfin", "../custom-icons/jellyfin.png")
                        qbittorent = Custom(
                            "qBittorent", "../custom-icons/qbittorrent.png"
                        )
                        sonarr = Custom("Sonarr", "../custom-icons/sonarr.png")
                        radarr = Custom("Radarr", "../custom-icons/radarr.png")
                        prowlarr = Custom("Prowlarr", "../custom-icons/prowlarr.png")
                        bazarr = Custom("Bazarr", "../custom-icons/bazarr.png")
                    # Piping
                    jellyfin >> cloudflare_tunnel
                    jellyfin << media_directory
                    qbittorent >> media_directory

                with Cluster("AI LLM"):

                    with Cluster("Open Web UI stack"):
                        open_web_ui = Custom(
                            "Open Web UI", "../custom-icons/open-webui.png"
                        )
                        ollama = Custom("Ollama", "../custom-icons/ollama.png")
                    # Piping
                    open_web_ui >> cloudflare_tunnel

                with Cluster("Portainer stack"):
                    portainer = Custom("Portainer", "../custom-icons/portainer-v1.png")
                    # Piping
                    docker_directory >> portainer

                with Cluster("Homarr stack"):
                    homarr = Custom("homarr", "../custom-icons/homarr.png")
                    # piping
                    homarr >> cloudflare_tunnel

                with Cluster("Monitoring"):
                    with Cluster("Beszel Stack"):
                        beszel_ui = Custom("Beszel-UI", "../custom-icons/beszel.png")
                        beszel_agent = Custom(
                            "Beszel-Agent", "../custom-icons/beszel.png"
                        )
                        # piping
                        beszel_agent >> homarr
