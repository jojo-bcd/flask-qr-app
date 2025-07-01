import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Prend le port Render ou 5000 en local
    app.run(host='0.0.0.0', port=port, debug=True)
