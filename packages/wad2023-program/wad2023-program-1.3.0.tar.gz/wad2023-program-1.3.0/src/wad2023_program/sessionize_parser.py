"""Module with the SessionizeParser.

Class that can be used to initiate a parser for Sessionize pages. Because the
organization of WeAreDevlopers 2023 have decided to turn off the REST API on
Sessionize, we have to parse the page using BeautifulSoup 4.
"""

from typing import Any
import requests
from bs4 import BeautifulSoup
from dateutil import parser

from .exceptions import HTMLNotDownloadedException


class SessionizeParser:
    """Parser for Sessionize pages.

    Parses Sessionize pages using BeautifulSoup 4.

    Attributes:
        sessionize_id: the ID for the meeting at sessionize.
        session: a list with the session for this program.
        speakers: a list with the speakers for this program.
    """

    def __init__(self, sessionize_id: str) -> None:
        """Set the defaults for the object.

        Sets the sessionize ID that is used later to parse the page.

        Args:
            sessionize_id: the ID for the meeting at sessionize. Is used in the
                URL to download the meetings.
        """
        self.session_id = sessionize_id

        # Sessions and speakers
        self.sessions: list[dict[str, Any]] | None = None
        self.speakers: list[dict[str, Any]] | None = None

        # Cache for the HTML
        self.cache: dict[str, str | None] = {
            'program': None,
            'speakers': None
        }

    @property
    def program_url(self) -> str:
        """Return the program URL from Sessionize for this program.

        Returns the URL to use when downloading the file from Sessionize.

        Returns:
            A string with the URL from Sessionize for the program.
        """
        return f'https://sessionize.com/api/v2/{self.session_id}/view/Sessions'

    @property
    def speakers_url(self) -> str:
        """Return the speakers URL from Sessionize for this program.

        Returns the URL to use when downloading the file from Sessionize.

        Returns:
            A string with the URL from Sessionize for speakers.
        """
        return f'https://sessionize.com/api/v2/{self.session_id}/view/Speakers'

    def download_pages(self) -> None:
        """Get HTML for the program and the speakers from the web.

        Retrieves the HTML for the program and the speakers from the web and
        saves them in the object cache.

        Raises:
            ValueError: when a wrong status code is returned.
        """
        for url in [
                ('program', self.program_url),
                ('speakers', self.speakers_url)]:
            download_request = requests.get(
                url=url[1],
                params={'under': True},
                timeout=10)
            if download_request.status_code != 200:
                raise ValueError(
                    ('Did not receive responsecode 200; got ' +
                     f'responsecode {download_request.status_code}'))
            self.cache[url[0]] = download_request.text

    def parse_program_html(self) -> None:
        """Parse the HTML for the program.

        Parses the program from the HTML returned by the webpage or from the
        cache. Saves it in the `sessions` attribute of the object.

        Raises:
            HTMLNotDownloadedException: when the HTML for the program page has
                not been downloaded yet.
        """
        # Local variable for the HTML
        if self.cache['program'] is None:
            raise HTMLNotDownloadedException('HTML for the program is not' +
                                             'downloaded yet')

        program_html = self.cache['program']
        self.sessions = []

        # Parse the HTML
        soup = BeautifulSoup(program_html, 'html.parser')
        session_list = soup.find_all('ul', {'class': 'sz-sessions--list'})
        sessions = session_list[0].find_all(
            'li', {'class': 'sz-session--full'})

        # Loop through the session and create the correct objects
        for session in sessions:
            # Create a new dict for the sessions
            session_object: dict[str, Any] = {}

            # Get the session ID
            session_object['uid'] = int(session['data-sessionid'])

            # Get the title
            session_object['title'] = session.find_all('h3')[0].text.strip()

            # Get the description
            description_tag = session.find_all(
                'p', {'class': 'sz-session__description'})
            if len(description_tag) == 1:
                session_object['description'] = description_tag[0].text.strip()

            # Get the stage
            stage = session.find_all('div', {'class': 'sz-session__room'})[0]
            session_object['stage'] = {
                'uid': stage['data-roomid'],
                'name': stage.text
            }

            # Get the speakers
            speakers = session.find_all(
                'ul', {'class': 'sz-session__speakers'})
            session_object['speakers'] = []
            for speaker in speakers[0].find_all('li'):
                speaker_object = {
                    'uid': speaker['data-speakerid'],
                    'name': speaker.text.strip()
                }
                session_object['speakers'].append(speaker_object)

            # Get the session times
            session_time = session.find_all(
                'div', {'class': 'sz-session__time'})[0]
            time_attribute = session_time['data-sztz'].split('|')
            session_object['start_time'] = parser.parse(time_attribute[2])
            session_object['end_time'] = parser.parse(time_attribute[3])

            # Append the session to the list
            self.sessions.append(session_object)

    def parse_speakers_html(self) -> None:
        """Parse the HTML for the speakers.

        Parses the speakers from the HTML returned by the webpage or the cache.
        Saves it in the `speakers` attribute of the object.

        Raises:
            HTMLNotDownloadedException: when the HTML for the speakers page has
                not been downloaded yet.
        """
        if self.cache['speakers'] is None:
            raise HTMLNotDownloadedException('HTML for the speakers is not' +
                                             'downloaded yet')

        speakers_html = self.cache['speakers']
        self.speakers = []

        # Parse the HTML
        soup = BeautifulSoup(speakers_html, 'html.parser')
        speaker_list = soup.find_all('ul', {'class': 'sz-speakers--list'})
        speakers = speaker_list[0].find_all(
            'li', {'class': 'sz-speaker'})

        # Loop through the speakers and create the correct objects
        for speaker in speakers:
            # Create a Speaker object
            speaker_object = {}

            # Get the UID for this speaker
            speaker_object['uid'] = speaker['data-speakerid']

            # Get the image for the speaker
            image_objects = speaker.find_all('img')
            if len(image_objects) == 1:
                try:
                    speaker_object['img_url'] = image_objects[0]['src']
                except KeyError:
                    speaker_object['img_url'] = ''

            # Get the name and tagline
            speaker_object['name'] = speaker.find_all('h3')[0].text.strip()
            speaker_object['tagline'] = speaker.find_all('h4')[0].text.strip()

            # Get the speaker bio
            bio = speaker.find_all(
                'p', {'class': 'sz-speaker__bio'})
            if len(bio) == 1:
                speaker_object['bio'] = bio[0].text.strip()

            # Get the links for the speaker
            links = speaker.find_all('ul', {'class': 'sz-speaker__links'})
            speaker_object['links'] = {}
            try:
                for link in links[0].find_all('li'):
                    link_tag = link.find_all('a')
                    speaker_object['links'].update(
                        {link_tag[0]['title']: link_tag[0]['href']}
                    )
            except IndexError:
                pass

            self.speakers.append(speaker_object)

    def update(self) -> None:
        """Update the sessions and speakers.

        Updates the sessions and speakers for this event.
        """
        self.download_pages()
        self.parse_speakers_html()
        self.parse_program_html()
