from src import app
import os

if __name__ == '__main__':
    port_number = os.getenv('PORT_VALUE', 5000)
    app.run(debug=False, port=int(port_number))
