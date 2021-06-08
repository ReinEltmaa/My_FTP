# -*- coding: utf-8 -*-
"""
Spyder Editor
Created on Sun Apr 14 20:20:35 2021
@author: reine

"""

import sys, os, stat

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QListWidgetItem
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QColor
 
from PyQt5.QtWidgets import QMessageBox

# import traceback
import shutil, time, datetime
from ftplib import FTP

# import glob for directory copy 
#from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QButtonGroup


remote_list_lines = []
remote_nlst_lines = []

Left_nlst_lines = []
Left_list_lines = []
Right_nlst_lines = []
Right_list_lines = []

Left_Dir_Rows = []
Left_File_Rows = []
Right_Dir_Rows = []
Right_File_Rows = []
dir_list = []
dir_list_Rows = 0

RemoteOn = False

Left_DirList_RowOn = -1
Right_DirList_RowOn = -1
DeleteButtonOn = -1
CopyButtonOn = -1
OpenButtonOn = -1
SENDButtonOn = -1
RETRButtonOn = -1
MakeDirButtonOn = -1
CDUPButtonOn = -1
AttrsButtonOn = -1

servers_lines = []

Local_Home = ""
Remote_Home = ".\\"


#lines = []


def get_Local_Attrs(self, Name, Mode):
    msg = "--- I'm at on_Local_Attrs ---"   
    debug(self, msg)

    if Mode == "Left":
       parent = self.Left_Path.toPlainText()
    else:
       parent = self.Right_Path.toPlainText()
                
    path = os.path.join(parent, Name)
#    path = "C:/Program Files\\WindowsApps"
    status = os.stat(path)

    statinfo = os.stat(path)
    print("statinfo: " + str(statinfo))
    
    prm = stat.filemode(status.st_mode)  
    attrs = prm
    
    nlink = statinfo.st_nlink
    attrs += ' ' + str(nlink)

    uid = statinfo.st_uid
    nuid = str(uid)
    attrs += " User" + nuid

    gid = statinfo.st_gid
    ngid = str(gid)
    attrs += " Group" + ngid

    size = statinfo.st_size
    nsize = str(size)
    attrs += ' ' + nsize
    
    mtime = statinfo.st_mtime
    timestamp_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d-%H:%M')
    attrs += ' ' + timestamp_str

#    print("Attrs line: " + attrs) 

    return attrs
         
#    ln = len("-rwx------ 1 user group            151 May 24 14:33 dir.png")
#    lv = len("12345678901234567890123456789012345678901234567890123456789")     
#    lg = len("          ! !    !     !              !   !  !     !       ")
#    lo = len("         11 13   18    24             39  43 46    52      ")
#    lp = len("    -10   .1. -4-. -5- .    -14-      .-3-.-3-. -5-.len-52 ")
# ect ???    
        
    return



def Fake_Click(Mode):
    global Left_DirList_RowOn
    global Right_DirList_RowOn
    global DeleteButtonOn
    global CopyButtonOn
    global OpenButtonOn
    global SENDButtonOn
    global RETRButtonOn
    global MakeDirButtonOn
    global CDUPButtonOn
    global AttrsButtonOn
    
    if Mode == "Delete":
        pass
    else:
        DeleteButtonOn = -1
     
    if Mode == "Copy":
        pass
    else:        
        CopyButtonOn = -1

    if Mode == "Open":
        pass
    else:    
        OpenButtonOn = -1

    if Mode == "SEND":
        pass
    else:    
        SENDButtonOn = -1

    if Mode == "RETR":
        pass
    else:    
        RETRButtonOn = -1

    if Mode == "MakeDir":
        pass
    else:    
        MakeDirButtonOn = -1

    if Mode == "CDUP":
        pass
    else:    
        CDUPButtonOn = -1

    if Mode == "Attrs":
        pass
    else:    
        AttrsButtonOn = -1

    if Mode == "Left":
        pass
    else:    
         Left_DirList_RowOn = -1
                
    if Mode == "Right":
       pass
    else:
        Right_DirList_RowOn = -1
        
    return
    
            
def set_ButtonGroup(self):
    self.bg1 = QButtonGroup(self)
    self.bg1.addButton(self.LeftOn)
    self.bg1.addButton(self.RightOn)
    
    self.RightOn.setChecked(True)
    return


