# Playit.gg Tunnel Agent

## Info

Playit.gg is an agent that opens a tunnel to allow forwarding of UDP traffic for use with games servers.

It provides a way to make game servers accessible from the internet while the home connection is behind carrier-grade NAT.

## Networking
The Playit agent creates and owns the shared Docker bridge network named `game-tunnel`. 
Each game server runs in its own Compose stack but attaches to that external network, allowing the Playit agent to reach it by its Docker service name and internal port. 
No game ports need to be published on the Fedora host or forwarded through the router.

See below example compose example for adding a new services to the network.
```
    networks:
      - game-tunnel

networks:
  game-tunnel:
    external: true
    name: game-tunnel
```


## Maintenance notes

**Warning!** Do not use `docker compose down` in the Playit stack because it attempts to remove resources created by that stack, including the shared `game-tunnel` network. Other game-server stacks depend on this network to communicate with the Playit agent, so removing it can disconnect or prevent those services from starting. Use `docker compose up -d` to apply changes; Docker will recreate only the services that need updating while preserving the shared network.

## Healthcheck notes
The Docker health check only confirms that the agent process is running. The Playit dashboard confirms whether the agent and tunnels are actually connected.
