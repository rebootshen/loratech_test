import os

from src.app import create_app

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

if __name__ == '__main__':
  env_name = os.getenv('FLASK_ENV')
  app = create_app(env_name)


  port = os.getenv('PORT')
  # run app

  #import logging
  #logging.basicConfig(filename='error.log',level=logging.DEBUG)

  import logging, logging.config, yaml

  #yaml.load(input, Loader=yaml.FullLoader)
  logging.config.dictConfig(yaml.load(open('logging.yml'), Loader=yaml.FullLoader))


  logfile    = logging.getLogger('file')
  logconsole = logging.getLogger('console')
  logfile.debug("Debug FILE")
  logconsole.debug("Debug CONSOLE")


  # run app
  #app.run()
  #app.run(host='0.0.0.0', port=port)
  app.run(port=port)
