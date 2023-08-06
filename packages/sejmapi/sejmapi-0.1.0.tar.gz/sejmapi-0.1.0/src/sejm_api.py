from requests import get
import json
class SejmApi():
    def __init__(self,term):
        self.term = term
    def get_all_MP(self):
        MP_list = get(f'http://api.sejm.gov.pl/sejm/term{self.term}/MP').text
        MP_list = json.loads(MP_list)
        return MP_list
    def get_MP_info(self,leg):
        info = get(f'http://api.sejm.gov.pl/sejm/term{self.term}/MP/{leg}').text
        info = json.loads(info)
        return info
    def getPhoto(self,leg):
        photo = f'http://api.sejm.gov.pl/sejm/term{self.term}/MP/{leg}/photo'
        return photo
    def getClubs(self):
        clubs = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/clubs').text
        clubs = json.loads(clubs)
        return clubs
    def getClub_info(self,id):
        club_info = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/clubs/{id}').text
        club_info = json.loads(club_info)
        return club_info
    def getClublogo(self,id):
        logo = f'https://api.sejm.gov.pl/sejm/term{self.term}/clubs/{id}/logo'
        return logo
    def getCommittees(self):
        commitees = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/committees').text
        commitees = json.loads(commitees)
        return commitees
    def getStreams(self):
        videos = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/videos').text
        videos = json.loads(videos)
        return videos
    def getTodayStreams(self):
        streams = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/videos/today').text
        streams = json.loads(streams)
        return streams
    def getTermInfo(self):
        term = get(f'http://api.sejm.gov.pl/sejm/term{self.term}').text
        term = json.loads(term)
        return term
    def getPrints(self):
        prints = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/prints/').text
        prints = json.loads(prints)
        return prints
    def getPrint_info(self,nr):
        info = get(f'https://api.sejm.gov.pl/sejm/term{self.term}/prints/{nr}').text
        info = json.loads(info)
        return info
    def getPrint_attachment(self,nr,fileName):
        attachment = f'https://api.sejm.gov.pl/sejm/term{self.term}/prints/{nr}/{fileName}'
        return attachment
sejm = SejmApi(term=9)