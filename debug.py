from ssd_api import create_app

if __name__ == '__main__': # pragma: no cover
    app = create_app()
    app.run(debug=True, port=5200)