def debug(self, line):
        
    c = line[0:1] 
    if c == 'U' or c == 'E' or c == 'T':
        item = QListWidgetItem(line)
        item.setForeground(QColor(200,0,0))
        self.LogList.insertItem(0, item)  
        if line[0:6] == 'Error:':
            buttonReply = QMessageBox.question(self, 'PyQt5 message', line + "\n Do You continue ?" , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                return True
            else:
                return False
            
            QMessageBox.show(self)
                        
    if self.check_Msg.checkState() or c == 'M' or c == '?':
        self.LogList.insertItem(0, line)
        return

    if self.check_Trace.checkState() and c == '-':
        self.LogList.insertItem(0, line)        
        return
     
    if self.check_Dbg.checkState() and c == 'D':
        self.LogList.insertItem(0, line)        

    return 

    
def clear_Buttons(self, setOn):
    self.MakeDirButton.setEnabled(setOn) 
    self.CopyButton.setEnabled(setOn)
    self.RenameButton.setEnabled(setOn) 
    self.CDUPButton.setEnabled(setOn)
    self.OpenButton.setEnabled(setOn)
    self.DeleteButton.setEnabled(setOn)
    self.RETRButton.setEnabled(setOn)
    self.SENDButton.setEnabled(setOn)    
    self.AttrsButton.setEnabled(setOn)    
    return 
  

def set_Buttons(self, setOn):
    global RemoteOn
    
    clear_Buttons(self, False)

    attr = self.Attr.text()
    if len(attr) > 0:
        self.AttrsButton.setEnabled(setOn)
        if setOn == False:
            self.Attrs.clear()
            self.FileAttrs.clear()
            self.FileName.clear()
            
    if self.LeftOn.isChecked():
        if RemoteOn:
            self.RETRButton.setEnabled(setOn)
            self.CDUPButton.setEnabled(setOn)
            self.MakeDirButton.setEnabled(setOn) 
            self.RenameButton.setEnabled(setOn) 
        else:
            self.CDUPButton.setEnabled(setOn)
            self.MakeDirButton.setEnabled(setOn) 
            self.CopyButton.setEnabled(setOn)
            self.RenameButton.setEnabled(setOn) 

        self.OpenButton.setEnabled(setOn)
        self.DeleteButton.setEnabled(setOn)

    else:
        if RemoteOn:
            self.SENDButton.setEnabled(setOn)    
        
        self.MakeDirButton.setEnabled(setOn) 
        self.CopyButton.setEnabled(setOn)
        self.RenameButton.setEnabled(setOn) 
        self.CDUPButton.setEnabled(setOn)
        self.OpenButton.setEnabled(setOn)
        self.DeleteButton.setEnabled(setOn)
        

    return

def Make_list_lines(self, path):
    msg = "--- I'm at Make_list_lines ---"
    debug(self, msg)

    list_lines = []
        
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                list_lines.append("drv")
            else:
                list_lines.append("-rw")

    return list_lines



def fill_Left_DirList(self):
    global Left_nlst_lines
    global Left_list_lines
    global Left_Dir_Rows
    global Left_File_Rows
    global Local_Home
    
    msg = "--- I'm at fill_Left_DirList ---"   
    debug(self, msg)
    
    self.Left_DirList.clear()  
    nlst_lines = Left_nlst_lines
    list_lines = Left_list_lines              
    Left_Dir_Rows = []
    Left_File_Rows = []

    ln = 0
    lns = len(nlst_lines)
    while ln < lns:
        name = nlst_lines[ln]
        item = QListWidgetItem(name)
        line = list_lines[ln]
        bcd = line[0:1]
        if bcd =='d':
            Icon_Path = os.path.join(Local_Home, "dir.png")
            icon = QtGui.QPixmap(Icon_Path)            
            Left_Dir_Rows.append(ln)
            if RemoteOn:
                item.setForeground(QColor(200,0,0))
        else:
            Icon_Path = os.path.join(Local_Home, "file.png")
            icon = QtGui.QPixmap(Icon_Path)            
            Left_File_Rows.append(ln)
            if RemoteOn:
                item.setForeground(QColor(0,0,200))
            
        item.setIcon(QtGui.QIcon(icon))
        self.Left_DirList.addItem(item)            
        ln += 1

    return


def fill_Right_DirList(self):
    global Right_nlst_lines
    global Right_list_lines
    global Right_Dir_Rows
    global Right_File_Rows
    global Local_Home
    
    msg = "--- I'm at fill_Right_DirList ---"   
    debug(self, msg)
    
    path = self.Right_Path.toPlainText()
    self.Right_DirList.clear()                     
    nlst_lines = Right_nlst_lines
    list_lines = Right_list_lines          
    Right_Dir_Rows = []
    Right_File_Rows = [] 
    
    ln = 0
    lns = len(nlst_lines)
    while ln < lns:
        name = nlst_lines[ln]
        attrs = list_lines[ln] 
        item = QListWidgetItem(name)
        bc = attrs[0:1] 
        if bc == 'd':
            Icon_Path = os.path.join(Local_Home, "dir.png")
            icon = QtGui.QPixmap(Icon_Path)            
            Right_Dir_Rows.append(ln)
        else:
            Icon_Path = os.path.join(Local_Home, "file.png")
            icon = QtGui.QPixmap(Icon_Path)            
            Right_File_Rows.append(ln)
 
        item.setIcon(QtGui.QIcon(icon))
        self.Right_DirList.addItem(item)            
        ln += 1
        
    Right_list_lines = list_lines
    Right_nlst_lines = nlst_lines
    
    return
            
def read_Server_DirList(self, Mode):
    global Left_nlst_lines
    global Left_list_lines

    msg = "--- I'm at read_Server_DirList ---"   
    debug(self, msg)
        
    Left_nlst_lines = []
    Left_list_lines = []
    
    try:
        parent = self.ftp.pwd()
    except Exception as e: 
        errno = str(e)
        if errno[0:3] != "550":
           msg = "Msg: " + errno
           debug(self, msg)
        else:
           msg = "Error: " + errno
           debug(self, msg)

    path =  self.Left_Path.toPlainText() 
    if parent != path:
        self.Left_Path.clear()        
        self.Left_Path.insertPlainText(parent)
        
    try:
        self.ftp.retrlines('NLST', Left_nlst_lines.append)
    except Exception as e: 
        errno = str(e)
        msg = "Error: " + errno + "\n user's home dir d'nt exist on Server"
        if debug(self, msg):
            DisConnect(self)
            return
        else:
            self.close()
            return
    try:
        self.ftp.retrlines('LIST', Left_list_lines.append)
    except Exception as e: 
        errno = str(e)
        msg = "Msg: " + errno
        debug(self, msg)
        return
    
    fill_Left_DirList(self)
    
    return


def open_File(self, Mode):
    msg = "--- I'm at open_File ---"   
    debug(self, msg)
       
    name = self.FileName.text()
    
    if Mode[0] == 'L':
        parent = self.Left_Path.toPlainText()
    else:    
        parent = self.Right_Path.toPlainText()
    lines = []
    path = os.path.join(parent, name)
    filename, ext = os.path.splitext(path)         
    if ext == '.txt' or ext == '.log' or ext == ".py" or ext == '.ui':
        fp = open(path, 'rt')
        lines = fp.readlines()
        ln = len(lines)
        self.LogList.clear()
        line = "file: " + path + " lines "  
        self.LogList.addItem(line)

        li = 0
        while li < ln:
            line = lines[li]
            self.LogList.addItem(line)
            li += 1
        fp.close()    
        
    return


def read_Left_Local_DirList(self, Mode):
    global Left_nlst_lines
    global Left_list_lines
    global RemoteOn

    msg = "--- I'm at read_Local_Left_DirList ---"   
    debug(self, msg)
                
    Left_list_lines = []
    Left_nlst_lines = []

    parent = self.Left_Path.toPlainText()
    name = self.FileName.text()
    
    if Mode == "Open":    
        path = os.path.join(parent, name)
    else:
        path = parent
          
    self.Left_DirList.clear()

    try:
        Left_nlst_lines = os.listdir(path)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)
        
    Left_list_lines = Make_list_lines(self, path)
    
    fill_Left_DirList(self)
    self.Left_Path.clear()
    self.Left_Path.insertPlainText(path)
    return


