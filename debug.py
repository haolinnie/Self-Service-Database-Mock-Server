from api import create_app

if __name__ == "__main__":  # pragma: no cover
    config = {
        "test": False,
        "host": "localhost",
        "username": "test_user",
        "password": "password",
        "db_name": "ssd_sample_database",
    }
    app = create_app(**config)
    app.run(debug=True, port=5100)
