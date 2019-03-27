import yaml
import os

class Project:
    def __init__(self, name, body, skills=None, github=None, document=None):
        self.name = name
        self.body = body
        self.skills = skills
        self.github = github
        self.document = document

    @classmethod
    def load_from_dir(cls, d):
        with open(os.path.join(d, "config.yml"), 'r') as stream:
            config = yaml.load(stream)

            skills = None
            github = None
            document = None

            if "skills" in config.keys():
                skills = config["skills"]
            if "github" in config.keys():
                github = config["github"]
            if "document" in config.keys():
                document = config["document"]

            body = open(os.path.join(d, "body.html"), 'r').read()
            return cls(config['name'], body, skills=skills, github=github, document=document)

    def hyphenated_name(self):
        return self.name.replace(' ', '-')