def read_Right_Local_DirList(self, Mode):
    global Right_nlst_lines
    global Right_list_lines

    msg = "--- I'm at read_Right_DirList ---"   
    debug(self, msg)
   
    Parent = self.Right_Path.toPlainText()
    name = self.FileName.text()
            
    if Mode == "Open":    
        path = os.path.join(Parent, name)
    else:
        path = Parent

    try:
        Right_nlst_lines = os.listdir(path)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)

    Right_list_lines = Make_list_lines(self, path)

    fill_Right_DirList(self)
    self.Right_Path.clear()
    self.Right_Path.insertPlainText(path)
    return
    

def unpack_line(self, line):
    global lc
    global c
    
    msg = "--- I'm at unpack_line ---"   
    debug(self, msg)
    
    ls = len(line)
    name = ""
    ip = ""
    port = ""
    user = ""
    passw = ""
    
    lc = 0
    c = ""
    
    while lc < ls:
        c = line[lc]
        if c != ',':
            name += c
            lc += 1
        else:
            break
        
    lc += 1        
    while lc < ls:
        c = line[lc]
        if c != ',':
            ip += c
            lc += 1
        else:
            break

    lc += 1       
    while lc < ls:
        c = line[lc]
        if c != ',':
            port += c
            lc += 1
        else:
            break

    lc += 1
    while lc < ls:
        c = line[lc]
        if c != ',':
            user += c
            lc += 1
        else:
            break

    lc += 1
    while lc < ls:
        c = line[lc]
        if c != ',':
            passw += c
            lc += 1
        else:
            break

    return name, ip, port, user, passw


def get_name(self, line):
    
    msg = "--- I'm at get_name ---"   
    debug(self, msg)

    ls = len(line)
    name = ""
    lc = 0
    c = ''
    
    while lc < ls:
        c = line[lc]
        if c == ',':
            name = line[0:lc]
            return name
        else:
            lc += 1


def Left_DirList_clicked(self):
    global RemoteOn
    global Left_list_lines
    global Left_nlst_lines

    msg = "--- I'm at Left_DirList_clicked ---"   
    debug(self, msg)
       
    row =self.Left_DirList.currentRow()       
    list_line = Left_list_lines[row]
    name = Left_nlst_lines[row]
    attr = list_line[0]
    if attr == 'd':
        self.Attr.setText("dir")
    else:
        self.Attr.setText("file")
    
    set_Buttons(self, True)
    self.FileName.setText(name)
    return


def Right_DirList_clicked(self):
    global RemoteOn
    global Right_list_lines
    global Right_nlst_lines

    msg = "--- I'm at Right_DirList_clicked ---"   
    debug(self, msg)
         
    row = self.Right_DirList.currentRow()       
    list_line = Right_list_lines[row]
    name = Right_nlst_lines[row]
    attr = list_line[0]
    if attr == 'd':
        self.Attr.setText("dir")
    else:
        self.Attr.setText("file")

    set_Buttons(self, True)
    self.FileName.setText(name)
    return




def sync_Lists(self):
    global Left_nlst_lines
    global Right_nlst_lines
    global Right_list_lines
    global Left_list_lines

    msg = "--- I'm at sync_Lists ---"   
    debug(self, msg)

    left = self.Left_Path.toPlainText()
    right = self.Right_Path.toPlainText()

    if left == right:
        if self.LeftOn.isChecked():
            Right_nlst_lines = Left_nlst_lines
            Right_list_lines = Left_list_lines
            fill_Right_DirList(self)
        else:
            Left_nlst_lines = Right_nlst_lines
            Left_list_lines = Right_list_lines
            fill_Left_DirList(self)
        return True
    
    else:
        return False 




def CDUP_on_Server(self):
    msg = "--- I'm CUPD on Server ---"
    debug(self, msg)

    path = self.Left_Path.toPlainText()
    ln =len(path)
    if ln > 1:
        try:
            self.ftp.cwd("..")
        except Exception as e: 
            msg = "Error: " + str(e)
            debug(self, msg)
        else:
            try:
                parent = self.ftp.pwd()
            except Exception as e: 
                msg = "Error: " + str(e)
                debug(self, msg)
            else:        
                self.Left_Path.clear()
                self.Left_Path.insertPlainText(parent)
#                check_slash(self, True)
                read_Server_DirList(self, "CDUP")

    Fake_Click("CDUP")
    
    return


