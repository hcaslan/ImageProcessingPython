# -*- coding: utf-8 -*-
"""
Created on Fri May 1 06:38:38 2022

@author: hcaslan
"""

from skimage import data , io , filters , color , segmentation , img_as_float
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog , QMessageBox , QDesktopWidget ,QProgressBar, QPushButton
from PyQt5.QtGui import QPixmap
import numpy as np
import os
from abc import ABCMeta,abstractmethod

class Operations():
    def __init__(self):  
        self.history_position = 0
        self.history = []
        self.last = []
        self.operation_list = ['first_operation','rgb2gray','rgb2hsv','multiOtsuThresholding','chanVeseSegmentation',
                               'morphologicalSnakes','roberts','sobel','scharr','prewitt']
   
    #open the source and set the history_position at 0
    def open_source(self,mainwindow):
        self.clearOutput(mainwindow)
        self.history.append('first_operation')
        self.history_position = 0
        print(self.last)
        fname= QFileDialog.getOpenFileName(QFileDialog(),
                                           'Open File', os.getcwd() + 
                                           '/sample_images','Image files (*.jpg *.png)')
        if len(fname[0]) != 0:
            self.source_imagePath = fname[0]
            self.sourceimage_pixmap = QPixmap(self.source_imagePath)
            mainwindow.sourceLabel.setPixmap(self.sourceimage_pixmap)
            
            self.setSourceImage(io.imread(self.source_imagePath))
            self.enableOperations(mainwindow)    
            self.first_operation(mainwindow)
            
    #set method for source image        
    def setSourceImage(self,img):
        self.SourceImage = img
          
    #get method for source image    
    def getSourceImage(self):
        return self.SourceImage
    
    #set method for output image              
    def setOutputImage(self,img,mainwindow):
        self.OutputImage = img
        io.imsave('icons/tempOutput.jpg',self.OutputImage)
        print("set output")
        print(len(self.history))
        mainwindow.outputLabel.setPixmap(QPixmap('icons/tempOutput.jpg'))
        mainwindow.pB_saveOutput.setEnabled(True)
        mainwindow.pB_saveAsOutput.setEnabled(True)
        mainwindow.output2sourceLabel.setEnabled(True)
        mainwindow.pB_exportAsOutput.setEnabled(True)
        mainwindow.pB_clearOutput.setEnabled(True)
        mainwindow.pB_undo.setEnabled(True)
        mainwindow.actionSave_Output.setEnabled(True)
        mainwindow.actionSave_As_Output.setEnabled(True)
        mainwindow.actionOutput.setEnabled(True)
        mainwindow.actionOutput_2.setEnabled(True)     
        mainwindow.actionUndo.setEnabled(True)
        
    #get method for output image       
    def getOutputImage(self):
        return self.OutputImage
      
    #clear the source and set the history_position at 0
    def clearSource(self,mainwindow):
        self.history.clear()
        self.history_position = 0
        mainwindow.sourceLabel.setPixmap(QPixmap())
        self.disableOperations(mainwindow)
        
    #export as source image
    def exportAsSourceImage(self,mainwindow):
        if self.source_imagePath[-3:] == 'png':
            fname=QFileDialog.getSaveFileName(QFileDialog(),'Export As', 'c\\','Image files (*.jpg)')
        
        if self.source_imagePath[-3:] == 'jpg':
            fname=QFileDialog.getSaveFileName(QFileDialog(),'Export As', 'c\\','Image files (*.png)')
        
        source_export_path = fname[0]
        io.imsave(source_export_path, self.getSourceImage())
    
    #Conversion Operations
    ##rgb to grayscale
    def rgb2gray(self,mainwindow,redo=False):
        print(self.history)
        try:
            image_gray = color.rgb2gray(self.getSourceImage())
            self.setOutputImage(image_gray,mainwindow)          
            if redo == False:
                self.history.append('rgb2gray')
                self.history_position += 1
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
    ##rgb to hsv
    def rgb2hsv(self,mainwindow,redo=False):
        print(self.history)
        try:
            image_hsv = color.rgb2hsv(self.getSourceImage())
            self.setOutputImage(image_hsv,mainwindow)           
            if redo == False:
                self.history.append('rgb2hsv')
                self.history_position += 1
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
            
    #Segmentation Operations   
    ##multi-otsu thresholding segmentation  
    def multiOtsuThresholding(self,mainwindow,redo=False):
        try:
            image_multiOtsu = filters.threshold_multiotsu(self.getSourceImage())
            regions = np.digitize(self.getSourceImage(), bins=image_multiOtsu)
            self.setOutputImage(regions,mainwindow)
            if redo == False:
                self.history.append('multiOtsuThresholding')
                self.history_position += 1
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
        
    ##chan-vese segmentation
    def chanVeseSegmentation(self,mainwindow,redo=False):
        try:
            self.waitEvent(mainwindow)
            #self.progressEvent(mainwindow)
            input_img =img_as_float(self.getSourceImage())
            image_chanVese = segmentation.chan_vese(input_img,mu =0.25,lambda1=1,lambda2=1,tol=1e-3, 
                                                      max_iter=200,dt=0.5, init_level_set="checkerboard", extended_output=True)
            self.setOutputImage(image_chanVese[1],mainwindow)           
            if redo == False:
                self.history.append('chanVeseSegmentation')
                self.history_position += 1
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
        
    ##morphological snakes segmentation
    def morphologicalSnakes(self,mainwindow,redo=False):
        try:
            self.waitEvent(mainwindow)
            #self.progressEvent(mainwindow)
            input_img =img_as_float(self.getSourceImage())
            init_ls = segmentation.checkerboard_level_set(input_img.shape, 6)
            evolution = []
            callback = self.store_evolution_in(evolution)
            l_s = segmentation.morphological_chan_vese(input_img, 35, init_level_set=init_ls, smoothing=3,
                                                        iter_callback=callback)             
            self.setOutputImage(l_s,mainwindow)            
            if redo == False:
                self.history.append('morphologicalSnakes')
                self.history_position += 1
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
        
    ##store evolution for morphologicalSnakes       
    def store_evolution_in(self,lst):
        def _store(x):
            lst.append(np.copy(x))

        return _store
    
    #Edge Detection Operations   
    ##roberts edge detection
    def roberts(self,mainwindow,redo=False):
        try:
            image_roberts = filters.roberts(self.getSourceImage())
            self.setOutputImage(image_roberts, mainwindow) 
             
            if redo == False:
                self.history.append('roberts')
                self.history_position +=1
                 
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
        
    ##sobel edge detection         
    def sobel(self,mainwindow,redo=False):
        try:
            image_sobel = filters.sobel(self.getSourceImage())
            self.setOutputImage(image_sobel, mainwindow)   
             
            if redo == False:
                self.history.append('sobel')
                self.history_position += 1
                 
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
    
    ##scharr edge detection         
    def scharr(self,mainwindow,redo=False):
        try:
            image_scharr = filters.scharr(self.getSourceImage())
            self.setOutputImage(image_scharr, mainwindow)  
             
            if redo == False:
                self.history.append('scharr')
                self.history_position += 1 
                 
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
        
    ##prewitt edge detection          
    def prewitt(self,mainwindow,redo=False):
        try:
            image_prewitt = filters.prewitt(self.getSourceImage())
            self.setOutputImage(image_prewitt, mainwindow)
             
            if redo == False:
                self.history.append('prewitt')
                self.history_position +=1
                 
        except:
            self.errorEvent(mainwindow)
        self.checkRepetition()
 
    #clear output         
    def clearOutput(self,mainwindow):
        mainwindow.outputLabel.setPixmap(QPixmap())
        self.history.clear()
        self.history_position = 0
        mainwindow.output2sourceLabel.setEnabled(False)
        mainwindow.pB_undo.setEnabled(False)
        mainwindow.pB_redo.setEnabled(False)
        mainwindow.pB_saveOutput.setEnabled(False)
        mainwindow.pB_saveAsOutput.setEnabled(False)
        mainwindow.pB_exportAsOutput.setEnabled(False)
        mainwindow.pB_clearOutput.setEnabled(False)
        mainwindow.actionSave_Output.setEnabled(False)
        mainwindow.actionSave_As_Output.setEnabled(False)
        mainwindow.actionRedo.setEnabled(False)
        mainwindow.actionUndo.setEnabled(False)
        mainwindow.actionOutput_2.setEnabled(False)
        mainwindow.actionOutput.setEnabled(False)
        self.clearAll(mainwindow)
        
    #clear both of source and output images    
    def clearAll(self,mainwindow):
        if (mainwindow.pB_clearSource.isEnabled() == True) or (mainwindow.pB_clearOutput.isEnabled() == True):  
            mainwindow.pb_clearAll.setEnabled(True)
            mainwindow.actionAll.setEnabled(True)
        else:
            mainwindow.pb_clearAll.setEnabled(False)
            mainwindow.actionAll.setEnabled(False)
            
    #save output image
    def saveOutputImage(self,mainwindow):
        io.imsave(self.source_imagePath,self.getOutputImage())
        mainwindow.pB_saveOutput.setEnabled(False)
        mainwindow.actionSave_Output.setEnabled(False)
        
    #save as output image        
    def saveAsOutputImage(self,mainwindow):
        fname=QFileDialog.getSaveFileName(QFileDialog(),'Save As', 'c\\','Image files (*.jpg *.png)')
        io.imsave(fname[0], self.getOutputImage())
        mainwindow.pB_saveAsOutput.setEnabled(False)
        mainwindow.actionSave_As_Output.setEnabled(False)
        
    #export as output image    
    def exportAsOutputImage(self,mainwindow):
        if self.source_imagePath[-3:] == 'png':
            fname=QFileDialog.getSaveFileName(QFileDialog(),'Save As', 'c\\','Image files (*.jpg)')
        
        if self.source_imagePath[-3:] == 'jpg':
            fname=QFileDialog.getSaveFileName(QFileDialog(),'Save As', 'c\\','Image files (*.png)')
        
        self.outputImagePath = fname[0]
        io.imsave(self.outputImagePath, self.getOutputImage())
        mainwindow.pB_exportAsOutput.setEnabled(False)
        mainwindow.actionOutput.setEnabled(False)
    
    #undo 
    def undo(self,mainwindow):   
        self.last.append(self.history[self.history_position])
        self.history_position -= 1
        self.history.pop()
        print("last", self.last)
        for operation in self.operation_list:
            if operation == self.history[self.history_position]:
                eval('self.'+ operation + "(mainwindow,redo=True)")
        if self.history_position == 0:
            mainwindow.pB_undo.setEnabled(False)
            mainwindow.actionUndo.setEnabled(False)
        mainwindow.pB_redo.setEnabled(True)
        mainwindow.actionRedo.setEnabled(True)
        print(self.history)
        print(self.history_position)

    #redo
    def redo(self,mainwindow): 
        self.last.reverse()
        for i in range(len(self.last)):
            self.history.append(self.last[i])
        self.last.clear()  
        self.history_position += 1
        for operation in self.operation_list:
            if operation == self.history[self.history_position]:
                eval('self.'+ operation + "(mainwindow,redo=True)")
                
        if self.history_position == len(self.history)-1:            
            mainwindow.pB_redo.setEnabled(False)
            mainwindow.actionRedo.setEnabled(False)
        print(self.history)
        print(self.history_position)
    
    #Prevent multiple implementation of the same operation to the same source.
    def checkRepetition(self):
        if (self.history[self.history_position] == self.history[self.history_position-1] ):
            print("Repetition")
            self.history.pop()
            self.history_position -= 1
            
    #Error message pop-up
    def errorEvent(self,mainwindow):
        mainwindow.message_box = QMessageBox()
        mainwindow.message_box.setWindowTitle("Error")
        mainwindow.message_box.setIcon(QMessageBox.Critical)
        mainwindow.message_box.setText("Selected source image is not suitable for this operation. Please select an appropriate source image.")
        mainwindow.message_box.setStandardButtons(QMessageBox.Ok)
        qr = mainwindow.message_box.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        mainwindow.message_box.frameGeometry()
        mainwindow.message_box.show()

    #Wait message pop-up   
    def waitEvent(self,mainwindow):
        mainwindow.message_box = QMessageBox()
        mainwindow.message_box.setWindowTitle("Please Wait")
        mainwindow.message_box.setIcon(QMessageBox.Information)
        mainwindow.message_box.setText("This operation takes some time. Thanks for waiting.")
        mainwindow.message_box.setStandardButtons(QMessageBox.Ok)
        qr = mainwindow.message_box.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        mainwindow.message_box.frameGeometry()
        mainwindow.message_box.show()         
    
    #close call for actionexit
    def exitEvent(self, event, mainwindow):
        mainwindow.close()
        
    def first_operation(self,mainwindow,redo=False):
        mainwindow.outputLabel.setPixmap(QPixmap())
    
    #disable the unavailable operations.
    def disableOperations(self,mainwindow):
        mainwindow.pB_exportAsSource.setEnabled(False)
        mainwindow.pB_clearSource.setEnabled(False)
        mainwindow.actionSource_2.setEnabled(False)
        mainwindow.pB_rgbToGray.setEnabled(False)
        mainwindow.pB_rgbToHsv.setEnabled(False)
        mainwindow.pB_Roberts.setEnabled(False)
        mainwindow.pB_Sobel.setEnabled(False)
        mainwindow.pB_MOS.setEnabled(False)
        mainwindow.pB_MS.setEnabled(False)
        mainwindow.pB_CVS.setEnabled(False)
        mainwindow.pB_Scharr.setEnabled(False) 
        mainwindow.pB_Previtt.setEnabled(False)   
        mainwindow.actionSource.setEnabled(False)
        mainwindow.actionSource_2.setEnabled(False)
        mainwindow.menuConversion.setEnabled(False)
        mainwindow.menuSegmentation.setEnabled(False)
        mainwindow.menuEdge_Detection.setEnabled(False)
        self.clearAll(mainwindow)
        
    #enable the available operations.    
    def enableOperations(self,mainwindow):  
        mainwindow.pB_exportAsSource.setEnabled(True)
        mainwindow.menuConversion.setEnabled(True)
        mainwindow.pB_clearSource.setEnabled(True)
        mainwindow.pB_rgbToGray.setEnabled(True)
        mainwindow.pB_rgbToHsv.setEnabled(True)
        mainwindow.pB_Roberts.setEnabled(True)
        mainwindow.pB_Scharr.setEnabled(True)
        mainwindow.pB_MOS.setEnabled(True)
        mainwindow.pB_MS.setEnabled(True)
        mainwindow.pB_CVS.setEnabled(True)
        mainwindow.pB_Sobel.setEnabled(True)       
        mainwindow.pB_Previtt.setEnabled(True)   
        mainwindow.actionSource.setEnabled(True)
        mainwindow.actionSource_2.setEnabled(True)
        mainwindow.menuSegmentation.setEnabled(True)
        mainwindow.menuEdge_Detection.setEnabled(True)
        self.clearAll(mainwindow)
        