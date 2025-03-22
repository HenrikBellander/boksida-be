from app import create_app

app = create_app()

if __name__ == '__main__':
    """Startar Flask-applikationen i debug-läge när denna fil körs direkt."""
    app.run(debug=True)
