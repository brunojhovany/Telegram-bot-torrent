# TransmissionTelegramBot fork from another repo only add more features
Quick implementation of the Python Transmission lib

## Tests:
You can tests the Transmission broker by doing `python broker.py` and It should queue ubuntu-8.10-desktop-i386.iso torrent. Legal use only right? right :P<br>
Run bot with `python transmission_bot/telegram_bot.py`

## Usage:
```txt
    /help - display this help
    /list - retrieve list of current torrents and their statuses
    /free_space - retrieve free device space
    /add <URI> - add torrent and start download
    /delete <ID> - delete torrent and downloaded data
```
## Docker compose example

```yaml
    version: '3.6'

    services: 

      transmission:
        image: lscr.io/linuxserver/transmission
        container_name: transmission
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=America/Mexico_City
          - TRANSMISSION_WEB_HOME=/combustion-release/ #optional
          - USER=admin #optional
          - PASS=admin #optional
          # - WHITELIST=iplist #optional
          - HOST_WHITELIST=dnsnane list #optional
        volumes:
          - ./config:/config:Z
          - /torrents:/downloads:Z
          - ./watch:/watch:Z
        ports:
          - 9091:9091
          - 51413:51413
          - 51413:51413/udp
        # restart: unless-stopped

      telegrambot:
        build: bot
        depends_on:
          - transmission
        restart: unless-stopped
        command: python /code/transmission_bot/telegram_bot.py
        environment:
          - ADDRESS=transmission
          - PORT=9091
          - TS_USER=admin
          - PASSWORD=admin
          - TOKEN=
          - PERSISTENCE_FILE=/var/lib/transmission-telegram/authorized_chats
```