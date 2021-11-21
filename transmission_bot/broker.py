import math

from transmissionrpc import Client, TransmissionError
from cfg import (ADDRESS, PORT, TS_USER, PASSWORD,
                 PERSISTENCE_FILE)


class TransmissionBroker:
    def __init__(self):
        print(f"user={TS_USER}, password={PASSWORD}")
        self.conn = Client(ADDRESS, PORT, user=TS_USER, password=PASSWORD)
        self.persistence = PERSISTENCE_FILE

    @staticmethod
    def pretty_torrents_list(torrents):
        info_list = []
        for torrent in torrents:
            percent = torrent.percentDone * 100
            info_list.append(
                f'Id: {torrent.id}. {torrent.name[:15]}. {torrent.status}:{percent}'
            )
        return '\n'.join(info_list)

    def retrieve_list(self, chat_id):
        torrents = self.conn.get_torrents()
        return TransmissionBroker.pretty_torrents_list(torrents)

    def free_space(self, chat_id):
        free_space = self.conn.free_space('/downloads/')
        free_space = round(free_space / 1000000000, 2)
        return free_space


    def add_torrent(self, chat_id, url):
        self.conn.add_torrent(url)

    def remove_torrent(self, chat_id, torrent_ids):
        # Check is not embedded to transmissionrpc module, so we have to do it ourselves
        missing_torrents = list()
        torrents = self.conn.get_torrents()
        torrent_ids = int(torrent_ids)
        # for tid in torrent_ids:
        id_found = False
        for torrent in torrents:
            if torrent_ids == torrent.id:
                id_found = True
                break
        if not id_found:
            missing_torrents.append(torrent_ids)
            

        if len(missing_torrents) > 0:
            raise TransmissionError(f'Torrents {missing_torrents} not found')

        self.conn.remove_torrent(torrent_ids, delete_data=True)


# Lets do some tests
if __name__ == "__main__":
    global_broker = TransmissionBroker()
    global_broker.add_torrent(
        None, 'http://releases.ubuntu.com/8.10/ubuntu-8.10-desktop-i386.iso.torrent')

    lst = global_broker.retrieve_list(None)
    print(lst)