def Delete_on_Server(self, name, attr):
    msg = "--- I'm at on_Delete_on_Server ---"   
    debug(self, msg)
    
    c = attr[0:1]
    if c == 'd':
        try:
            self.ftp.rmd(name)
        except Exception as e: 
            msg = "Error: " + str(e)
            if debug(self, msg):
                pass
            else:
                self.close()
    
    else:
        try:
            self.ftp.delete(name)
        except Exception as e: 
            msg = "Error: " + str(e)
            if debug(self, msg):
                pass
            else:
                self.close()

    read_Server_DirList(self, "DELETE")
    
    self.Attr.clear()
    self.FileName.clear()
#    sync_Lists(self)
    self.Attr.clear()    
    Fake_Click("Delete")
    return


def Open_Dir_on_Server(self):
    global Left_list_lines
    global Left_nlst_lines
        
    msg = "--- I'm at Open_on_Server ---"
    debug(self, msg)

    row =self.Left_DirList.currentRow() 
    name = Left_nlst_lines[row]
    list_line = Left_list_lines[row]
    attr = list_line[0:1]

#    self.FileName.clear() 
#    self.FileName.setText(name)

    if attr == 'd':
        parent = self.Left_Path.toPlainText()
        path = os.path.join(parent, name)

        try:
            self.ftp.cwd(path)
        except Exception as e: 
            msg = "Error: " + str(e)
            debug(self, msg)
        
        self.Left_Path.clear()
        self.Left_Path.insertPlainText(path)
        read_Server_DirList(self, "Open")
                
    self.Attr.clear()
    self.FileName.clear()
#    sync_Lists(self)
    Fake_Click("Open")
    return    


        

def Local_Copy(self):
    msg = "--- I'm at on_Local_Copy ---"   
    debug(self, msg)

    if self.LeftOn.isChecked():
        msg = "--- I'm at on_Copy_clicked from Left_DirList ---"   
        debug(self, msg)

        fromDir= self.Left_Path.toPlainText()
        toDir = self.Right_Path.toPlainText() 

    else: 
        msg = "--- I'm at on_Copy_clicked from Right_DirList ---"   
        debug(self, msg)
 
        fromDir= self.Right_Path.toPlainText()
        toDir = self.Left_Path.toPlainText() 

    typ = self.Attr.text()
    name =self.FileName.text()
    srcPath = os.path.join(fromDir, name)
    dsc = typ[0]
    if dsc == 'd':
        dstPath = os.path.join(toDir, name)
        shutil.copytree(srcPath, dstPath) 
    else:
        shutil.copy(srcPath, toDir) 
             
    if self.LeftOn.isChecked():
        read_Right_Local_DirList(self, "Copy")           
    else:
        read_Left_Local_DirList(self, "Copy")

    self.FileName.clear()
    self.Attr.clear()
    return



def Connect(self):
    global RemoteOn
    global remote_list_lines
    global remote_nlst_lines
    global Left_nlst_lines
    global Left_list_lines
    global Remote_Home
    
    msg = "--- I'm at Connect ---"   
    debug(self, msg)
        
    name = self.serverName.text()
        
    if RemoteOn:
        RemoteOn = False
        self.ftp.quit()
        time.sleep(2)
        msg = "Msg: Reconnecting FTP Server " + name + " ..." 
        debug(self, msg)
    else:
        msg = "Msg: Connecting FTP Server " + name + " ..."   
        debug(self, msg)
                     
    host_addr = self.ipAddr.text()
    
    try:
        self.ftp = FTP(host_addr)
    except Exception as e: 
        msg = "Error: " + str(e)
        if debug(self, msg):
            return
        else:
            self.close() 
            return
        
    self.Left_Label.setText("S e r v e r   DirList")
    self.Left_Check_Label.setText("Server")
    self.Left_DirList.clear()

    debug(self, "Msg: " + str(self.ftp))
    user_name = self.userName.text()   
    user_passw = self.userPassw.text()
    try:
        self.ftp.login(user_name, user_passw)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)
        return
                
    msg = "Msg: user name=" + user_name + " user passw = " + user_passw
    debug(self, msg)
    welcomeMessage = self.ftp.getwelcome()
    debug(self, "Msg: " + welcomeMessage)

    try:
        path = self.ftp.pwd()
    except Exception as e: 
        msg = "Error: " + str(e)
        if debug(self, msg):
            return
        else:
            self.close() 
            return

    Remote_Home = path
    
    self.Left_Path.clear()
    self.Left_Path.insertPlainText(path) 
    RemoteOn = True
    self.connectButton.setText("ReConnect")
    read_Server_DirList(self, "Connect") 
        
    self.disConnectButton.setEnabled(True)
    self.LeftOn.setChecked(True)

    set_Buttons(self, True) 
    Fake_Click("Connect")
    return


def DisConnect(self):
    global RemoteOn
    global Left_nlst_lines
    global Left_list_lines
        
    if RemoteOn:
        try:
            self.ftp.quit()
        except Exception as e: 
            msg = "Error: " + str(e)
            if debug(self, msg):
                debug(self, "Msg: FTP_Client disconnected")
                pass
            else:
                self.close() 
                return
                
    RemoteOn = False
         
    self.connectButton.setText("Connect")
    path = self.Right_Path.toPlainText()
    
    try:
        Left_nlst_lines = os.listdir(path)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)
        return
    
    self.Left_Label.setText("Left  L o c a l   DirList")
    self.Left_Check_Label.setText("  Left")
    self.Left_Path.clear()
    self.Left_Path.insertPlainText(path)
        
    read_Left_Local_DirList(self, "DisConnect")
    self.RightOn.setChecked(True)
        
    set_Buttons(self, True) 
    Fake_Click("DisConnect")    
    return


