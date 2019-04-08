#!/usr/bin/python3
import jinja2
import sys
import os
import shutil
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
        print("generating posts.")
        for post in self.posts:
            post.set_output_dir(posts_dir_path)
            post_file = post.post_file()
            post_dir = os.path.join(post.posts_output_dir, post.hyphenated_title())
            print(post.origin_dir, "->", post_dir)
            print("copy media: ")
            post_media_origin_dir = os.path.join(post.origin_dir, "media")
            post_media_dest_dir = os.path.join(post_dir, "media")
            print(post_media_origin_dir, "->", post_media_dest_dir)
            if os.path.exists(post_media_dest_dir):
                shutil.rmtree(post_media_dest_dir)
            shutil.copytree(post_media_origin_dir, post_media_dest_dir)
            if not os.path.exists(post_dir):
                os.mkdir(post_dir)
            open(post_file, 'w').write(self.render_template("post.html", {"post": post}))

        print("generating blog.")
        open(blog_path, 'w').write(self.render_template("blog.html"))

if __name__ == "__main__":
    print("initializing...")
    generator = Generator(sys.argv[1], sys.argv[2], sys.argv[3])
    print("rendering blog.")
    generator.render_blog("blog.html", "posts")
    print("rendering index.")
    generator.render_index("index.html")
    print("done.")
