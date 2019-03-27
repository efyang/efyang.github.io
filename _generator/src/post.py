from datetime import datetime
from bs4 import BeautifulSoup
import yaml
import os

class Post:
    def __init__(self, title, date, body):
        self.title = title
        self.body = body
        self.date = date
        self.posts_output_dir = None

    def preview_text(self, preview_length=300):
        soup = BeautifulSoup(self.body, features="lxml")

        preview_text = ""
        for paragraph in soup.findAll("p"):
            if len(preview_text) <= preview_length:
                if len(preview_text) + len(paragraph.getText()) > preview_length:
                    text = paragraph.getText()[:preview_length - len(preview_text)].rstrip()
                    if ' ' in text:
                        text = text[:text.rfind(' ')].rstrip()
                        preview_text += "\n<p>" + text + "...</p>\n"
                        break;
                else:
                    preview_text += "\n<p>" + paragraph.getText() + "</p>\n"
            else:
                break;

        return preview_text

    def formatted_date(self):
        return self.date.strftime("%B %-d, %Y").lower()

    @classmethod
    def load_from_dir(cls, d):
        with open(os.path.join(d, "config.yml"), 'r') as stream:
            config = yaml.load(stream)
            dt = datetime.strptime(config['time'], "%m/%d/%Y")
            body = open(os.path.join(d, "body.html"), 'r').read()
            return cls(config['title'], dt, body)

    def set_output_dir(self, d):
        self.posts_output_dir = d

    def hyphenated_title(self):
        return self.title.replace(' ', '-')

    def post_file(self):
        return str(os.path.join(self.posts_output_dir, self.hyphenated_title() + ".html"))
