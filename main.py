from functions import *
from log import *
from conf import *


wait_time=int(config['programconfig']['checktimemins'])*60
heart_time=int(config['programconfig']['heartbeatmins'])*60
websiteurl=config['urls']['siteurl']

ff_visible=0

if config['programconfig'].getboolean('hide_ff') == False:
    ff_visible=1
    
count_time = 0

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
    count_time=wait_time+count_time
    if count_time > heart_time:
        logger.info("Heartbeat")
        send_matrix_msg("Eeeeee! This is DownloadHawk. The time is " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        count_time = 0
    else:
        logger.info("No Heartbeat")