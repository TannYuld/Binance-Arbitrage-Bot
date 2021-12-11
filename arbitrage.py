from types import TracebackType
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import showbase
import config, data
import sys, time, os
import subprocess as sp
import pywintypes
from win10toast import ToastNotifier
from threading import Thread
from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QMenu, QWidget
from PyQt5.QtGui import QIcon

toolTipMessage = 'Arbitrage Catcher\nCreatd By TannYuld\n(Alpha 0.7)\nStatus:'
global isLoopOpen
isLoopOpen = False

def dataLoop():
    binanceVal = data.getDataFromBinance(config.BINANCE_API,config.BINANCE_SECRET,config.BINANCE_COIN)
    bankVal = data.getDataFromBank(config.BANK_URL,'BUYING')
    finalVal = bankVal - binanceVal
    print('Bankval = %s' %bankVal+'  Binanceval = %s' %binanceVal+' finalVal = %s' %finalVal)
    if(abs(finalVal) >= config.DIFFRENCE_RATE):
        global isLoopOpen
        global switchAction
        isLoopOpen = False
        switchAction.setText('Open Catching')
        switchAction.setIcon(QtGui.QIcon('Src/start.png'))
        global trayIcon
        trayIcon.setToolTip(toolTipMessage+'closed')
        print('You can make arbitrage !')
        notify("Arbitrage Catcher","There is a arbitrage chance HURRY!!!\nBank Value: %s" %bankVal+"\nBinance Value: %s" %binanceVal+"\nDiffrent: %s"%finalVal)

def threadLoop():
    while True:
        if(isLoopOpen):
            dataLoop()
        time.sleep(clamp(config.DELAY_TIME,10,60))

def clamp(value,minVal,maxVal):
    if(value < minVal):
        return minVal
    elif(value > maxVal):
        return maxVal
    else:
        return value

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self,icon,parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self,icon,parent)
        self.setToolTip(toolTipMessage+'closed')
        menu = QtWidgets.QMenu(parent)

        openConfig = menu.addAction('Open Config File')
        openConfig.triggered.connect(self.openConf)
        openConfig.setIcon(QtGui.QIcon('Src/config.png'))

        global switchAction
        switchAction = menu.addAction('Open Catching')
        switchAction.triggered.connect(self.switchFunc)
        switchAction.setIcon(QtGui.QIcon('Src/start.png'))

        quitAction = menu.addAction('Quit Program')
        quitAction.triggered.connect(self.quitProgram)
        quitAction.setIcon(QtGui.QIcon('Src/quit.png'))
        #menu.addSeparator()

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActive)
    
    def changeToolTip(self):
        self.setToolTip(toolTipMessage+'closed')

    def switchFunc(self,reason):
        global isLoopOpen
        global switchAction

        if isLoopOpen:
            isLoopOpen = False
            self.setToolTip(toolTipMessage+'closed')
            switchAction.setText('Open Catching')
            switchAction.setIcon(QtGui.QIcon('Src/start.png'))
            notify('Arbitrage Catcher','Background arbitrage shearching closed !')
            #toaster1 = ToastNotifier()
            #toaster1.show_toast("Arbitrage Catcher","Background #arbitrage shearching closed !","Src/coin128.ico")
        else:
            isLoopOpen = True
            self.setToolTip(toolTipMessage+'opened')
            switchAction.setText('Close Catching')
            switchAction.setIcon(QtGui.QIcon('Src/pause.png'))
            #toaster2 = ToastNotifier()
            #toaster2.show_toast("Arbitrage Catcher","Background #arbitrage shearching opened !","Src/coin128.ico")
            notify('Arbitrage Catcher','Background arbitrage shearching opened !')
            
    def openConf(slef,reason):
        notify("Arbitrage Catcher","Don't forget to restart program after save changes in config file !")
        programName = "notepad.exe"
        fileName = "config.py"
        sp.Popen([programName, fileName])

    def quitProgram(self):
        os._exit(os.X_OK)

    def onTrayIconActive(self,reason):
        #print('Tray Icon Opened')
        pass

def notify(message,title):
    toaster = ToastNotifier()
    toaster.show_toast(message,title,'Src/coin128.ico', duration=5,threaded=True)
    del toaster

    
def main():
    #global toaster
    #toaster.show_toast("Arbitrage Catcher","Welcom to Arbitrage #Cather (Alpha 0.7) this program creatd by TannYuld. Program #currently working on background.","Src/coin128.ico",#duration=10,threaded=True)
    #del toaster
    notify("Arbitrage Catcher","Welcom to Arbitrage Cather (Alpha 0.7) this program creatd by TannYuld. Program currently working on background.")
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    global trayIcon
    trayIcon = SystemTrayIcon(QtGui.QIcon("Src/coin.png"),w)
    trayIcon.show()
    sys.exit(app.exec_())

mainLoop = Thread(target=threadLoop, args=())
mainLoop.start()

if __name__=='__main__':
    main()