def Rename_on_Local(self, old_name, new_name):
    msg = "--- I'm at Rename_on_Local ---"
    debug(self, msg)
    
    if self.LeftOn.isChecked():
        parent = self.Left_Path.toPlainText()
    else:
        parent = self.Right_Path.toPlainText()
        
    old_path = os.path.join(parent, old_name)
    new_path = os.path.join(parent, new_name)    
   
    try:
        os.rename(old_path, new_path)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)
        
    if self.LeftOn.isChecked():
        read_Left_Local_DirList(self, "Rename") 
    else:
        read_Right_Local_DirList(self, "Rename")
        
    self.Attr.clear()
    self.FileName.clear()
    sync_Lists(self)
    Fake_Click("Rename")
    return    


def Rename_on_Server(self, old_name, new_name):
    msg = "--- I'm at Rename_on_Server ---"
    debug(self, msg)

    try:
        self.ftp.rename(old_name, new_name)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)
        
    read_Server_DirList(self, "Rename")
                
    self.Attr.clear()
    self.FileName.clear()
#    sync_Lists(self)
    Fake_Click("MakeDir")
    return    


def Make_Dir_on_Local(self, name):        
    msg = "--- I'm at Make_Dir_on_Local ---"
    debug(self, msg)
    
    if self.LeftOn.isChecked():
        parent = self.Left_Path.toPlainText()
        path = os.path.join(parent, name) 
        try:
            os.mkdir(path) 
        except Exception as e: 
            msg = "Error: " + str(e)
            if debug(self, msg):
                return
            else:
                self.close()
                return
            
        read_Left_Local_DirList(self, "Make") 
               
    else: 
        parent = self.Right_Path.toPlainText()
        path = os.path.join(parent, name) 
        try:
            os.mkdir(path) 
        except Exception as e: 
            msg = "Error: " + str(e)
            if debug(self, msg):
                return
            else:
                self.close()
                return

        read_Right_Local_DirList(self, "Make") 

    return




def SEND_file(self, name):
    msg = "--- I'm at SEND_file ---"   
    debug(self, msg)
    
    dr = self.Right_Path.toPlainText()
    fe = os.path.join(dr, name)
    fpd = open(fe, "rb");
 
    msg = "Msg: STOR file " + name
    debug(self, msg)

    try:
        self.ftp.storbinary("STOR " + name, fp=fpd)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)

    read_Server_DirList(self, "SEND")
    self.FileName.clear()
    self.Attr.clear()  
    Fake_Click("SEND")
    return


def Make_Dir_on_Server(self, name):        
    msg = "--- I'm at Make_Dir_on_Server ---"
    debug(self, msg)

    parent = self.Left_Path.toPlainText()
    path = os.path.join(parent, name)

    try:
        self.ftp.mkd(path)
    except Exception as e: 
        msg = "Error: " + str(e)
        if debug(self, msg):
            return
        else:
            self.close()
            return
       
    read_Server_DirList(self, "MakeDir")
                
    self.Attr.clear()
    self.FileName.clear()
#    sync_Lists(self)
    Fake_Click("MakeDir")
    return    

   
def SEND_tree(self, row, path):
    global dir_list

    for x in os.listdir(path):
        frf = os.path.join(path, x)
        if os.path.isdir(frf):
            Make_Dir_on_Server(self, x)                
            dir_list.append(frf)

        else:
            SEND_file(self, x)
            time.sleep(0.2)
            
    rows = len(dir_list)
    while row < rows:
        path = dir_list[row]
        name = os.path.basename(path)
        self.ftp.cwd(name)
        row += 1
        SEND_tree(self, row, path)
    
    return


def SEND_dir(self, name):
    global dir_list   
    
    msg = "--- I'm at SEND_dir ---"   
    debug(self, msg)

    dir_list = []
    
    Make_Dir_on_Server(self, name)
    self.ftp.cwd(name)
#    server = self.ftp.pwd()
    local = self.Right_Path.toPlainText()
    local = os.path.join(local, name)
    self.Right_Path.clear()
    self.Right_Path.insertPlainText(local)
    SEND_tree(self, 0, local)
    
    read_Server_DirList(self, "SEND")
    self.FileName.clear()
#    sync_Lists(self)
    self.Attr.clear()    
    Fake_Click("SEND")
    return


def RETR_file(self, name):
    msg = "--- I'm at RETR_file ---"   
    debug(self, msg)
    
    msg = "Msg: RETR file: " + name
    debug(self, msg)
    
    parent = self.Right_Path.toPlainText()
    path = os.path.join(parent, name)
    
    try:
        fp = open(path, 'wb')
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)

    try:    
        self.ftp.retrbinary('RETR ' + name, fp.write)
    except Exception as e: 
        msg = "Error: " + str(e)
        debug(self, msg)
   
    fp.close()

    read_Right_Local_DirList(self, "RETR")
    self.FileName.clear()
#    sync_Lists(self)
    self.Attr.clear()    
    Fake_Click("RETR")
    return

def retrlines(self):
    global Left_nlst_lines
    global Left_list_lines
    
    Left_list_lines = []
    Left_nlst_lines = []
    
    try:
        self.ftp.retrlines('NLST', Left_nlst_lines.append)
    except Exception as e: 
        errno = str(e)
        msg = "Error: " + errno + "\n user's home dir d'nt exist on Server"
        DisConnect(self)
        yes = debug(self, msg)
        if yes:
            return False
        else:
            self.close()
            return
        
    try:
        self.ftp.retrlines('LIST', Left_list_lines.append)
    except Exception as e: 
        errno = str(e)
        msg = "Msg: " + errno
        DisConnect(self)
        yes = debug(self, msg)
        if yes:
            return False
        else:
            self.close()
            return

    return True
 

def RETR_tree(self, row, path):
    global dir_list
    global Left_list_lines
    global Left_nlst_lines
    global dir_list_Rows
   
