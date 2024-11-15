import keke_log as kekelog

try:
    log = kekelog.LogManager('root','log.log')
    addlog = log.addLog
except:
    print('log setup failed!!!')
