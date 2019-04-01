#!/usr/bin/python3
import jinja2
import sys
import os
from project import Project
from post import Post

class Generator:
    # projects: [Project]
    # posts: [Post]

    def __init__(self, projects_dir, posts_dir, templates_dir):
        self.projects = []
        self.posts = []
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_dir))

        projects_subdirs = [os.path.join(projects_dir, f) for f in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, f))]
        for project_dir in projects_subdirs:
            project = Project.load_from_dir(project_dir)
            self.projects.append(project)

        posts_subdirs = [os.path.join(posts_dir, f) for f in os.listdir(posts_dir) if os.path.isdir(os.path.join(posts_dir, f))]
        for post_dir in posts_subdirs:
            post = Post.load_from_dir(post_dir)
            self.posts.append(post)

        self.posts.sort(key=lambda x: x.date, reverse=True)

    def render_template(self, template, other_vars=dict()):
        template = self.env.get_template(template)
        v = {"projects": self.projects, "posts": self.posts}
        return template.render({**v, **other_vars})

    def render_index(self, index_path):
        open(index_path, 'w').write(self.render_template("index.html"))

    def render_blog(self, blog_path, posts_dir_path):
        if not os.path.exists(posts_dir_path):
            os.makedirs(posts_dir_path)
        for post in self.posts:
            post.set_output_dir(posts_dir_path)
            post_file = post.post_file()
            open(post_file, 'w').write(self.render_template("post.html", {"post": post}))

        open(blog_path, 'w').write(self.render_template("blog.html"))

if __name__ == "__main__":
    generator = Generator(sys.argv[1], sys.argv[2], sys.argv[3])
    generator.render_blog("blog.html", "posts")
    generator.render_index("index.html")
