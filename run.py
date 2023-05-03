from app import create_app

application = create_app()
if __name__ == "__main__":
    application.run(port=8000)

# https://codersdiaries.com/blog/flask-project-structure
# https://www.youtube.com/watch?v=IBfj_0Zf2Mo
