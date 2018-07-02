
class Job:
    def __init__(self, job_metadata, job_description):
        self.metadata = job_metadata
        self.description = job_description

    def get_id(self):
        return self.metadata.job_id


class JobMetadata:   # Acquired from Crawler - general info
    def __init__(self, title='', date='', location='', company='', url='', job_id=0):
        self.title = title
        self.date = date
        self.location = location
        self.company = company
        self.origin_url = url
        self.job_id = job_id


# Acquired from JobParser - job description document

class JobDescription:
    def __init__(self, soup):
        self.url = None
        self.keywords = None
        self.passed = False
        self.soup = soup
        self.text = soup.text

