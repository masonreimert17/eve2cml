from os import walk, remove

import threading
import time
from datetime import datetime
from FileMetadataDB import FileMetadataDB
class FileWatcherDaemon(threading.Thread):
    # def __init__(self):
    #     super(FileWatcherDaemon,self).__init__()
    #     self.__stop_event=threading.Event()
        
    def run(self):
        self.startWatcherLoop()
    
    def startWatcherLoop(self):
        print('Starting File Watcher Daemon')
        db = FileMetadataDB()
        while True:
            now = datetime.now().timestamp()
            print('Watching Cycle: ',now)
            f = []
            for (dirpath, dirnames, filenames) in walk('./static'):
                f.extend(filenames)
                break
            for file in f:
                res = db.search_file_metadata(file)
                if res:
                    if res[0][1] + 10 < now:
                        remove('./static/'+file)
                else:
                    print("Removed, file not in DB: ",file)
                    remove('./static/'+file)
            
            
            
            time.sleep(10)