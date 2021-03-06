# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
import Logdatabase
import ConfigParser
import functools
import logging
import globalvar
import traceback
class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        ft = self.font()
        
        self.seetings = QtCore.QSettings('LogcatViewer', 'Borqs')
        
        self.savefile = self.seetings.value('SaveFile').toString()
        self.customfilterstr = self.seetings.value('CustomFilterStr',QtCore.QVariant('where detail LIKE \'%AT[%\'')).toString()
        self.findfilterstr = self.seetings.value('FindFilterStr',QtCore.QVariant('AT')).toString()
                

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.custorstr='where detail LIKE \'%AT[%\''
        
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.sourceWidget = QtGui.QTextEdit()
        self.sourceWidget.setFont(font)        
  
        self.setCentralWidget(self.sourceWidget)
       
        self.createActions()
        self.createMenus()
        
        self.createToolBars()
        self.createStatusBar()
        
        self.setWindowTitle("LogCat Viewer")
        self.resize(800, 600)

        self.db = Logdatabase.LogModels()
        
    def InitSourceWidget(self):
        pass
#        labels = QtCore.QStringList()
#logtime,info,,type,component,detail        
#        labels << self.tr("logtime") << self.tr("type") << self.tr("component")<<self.tr("detail")
#        self.sourceWidget.setHeaderLabels(labels)
        #self.sourceWidget.autoRefresh = True
        #self.setSourceModel()
        #self.sourceWidget.setModel(self.model)
        
    def setSourceModel(self,str):
        #first remove the old model
        self.sourceWidget.clear()
        
        #rows = self.model.rowCount()
        #self.model.removeRows(0,rows)
        pattern_str = 'SELECT * from logtable  ' + str
        globalvar.logcatlogging.debug('your sql is %s'%(pattern_str))        
        self.alllog = self.db.execute(pattern_str)
        self.rec_index=0
        self.alllog.reverse()
        for item in self.alllog:
            self.addItem(item)
            self.rec_index = self.rec_index + 1
        self.statusBar().showMessage(self.tr("Filter: %s . Total %d rows"%(pattern_str,self.rec_index)))     
        #self.sourceWidget.setModel(self.model)
        #ft = self.font()
    def addItem(self,item):


        item_str=[0,1,2,4,5,6,7,9]
        
        for i in range(1,6):
            item_str[i] = item[i]
            if(type(item[i]) != type(u'fdsa')):
                    item_str[i] = "%s"%(item[i])
#                    item[i] = str(item[i])
        insert_str = '[' + item_str[1] + ' '+ item_str[2] + item_str[3] +'/' +  item_str[4] + ']\n' + item_str[5]
          
        self.sourceWidget.append(insert_str)
 
         
    def createActions(self):
        self.openAct = QtGui.QAction(self.tr("&Open..."), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.openAct.setStatusTip(self.tr("Open a log file"))
        self.connect(self.openAct, QtCore.SIGNAL("triggered()"), self.open)


        self.saveAct = QtGui.QAction(self.tr("&Save..."), self)
        self.saveAct.setShortcut(self.tr("Ctrl+S"))
        self.saveAct.setStatusTip(self.tr("Save a log file"))
        self.connect(self.saveAct, QtCore.SIGNAL("triggered()"), self.saveAs)
        
        
        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.exitAct.setStatusTip(self.tr("Exit the application"))
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"), 
                     QtGui.qApp.closeAllWindows)
        
        
        #create the filterAct
        self.CustomFilter = QtGui.QAction(self.tr('Custom...'),self)
        self.CustomFilter.setShortcut(self.tr("Ctrl+M"))        
        self.connect(self.CustomFilter,QtCore.SIGNAL("triggered()"),self.CustomFilterClick)
        
        #create the DetailFindAct
        self.DetailFilter = QtGui.QAction(self.tr('Find...'),self)
        self.DetailFilter.setShortcut(self.tr("Ctrl+F"))        
        self.connect(self.DetailFilter,QtCore.SIGNAL("triggered()"),self.DetailFilterClick)

        
        self.filterAct = []
        
        config = ConfigParser.RawConfigParser()
        config.read('filter.ini')
        filter_list = config.options('Filters')
        filter_list.sort()
        for each_item in filter_list:
            tempAct=QtGui.QAction(self.tr(each_item),self)
            self.filterAct.append(tempAct)
            self.connect(tempAct, QtCore.SIGNAL("triggered()"), 
                      functools.partial(self.setSourceModel, config.get('Filters',each_item)))

