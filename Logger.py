__author__ = 'leonardoalbuquerque'

import logging

logging.basicConfig(filename='/Users/leonardoalbuquerque/Desktop/example.log',level=logging.DEBUG)

logging.debug("debug on root")

oldLogger = logging.getLogger("oldLogger")

oldLogger.warning("warning")
oldLogger.info("info")
oldLogger.debug("debugging")


newLogger = logging.getLogger("abc")
#newLogger.basicConfig(filename='/Users/leonardoalbuquerque/Desktop/newLogger.log',level=logging.DEBUG)
newLogger.debug("debug")


