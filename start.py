import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.abspath(os.path.dirname(curPath) + os.path.sep + ".")
sys.path.append(root_path)
#from user_mode.login import server
#from config import server
from config import SERVER_PORT
from flask_cors import CORS
#from user_mode.tiaoshi import server
#debug=True，修改代码后，不需要重启服务，它会帮你自动重启    #起动服务。8888,
from user_mode.API import server
if __name__ == "__main__":
    CORS(server, supports_credentials=True)
    server.run(port=SERVER_PORT, debug=True, host='0.0.0.0')