#        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct.setStatusTip(self.tr("Show the application's About box"))
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtAct.setStatusTip(self.tr("Show the Qt library's About box"))
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"), QtGui.qApp.aboutQt)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.exitAct)
        
        self.menuBar().addSeparator()
        self.filtersMenu = self.menuBar().addMenu(self.tr("F&ilters"))
        self.filtersMenu.addAction(self.DetailFilter)
        self.filtersMenu.addAction(self.CustomFilter)
        self.filtersMenu.addSeparator()

        for item in self.filterAct:
            self.filtersMenu.addAction(item)
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,"LogCat Viewer Open File",self.savefile)
        if not fileName.isEmpty():
            globalvar.logcatlogging.debug("Open file %s"%(fileName))
            self.setWindowTitle("LogCat Viewer: %s"%(fileName))
            fileName=unicode(fileName)

            self.db.setlogfile(fileName)
            self.setSourceModel('')
            self.seetings.setValue('SaveFile', QtCore.QVariant(fileName))
            self.savefile = fileName


        
    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About LogCatViewer"),
            self.tr("The <b>LogCatViewer</b> is used to view arndord logcat log\n\
             It is designed by borqs harold"))    

    def createToolBars(self):
        self.fileToolBar = self.addToolBar(self.tr("File"))
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        
        self.fileToolBar.addAction(self.exitAct)

        self.filtersToolBar = self.addToolBar(self.tr("Filter"))
        self.filtersToolBar.addAction(self.DetailFilter)
        self.filtersToolBar.addAction(self.CustomFilter)

        for item in self.filterAct:
            self.filtersToolBar.addAction(item) 


    def createStatusBar(self):
        self.statusBar().showMessage(self.tr("Ready"))
        
            
    def DetailFilterClick(self):
        text, ok = QtGui.QInputDialog.getText(self, self.tr("Input your filter"),
                                self.tr("Filter:"), QtGui.QLineEdit.Normal,
                                self.findfilterstr)
        
        condition = str(text)
        globalvar.logcatlogging.debug("your condition %s"%(condition)) 
        if ok and not text.isEmpty():
            self.findfilterstr = condition
            condition = 'where detail LIKE \'%%%s%%\''%(condition)
            self.setSourceModel(condition)
            self.seetings.setValue('FindFilterStr', QtCore.QVariant(self.findfilterstr))
 
    def CustomFilterClick(self):
        text, ok = QtGui.QInputDialog.getText(self, self.tr("Input your filter"),
                                self.tr("Filter:"), QtGui.QLineEdit.Normal,
                                self.customfilterstr)
        
        condition = str(text)
        globalvar.logcatlogging.debug("your condition %s"%(condition))
        if ok and not text.isEmpty():
            self.setSourceModel(condition)
            self.customfilterstr = condition
            self.seetings.setValue('CustomFilterStr', QtCore.QVariant(self.customfilterstr))


    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,"LogCat Viewer Open File",self.savefile)
        if fileName.isEmpty():
            return False
              
        self.saveFile(fileName)
        
    def saveFile(self, fileName):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        file = open(fileName,'w')
        for item in self.alllog:
#            print item
            str_item5 = str(repr(item[5]))
            str_item5 = str_item5[2:-1]
            file.write("%s %s %s/%s %s \n"%(str(item[1]),str(item[2]),str(item[3]),str(item[4]),str_item5))
        QtGui.QApplication.restoreOverrideCursor()
        
        #self.savefile = self.seetings.value('SaveFile').toString()
        self.seetings.setValue('SaveFile', QtCore.QVariant(fileName))
        self.savefile = fileName

        self.statusBar().showMessage(self.tr("File saved"), 2000)
        return True               

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s  %(levelname)-8s %(message)s',
                    filename="logcatviewer.log",
                    datefmt="%m-%d %H:%M:%S",        
                    filemode='a')
console=logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

globalvar.logcatlogging = logging.getLogger('Viewer')
                           
app = QtGui.QApplication(sys.argv)
window = Window()
window.InitSourceWidget()
    #window.setSourceModel()
try:    
    window.show()
    sys.exit(app.exec_())
except:
    exption_str=traceback.format_exc()
    globalvar.logcatlogging.error( "Unexpected error:\n %s ",exption_str )
    sys.exit(0)        
                
        
        