from requests_html import HTMLSession
import atparts


class Quoter:
    quote = []

    def __init__(self):
        self.start_session()
        self.loggedin = False
    
    def start_session(self):
        self.session = HTMLSession()
        self.active = True
    
    def close_session(self):
        self.session.close()
        self.active = False
    
    def part(self, pn):
        info = atparts.get_part(self.session, pn, self.loggedin, verbose=True)
        if info:
            self.quote.append(info)
            return info._asdict()
        return None