#    pth = os.getcwd()
    pths = self.ftp.pwd()
    
    ln = 0
    lnw = len(Left_nlst_lines)
    while ln < lnw:
        name = Left_nlst_lines[ln]
        lpth = os.path.join(path, name)
        prm = Left_list_lines[ln]
        prc = prm[0:1]
        if prc == 'd':
            pld = pths + '\\' + name
            dir_list.append(pld)
            pld = path + '\\' + name
            dir_list.append(pld)

        else:
            try:
                fp = open(lpth, 'wb')
            except Exception as e: 
                msg = "Error: " + str(e)
                if debug(self, msg):
                    return False  
                else:
                    self.close()
                    return

            try:    
                self.ftp.retrbinary('RETR ' + name, fp.write)
            except Exception as e: 
                msg = "Error: " + str(e)
                if debug(self, msg):
                    return False  
                else:
                    self.close()
                    return
   
            fp.close()  
            
        ln += 1
        
    rows = len(dir_list)
#    if  rows > dir_list_Rows:
#        os.chdir("..")
#        path = os.getcwd()
#        self.ftp.cwd("..")
    
    while row < rows:
        name = dir_list[row]
        row += 1
        subdir = dir_list[row]
        row += 1
        dir_list_Rows = rows
        
        if os.path.isdir(subdir) == False:
            try:
                os.mkdir(subdir)
#            os.chdir(subdir)
            except Exception as e: 
                errno = str(e)
                msg = "Error: " + errno + "\n c'nt change Local dir " + name
                yes = debug(self, msg)
                msg = "Debug: Row:" + str(row-2) + " " + str(dir_list) 
                print(msg)
                if yes:
                    return False
                else:
                    self.close()
                    return
        
        path = subdir
#        pth = self.ftp.pwd()
        
        try:
            self.ftp.cwd(name)
        except Exception as e: 
            errno = str(e)
            msg = "Error: " + errno + "\n c'nt change remote dir " + name
            DisConnect(self)
            yes = debug(self, msg)
            if yes:
                return False
            else:
                self.close()
                return
            
        ok = retrlines(self)
        if ok:
#            row += 1
#            path = os.getcwd()
            ok = RETR_tree(self, row, path)
            if ok == False:
                return False
        else:
            return False

    return True


def RETR_dir(self, name):
    global dir_list   
    global dir_list_Rows    
    
    msg = "--- I'm at RETR_dir ---"   
    debug(self, msg)

    dir_list = []
    
    parent = self.Right_Path.toPlainText()
    path = os.path.join(parent, name)
#    self.Right_Path.clear()
#    self.Right_Path.insertPlainText(path)
    
    if os.path.isdir(path) == False:
        try:
            os.mkdir(path)
        except Exception as e: 
            msg = "Error: " + str(e)
            if debug(self, msg):
                pass
            else:
                self.close()
                return            

#    os.chdir(path)
    self.ftp.cwd(name)
#    name = self.ftp.pwd()
    
    ok = retrlines(self)
    
    if ok:
        dir_lines_Rows = 0
        RETR_tree(self, 0, path)
    
    os.chdir(Local_Home)

    read_Right_Local_DirList(self, "RETR") 
    self.FileName.clear()
#    sync_Lists(self)
    self.Attr.clear()    
    Fake_Click("RETR")
    return




class My_FTP_Client(QtWidgets.QMainWindow):
    def __init__(self):
        super(My_FTP_Client, self).__init__()
        uic.loadUi('My_FTP_Client.ui', self)
        self.connectButton.clicked.connect(self.on_ConnectClicked)
        self.disConnectButton.clicked.connect(self.on_disConnectClicked)

# serverslist signals
        self.serversList.itemClicked.connect(self.on_serversItemClicked)
        self.serversList.itemDoubleClicked.connect(self.on_serversItemDblClicked)
        self.readServers.clicked.connect(self.on_readServersClicked) 
        self.addNewServer.clicked.connect(self.on_addNewServerClicked) 

# LogList signals
        self.LogClearButton.clicked.connect(self.on_logClearClicked)

# DirList signals                                          # Remote signals
        self.Left_DirList.itemClicked.connect(self.on_Left_DirList_clicked)
        self.Right_DirList.itemClicked.connect(self.on_Right_DirList_clicked)

# Buttons signals
        self.SENDButton.clicked.connect(self.on_SEND_clicked)
        self.RETRButton.clicked.connect(self.on_RETR_clicked)
        self.CopyButton.clicked.connect(self.on_Copy_clicked)
        self.MakeDirButton.clicked.connect(self.on_MakeDir_clicked)
        self.CDUPButton.clicked.connect(self.on_CDUP_clicked)
        self.DeleteButton.clicked.connect(self.on_Delete_clicked)
        self.OpenButton.clicked.connect(self.on_Open_clicked)
        self.AttrsButton.clicked.connect(self.on_Attrs_clicked)
        self.RenameButton.clicked.connect(self.on_Rename_clicked)

        self.CloseButton.clicked.connect(self.on_Close_clicked)

        global Left_nlst_lines
        global Right_nlst_lines
        global Left_list_lines
        global Right_list_lines
        global RemoteOn
        global Local_Home
       
        msg = "--- My-FTP_Client app starting ---" 
        debug(self, msg)
        
        path = os.getcwd()
        Local_Home = path
        Right_nlst_lines = os.listdir(path)
        
