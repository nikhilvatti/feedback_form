from Registration import create_app

app = create_app()

if __name__ == "__main__":
    if app is not None:
        app.run(debug=True)