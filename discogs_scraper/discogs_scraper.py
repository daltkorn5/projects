"""
Web scraper that loops through a list of albums on discogs.com, gets the tracks and some metadata
for each album, and then writes out the track, album title, and other metadata to a CSV.
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv


def scrape_tracks(title_url, *album_metadata):
    """Function that scrapes all the tracks from the provided album URL.

    :param title_url: The URL of the album whose tracks we are scraping
    :param album_metadata: Other metadata associated with that album, such as title, artist, and year
    :return: A list of tuples, each tuple storing the information for one track. For example:
        [
            ("Track 1", "Artist 1", "Album 1", "1990"),
            ("Track 2", "Artist 1", "Album 1", "1990"),
        ]
    """
    tracks = []
    html = urlopen(f"https://www.discogs.com/{title_url}")
    soup = BeautifulSoup(html, features="lxml")

    rows = soup.find_all('tr', {'class': 'track'})
    for row in rows:
        track = row.find('td', {'class': 'track'}).get_text().strip()
        tracks.append((track, *album_metadata))

    return tracks


def scrape_album_list(url):
    """Function that scrapes a list of albums from discogs.com

    Loops through the albums and extracts the artist, album title, and year. Then gets all the
    tracks associated with that album.

    :param url: The URL with the list of albums
    :return: A list of tuples, each tuple storing the information for one track. For example:
        [
            ("Track 1", "Artist 1", "Album 1", "1990"),
            ("Track 2", "Artist 1", "Album 1", "1990"),
            ...
            ("Track 1", Artist 1", "Album 343", "2020"),
        ]
    """
    all_tracks = []
    count = 0

    html = urlopen(url)
    soup = BeautifulSoup(html, features="lxml")

    albums = soup.find_all('tr', {'class': 'main'})
    for album in albums:
        artist = album.find('td', {'class': 'artist'}).get_text()

        # we take the last anchor tag here because there might be others associated with the artists
        title_element = album.find('td', {'class': 'title'}).find_all('a')[-1]
        title_url = title_element.get('href')
        album_title = title_element.get_text()
        year = album.find('td', {'class': 'year'}).get_text()

        all_tracks.extend(scrape_tracks(title_url, artist, album_title, year))

        count += 1
        if count % 10 == 0:
            print(f"Scraped {count} albums!")

    return all_tracks


def write_csv(tracks_list, filename="track_list.csv"):
    """Function to write the list of tracks out to a pipe-delimited CSV

    :param tracks_list: The list of tracks
    :param filename: The filename, defaults to "track_list.csv"
    """
    headers = ('track', 'artist', 'album', 'year')

    with open(filename, 'w+') as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(headers)
        writer.writerows(tracks_list)


def main():
    tracks = scrape_album_list("https://www.discogs.com/artist/135930-Sonny-Stitt?sort=year%2Casc&limit=500&page=1")
    write_csv(tracks)


if __name__ == '__main__':
    main()