#        msg = "Dbg: " + str(Right_nlst_lines)
#        debug(self, msg)

        self.Left_Label.setText("Left  L o c a l   DirList")  
    
        self.Right_Path.clear()
        self.Right_Path.insertPlainText(path)
        self.Left_Path.clear()
        self.Left_Path.insertPlainText(path)

        read_Right_Local_DirList(self, "Connect")        
        Left_nlst_lines = Right_nlst_lines 
        Left_list_lines = Right_list_lines
        fill_Left_DirList(self) 

        set_ButtonGroup(self)
        set_Buttons(self, True)
        
    def on_ConnectClicked(self):
        msg = "--- I'm at on_ConnectClicked ---"   
        debug(self, msg)
        Connect(self)
        return
    
        
    def on_disConnectClicked(self):
        msg = "--- I'm at on_disConnectClicked ---"   
        debug(self, msg)
        DisConnect(self)
        return
    

# log modules

    def on_logClearClicked(self):
        
        msg = "--- I'm at on_logClearClicked ---"   
        debug(self, msg)
        
        self.LogList.clear()

        
# servers modules

    def on_serversItemDblClicked(self):
        global servers_lines
        global lines

        msg = "--- I'm at on_on_serversItemDblClicked ---"   
        debug(self, msg)
        
        row = self.serversList.currentRow()
        rows = len(servers_lines)
        rown = rows - 1
        while row < rows:
            if row < rown:
                rwn = row + 1
                line = servers_lines[rwn]
                lines[row] = line
                row += 1
            else:
                rows = rown
                
        servers_lines[rown] = ""
        
        path = os.path.join(Local_Home, "servers.txt")
        with open(path, 'w') as fd:
            fd.writelines(servers_lines)
            fd.close()

        self.serversList.clear()
        ls = len(servers_lines)
        ln = 0
        while ln < ls:
            name = get_name(servers_lines[ln])
            self.serversList.addItem(name)
            ln += 1
        
        return
    

    def on_addNewServerClicked(self):
        global Path
        global servers_lines
        
        msg = "--- I'm at on_addNewServerClicked ---"   
        debug(self, msg)
        
        name = self.serverName.text()
        ip = self.ipAddr.text()
        port = self.portNo.text()
        user = self.userName.text()
        passw = self.userPassw.text()
        line = name + ',' + ip + ',' + port + ',' + user + ',' + passw + ',' + '\n'
        with open("servers.txt", 'a') as fd:
            fd.writelines(line)
            fd.close()
        self.serversList.clear()
            

    def on_readServersClicked(self):
        global servers_lines
        
        msg = "--- I'm at on_readServersClicked ---"   
        debug(self, msg)
 
        name = ""
        ls = 0
        ln = 0
        self.serversList.clear()
        path = os.path.join(Local_Home, "servers.txt")
        with open(path, 'r') as fd:
            servers_lines = fd.readlines(-1)
            ls = len(servers_lines)
            while ln < ls:
                name = get_name(self, servers_lines[ln])
                self.serversList.addItem(name)
                ln += 1
            fd.close()
 

    def on_serversItemClicked(self):
        global servers_lines
        
        msg = "--- I'm at on_on_serversItemClicked ---"   
        debug(self, msg)
 
        row = self.serversList.currentRow()
        name, ip, port, user, passw = unpack_line(self, servers_lines[row])
        self.serverName.setText(name) 
        self.ipAddr.setText(ip) 
        self.portNo.setText(port) 
        self.userName.setText(user) 
        self.userPassw.setText(passw) 
        return
    
    
    
    
# Ftp Client modules

    def on_SEND_clicked(self):
        global RemoteOn
        
        msg = "--- I'm at on_SEND_clicked ---"   
        debug(self, msg)

        if RemoteOn and self.RightOn.isChecked():
            name = self.FileName.text()
            ext = self.Attr.text()
            if ext == 'dir':
                SEND_dir(self, name)
            else:
                SEND_file(self, name)
        
            self.Attr.clear()
            self.FileName.clear()
            read_Server_DirList(self, "SEND")
            
        self.Attr.clear()
        self.FileName.clear()
        Fake_Click("SEND")
        return


    def on_RETR_clicked(self):
        global RemoteOn
        
        msg = "--- I'm at on_RETR_clicked ---"   
        debug(self, msg)

        if RemoteOn and self.LeftOn.isChecked():
            name = self.FileName.text()
            ext = self.Attr.text()
            if ext == 'dir':
                RETR_dir(self, name)
            else:
                RETR_file(self, name)
        
        self.Attr.clear()
        self.FileName.clear()
        Fake_Click("RETR")
        return


# Common modules

    def on_Copy_clicked(self):
        global RemoteOn

        msg = "--- I'm at on_Copy_clicked ---"   
        debug(self, msg)

        if RemoteOn:
            pass
        else:
            Local_Copy(self)  
            
        self.Attr.clear()
        self.FileName.clear()
        Fake_Click("Copy")
        return
           

    def on_Attrs_clicked(self):
        global RemoteOn
         
        msg = "--- I'm at on_Attr_clicked ---"   
        debug(self, msg)
       
        name = self.FileName.text()
        
        if self.LeftOn.isChecked():
            
            if RemoteOn:
                row = self.Left_DirList.currentRow()
                line = Left_list_lines[row]
            else:
                line = get_Local_Attrs(self, name, "Left")

        else: 
            line = get_Local_Attrs(self, name, "Right")
        
        self.FileAttrs.setText(line[0:52])
        Fake_Click("Attrs")
        return
    
        
    def on_Delete_clicked(self):
        global RemoteOn
        
        name =self.FileName.text()
        attr = self.Attr.text()

        if self.LeftOn.isChecked():
            msg = "--- I'm at on_Delete_clicked from Left_DirList ---"   
            debug(self, msg)

            if RemoteOn:
                Delete_on_Server(self, name, attr)
                return
            
            path = self.Left_Path.toPlainText()
        else: 
            msg = "--- I'm at on_Delete_clicked from Right_DirList ---"   
            debug(self, msg)
            path = self.Right_Path.toPlainText()


        if attr == "dir":
            dir_path = os.path.join(path, name)

            try:
                shutil.rmtree(dir_path)
            except Exception as e: 
                msg = "Error: " + str(e)
                debug(self, msg)
            
        else:
            file_path = os.path.join(path, name)
            
            try:
               os.remove(file_path)
            except Exception as e: 
                msg = "Error: " + str(e)
                debug(self, msg)

        if self.LeftOn.isChecked():
            read_Left_Local_DirList(self, "Delete")
        else:
            read_Right_Local_DirList(self, "Delete")
                
        self.Attr.clear()
        self.FileName.clear()
        sync_Lists(self)
        self.Attr.clear()    
        Fake_Click("Delete")
        return


    def on_CDUP_clicked(self):
        global RemoteOn
        
        if self.LeftOn.isChecked():
            msg = "--- I'm at on_CDUP_clicked at Left_DirList ---"   
            debug(self, msg)

            self.FileAttrs.clear()
            self.FileName.clear()

