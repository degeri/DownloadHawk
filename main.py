from functions import *
from log import *
from conf import *

wait_time=int(config['programconfig']['checktimemins'])*60
websiteurl=config['urls']['siteurl']

ff_visible=0

if config['programconfig'].getboolean('hide_ff') == False:
    ff_visible=1
    

while True:
    logger.info("Started checks")
    display = Display(visible=ff_visible, size=(800, 600))
    display.start()
    try:
        visiturl(websiteurl)
    except Exception as e:
        logger.exception(e)
    display.stop()
    logger.info("Checks ended")
    time.sleep(wait_time)