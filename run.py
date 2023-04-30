from app import create_app

if __name__ == "__main__":
    application = create_app()
    application.run(port=8000)

# https://codersdiaries.com/blog/flask-project-structure