#            check_slash(self, False)
            if RemoteOn:
                CDUP_on_Server(self) 
                return

            path = self.Left_Path.toPlainText()
            parent = os.path.dirname(path)
            self.Left_Path.clear()
            self.Left_Path.insertPlainText(parent)
            read_Left_Local_DirList(self, "CDUP")
         
        else: 
            msg = "--- I'm at on_CDUP_clicked at Right_DirList ---"   
            debug(self, msg)

            self.FileAttrs.clear()
            self.FileName.clear()

#            check_slash(self, False)
            path = self.Right_Path.toPlainText()
            parent = os.path.dirname(path)
            self.Right_Path.clear()
            self.Right_Path.insertPlainText(parent)
            read_Right_Local_DirList(self, "CDUP")

#        sync_Lists(self)
        Fake_Click("CDUP")
        return    


    def on_Left_DirList_clicked(self):
        global Left_DirList_RowOn
        global Right_DirList_RowOn

        self.FileAttrs.clear()   
        row = self.Left_DirList.currentRow()
        if row == Left_DirList_RowOn:
            msg = "Error - Fake click on_Left_DirList"   
            debug(self, msg)

        else:
            msg = "--- I'm at on_Left_DirList_clicked ---"   
            Left_DirList_RowOn = row                  
            self.LeftOn.setChecked(True)
            Left_DirList_clicked(self) 

        Fake_Click("Left")
        return

        
    def on_Right_DirList_clicked(self):
        global Left_DirList_RowOn
        global Right_DirList_RowOn
        
        self.FileAttrs.clear()   
        row = self.Right_DirList.currentRow()
        if row == Right_DirList_RowOn:
            msg = "Error - Fake click on_Right_DirList"   
            debug(self, msg)

        else:
            msg = "--- I'm at on_Right_DirList_clicked ---"   
            debug(self, msg)
            Right_DirList_RowOn = row                  
            self.RightOn.setChecked(True)
            Right_DirList_clicked(self) 

        Fake_Click("Right")
        return


    def on_Open_clicked(self):
        global RemoteOn
        global OpenButtonOn

        exc = self.Attr.text()
        
        if self.LeftOn.isChecked():
            msg = "--- I'm at on_Open_clicked for Left_DirList ---"   
            debug(self, msg)
 
            if OpenButtonOn > -1:
                msg = "Error - Fake click on_OpenButton"   
                debug(self, msg)
                return
            else:
                OpenButtonOn += 1
                
            if RemoteOn:
                Open_Dir_on_Server(self)
                return
        
#            check_slash(self, True)
            if exc[0] == 'f':
                open_File(self, "Left")
                return
            read_Left_Local_DirList(self, "Open")
#            check_slash(self, True)
        else: 
            msg = "--- I'm at on_Open_clicked for Right_DirList ---"   
            debug(self, msg)

            if OpenButtonOn > -1:
                msg = "Error - Fake click on_OpenButton"   
                debug(self, msg)
                return
            else:
                OpenButtonOn += 1

#            check_slash(self, True)
            if exc[0:1] == 'f':
                open_File(self, "Right")
                return
            read_Right_Local_DirList(self, "Open")
#            check_slash(self, True)

        sync_Lists(self)
        self.FileName.clear()
        Fake_Click("Open")
        return
        

    def on_Rename_clicked(self):
        global RemoteOn

        msg = "--- I'm at on_Rename_clicked ---"   
        debug(self, msg)

        new_name = self.FileAttrs.text()
        old_name = self.FileName.text()
        if len(old_name) == 0 or len(new_name) == 0:
            return
        if self.LeftOn.isChecked():            
            if RemoteOn:
                Rename_on_Server(self, old_name, new_name)
            else:
                Rename_on_Local(self, old_name, new_name)
                
        else:
            Rename_on_Local(self, old_name, new_name)
           

        self.FileAttrs.clear()
        self.FileName.clear()        
        Fake_Click("Rename")
        return    


    def on_MakeDir_clicked(self):
        global RemoteOn
        
        msg = "--- I'm at on_MakeDir_clicked ---"
        debug(self, msg)
        
        name = self.FileName.text()
        if len(name) == 0:
            name = "New Directory"
       
        if self.LeftOn.isChecked():
            msg = "Msg: Local Left_Make_Dir as - " + name   
            debug(self, msg)
        
            if RemoteOn:
                Make_Dir_on_Server(self, name)
            else:
                Make_Dir_on_Local(self, name)            
                  
        else:
            Make_Dir_on_Local(self, name)            

        sync_Lists(self) 
        self.Attr.clear()
        self.FileName.clear()
        Fake_Click("MakeDir")
        return        

    def on_Close_clicked(self):
        self.close() 
        
        
        
        
app = QtWidgets.QApplication([])
win = My_FTP_Client()
win.show()
sys.exit(app.exec())

