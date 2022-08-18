from .method import movie_info, get_preview

class Movie():
    def __init__(self, cid):
        info = movie_info(cid)
        self.name = info['title']
        self.runtime = info['volume']
        self.url = info['URL']
        self.poster = info['imageURL']['large']
        self.samples = info.get('sampleImageURL', {}).get('sample_l')
        self.genres = [i['name'] for i in info['iteminfo']['genre']]
        self.series = [i['name'] for i in info['iteminfo'].get('series', [])]
        self.actress = [a['name'] for a in info['iteminfo'].get('actress', [])]
        self.maker = [i['name'] for i in info['iteminfo']['maker']]
        self.label = [i['name'] for i in info['iteminfo']['label']]
        self.preview = get_preview(cid)
        self.date = info['date'][:10]
