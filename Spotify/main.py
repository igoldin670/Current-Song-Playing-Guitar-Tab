import time
from bs4 import BeautifulSoup
from selenium import webdriver
from spotify_info import get_current_song_data, get_song_name, get_artist_name

def format_song_artist(artist_name, song_name):
    """Combine artist name and song name into a formatted string."""
    if not artist_name or not song_name:
        return None

    formatted_artist = artist_name.lower().replace(" ", "%20")
    formatted_song = song_name.lower().replace(" ", "%20")

    return f"{formatted_artist}%20{formatted_song}"

def new_format_song_artist(artist_name, song_name):
    """Combine artist name and song name into a formatted string to use to find correct link in html."""
    if not artist_name or not song_name:
        return None

    formatted_artist = artist_name.lower().replace(" ", "-")
    formatted_song = song_name.lower().replace(" ", "-")

    return f"{formatted_artist}-{formatted_song}"


def update_songsterr_tab(driver, song_name, artist_name):
    """Update the current browser tab with Songsterr for the given song and artist."""
    name = format_song_artist(artist_name, song_name)
    newName = new_format_song_artist(artist_name, song_name)

    if name:
        search_url = f"https://www.songsterr.com/?pattern={name}"
        driver.get(search_url)
        print(f"Updated Songsterr tab for: {song_name} by {artist_name}")
        
        #Get the page source and parse it
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        #Find the anchor tag with the specific song URL
        anchor_tag = soup.find('a', href=lambda href: href and f'/a/wsa/{newName}-tab-s' in href)
        if anchor_tag:
            #Extract and construct the full URL
            relative_url = anchor_tag['href']
            full_url = f"https://www.songsterr.com{relative_url}" if relative_url.startswith('/') else relative_url
            print(f"Navigating to: {full_url}")
            driver.get(full_url)
        else:
            print(f"No matching tab URL found for: {song_name} by {artist_name}")
    else:
        print("Invalid song or artist name. Cannot update Songsterr.")

def main(interval=5):
    """Continuously fetch and update the currently playing song on Songsterr."""
    last_song = None
    last_artist = None

    driver = webdriver.Chrome()
    print("Monitoring currently playing song... (Press Ctrl+C to stop)")
    
    try:
        while True:
            song_data = get_current_song_data()
            if song_data:
                song_name = get_song_name(song_data)
                artist_name = get_artist_name(song_data)

                #Refresh only if the song has changed
                if song_name != last_song or artist_name != last_artist:
                    update_songsterr_tab(driver, song_name, artist_name)
                    last_song = song_name
                    last_artist = artist_name
                else:
                    print(f"No change in currently playing song: {song_name} by {artist_name}")
            else:
                print("No song is currently playing.")

            #Wait for the specified interval before checking again
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped monitoring the currently playing song.")
    finally:
        driver.quit()  #Ensure the browser closes when the script ends

if __name__ == '__main__':
    main(interval=5)