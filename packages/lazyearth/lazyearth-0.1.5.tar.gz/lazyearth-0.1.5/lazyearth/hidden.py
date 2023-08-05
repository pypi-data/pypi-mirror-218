from pathlib import Path
import os
import matplotlib.pyplot as plt


def get_directory_size(directory_path):
    total = 0
    for path, dirs, files in os.walk(directory_path):
        for f in files:
            fp = os.path.join(path, f)
            total += os.path.getsize(fp)
    return total
def byteconvert(num):
    if num<1024**2:
        output = str(round(num/(1024**1),5)) + " Kb"
    elif num<1024**3:
        output = str(round(num/(1024**2),5)) + " Mb"
    elif num<1024**4:
        output = str(round(num/(1024**3),5)) + " Gb"
    else:
        output = str(round(num/(1025**4),5)) + " Tb"
    return output

def memory_checker():
    """
    Use to check memory of everyfile from path
    :param size  : size of image
    :param range : Range of value
    :param nan   : Number of NaN
    :param inf   : Number of Inf
    :return      : 1D array image
    """
    p = Path(input("Enter path : "))
    os.chdir(Path(p))
    # print(os.getcwd())
    p = os.listdir()
    # create file dict
    file_list = {}
    for i in p:
        try:
            if os.path.isfile(i):
                filesize = os.path.getsize(i)
                print("File : ",i," size:",byteconvert(filesize))
                file_list.update({i:filesize})
            elif os.path.isdir(i):
                foldersize = get_directory_size(i)
                print("Folder : ",i," size:",byteconvert(foldersize))
                file_list.update({i:foldersize})
        except:
            print(i,"file type error")
    # file_list
    x = {}
    # analyze
    while len(file_list)>0:
        maximum = file_list[str(list(file_list)[0])]
        for i in file_list.items():
            if i[1]>maximum:
                maximum = i[1]
        for j in file_list.items():
            if j[1]==maximum:
                print(j)
                x.update({j[0]:j[1]})
                file_list.pop(j[0])
                break
    # Create lists of keys and values
    keys = x.keys()
    values = x.values()
    plt.figure(figsize=(100,40))
    # Create a bar plot
    plt.bar(keys, values)
    # plt.bar(values, keys)
    plt.xticks(rotation='vertical')# Show the plot
    plt.grid()
    plt.show()
    # input("Press Enter to exit...")



# """
# Thu May 19 15:30:54 2022
# OS system: Linux
# Project_name: pathrowcheckfile
# @author:Tun.k
# """
# ######################################################################


# ######################################################################



# def PathRowcheck(pathrow):
#      import os       
#      from tracemalloc import start
#      import xlsxwriter as xw
#      import tarfile
#      import logging as log
#      from osgeo import gdal
#      import shutil
#      import datetime
#      # name of file
#      filter = pathrow  #132048 #129048,129049,130048,130049
#      starttime=datetime.datetime.now()
#      # path
#      maindirectory='/home/tun/tunsharedrive/download_data/ls7_collections_sr_scene'
#      destination = '/home/tun/Desktop'+'/'+'LC07-'+filter
#      Extractfolder = '/home/tun/Desktop/Extract_folder'
#      #Create foldr 
#      os.mkdir(destination)
#      # status
#      countmain = 1 
#      x=len(os.listdir(os.chdir(maindirectory)))
#      LS_Prove = ['LC04','LC05','LC07','LC08']   
#      LS_Exten = ['.tif']
#      LS_Retry = 3
#      row =1
#      # create xlsx file
#      os.chdir('/home/tun/Desktop')
#      wbname = 'Tarmanage-'+filter+'.xlsx'
#      wb = xw.Workbook(wbname)
#      ws = wb.add_worksheet('page1')
#      ws.write(0,0,'Tarname')
#      ws.write(0,1,'PR_ID')
#      ws.write(0,2,'Path')
#      ws.write(0,3,'Row')
#      ws.write(0,4,'Acc')
#      ws.write(0,5,'Size(Byte)')
#      ws.write(0,6,'Copied')
#      ws.write(0,7,'Extracted')
#      ws.write(0,8,'Source')
#      ws.write(0,9,'Target')
#      ws.write(0,10,'okName')
#      ws.write(0,11,'okSize')
#      ws.write(0,12,'okGDAL')
#      ws.write(0,13,'error massage')
#      ####################################################################################
#      # Folder loop
#      for indxfolder,folder in enumerate(os.listdir(os.chdir(maindirectory))):
#          print('indx',indxfolder,'folder:',folder)
#          countsub = 0
#          if 'bak' in folder:
#              continue
#          # Tar File loop 
#          for file in os.listdir(os.chdir(maindirectory+'/'+folder)):
#              okName = False
#              okGDAL = '?'
#              okSize = '?'
#              # Condition Check #1 Landsat name check
#              if os.path.isfile(file)==1 and file[:4].upper() in LS_Prove:
#                  print(file)
#                  okName = True
#                  # File pathrow selection
#                  if filter in file:
#                      filesize=os.path.getsize(file)
#                      # Extract file at Extractfoldr for condition 234
#                      os.mkdir(Extractfolder)
#                      try:
#                          my_tar = tarfile.open(file)
#                          my_tar.extractall(Extractfolder)
#                          # Extracted file loop
#                          for member in my_tar.getmembers():
#                              okSize = True
#                              log.info((member.name,member.size))
#                              desFile = os.path.join(Extractfolder,member.name)
#                              # Condition Check #2 .tif file Check
#                              if member.size != os.path.getsize(desFile):
#                                  okSize=False
#                                  break
#                              # Condition Check #3 GDAL Check
#                              if os.path.splitext(desFile)[1] in LS_Exten:
#                                  okCount = 0
#                                  okGDAL = False
#                                  while okCount < 3 and not okGDAL:
#                                      okCount +=1
#                                      desData =gdal.Open(desFile)
#                                      print(desData)
#                                      if not desData == None:
#                                          okGDAL = True
#                                      else:
#                                          okGDAL = False
#                                  errorm = ''
#                      except Exception as e:
#                          print(e)
#                          errorm = e
#                      print(os.getcwd())
#                      # Assign value to .xlsx file
#                      ws.write(row,0,file)
#                      ws.write(row,1,file[4:10])
#                      ws.write(row,2,file[4:7])
#                      ws.write(row,3,file[7:10])
#                      ws.write(row,4,file[16:18]+'/'+file[14:16]+'/'+file[10:14])
#                      ws.write(row,5,filesize)
#                      ws.write(row,8,(os.getcwd()+'/'+file))
#                      ws.write(row,10,okName)
#                      ws.write(row,11,okSize)
#                      ws.write(row,12,okGDAL)
#                      ws.write(row,13,str(errorm))
#                      row +=1
#                      os.listdir(Extractfolder)
#                      shutil.rmtree(Extractfolder)
#              countsub +=1
#              # Status
#              allfile=len(os.listdir(os.getcwd()))
#              print('status :',end=' ')
#              print(countsub,'/',allfile,'/',countmain,'/',x,end=' ')
#              print('(%.2f'%(countsub/allfile*100),'%)')
#          countmain = countmain+1
#          print('status:',indxfolder+1,'/',x) 
     
#      os.chdir('/home/tun/Desktop')
#      wb.close()
#      endtime=datetime.datetime.now()
#      print("Total time:",endtime-starttime)

# import pandas as pd
# file = pd.read_excel('/home/tun/Desktop/pathrowlist.xlsx')
# lst = file['pathrow'].tolist()
# for pr in enumerate(lst):
#     print(pr[0]+1,'/ 45 :',pr[1])
#     PathRowcheck(str(pr[1]))



# import datetime
# import subprocess
# import os

# now = datetime.datetime.now()
# trz = datetime.datetime(now.year,now.month,now.day, 16, 30, 00, 000000)
# os.chdir(r"D:\clockcode")
# command1 = "python 2345.py"
# command2 = "python 1630.py"
# if now<trz:
#         subprocess.run(command2)
# else:
#     subprocess.run(command1)



# # =============================================================================
# # #operation function
# # =============================================================================
# # import os
# # import cv2
# # os.chdir(r'C:\Users\tul\Desktop')
# # from tul import *
# # imagefolder='hand'
# # dedtinationfolder='after_findfing2'
# # T=len(os.listdir(chfo(imagefolder)))
# # n=0
# # for item in os.listdir(chfo(imagefolder)):
# #     chfo(imagefolder)
# # #-----------------------------------------------------------------------------#
# #     output=findfing2(item)
# #     output=output*255
# # #-----------------------------------------------------------------------------#
# #     print('Calculating : %.5f'%((n+1)/T*100),'%')
# #     chfo(dedtinationfolder)
# #     imwr(item,output)
# #     n=n+1
# # =============================================================================



# # =============================================================================
# # name : evaluatefunction
# # =============================================================================
# def evaluatefunction(Groundtruthfolder,imagefolder,resulution=2):
#     from tul import chfo_q,grayread,im_cofu_ma2
#     import os 
#     from datetime import datetime
#     import time
#     start=time.time()
    
#     GTlst=[x for x in os.listdir(chfo_q(Groundtruthfolder))]
#     imglst=[y for y in os.listdir(chfo_q(imagefolder))]
#     if len(GTlst)!=len(imglst):
#         print('Something wrong')
#         return
#     # rwhite=[];rblack=[];cwhite=[];cblack=[];
#     TP=[];FN=[];TN=[];FP=[];Aa=[];Ee=[];Pp=[];Rr=[];Ff=[]
#     T=len(os.listdir(chfo_q(imagefolder)))
#     for num in range(T):
#           chfo_q(Groundtruthfolder);GT=grayread(GTlst[num])
#           chfo_q(imagefolder);img=grayread(imglst[num])
#           value=im_cofu_ma2(GT,img)
#           # rwhite.append(value[0])
#           # rblack.append(value[1])
#           # cwhite.append(value[2])
#           # cblack.append(value[3])
#           TP.append(value[4])
#           FN.append(value[5])
#           TN.append(value[6])
#           FP.append(value[7])
#           Aa.append(value[8])
#           Ee.append(value[9])
#           Pp.append(value[10])
#           Rr.append(value[11])
#           Ff.append(value[12])    
#           print("Evaluate Calculating",':',datetime.now().strftime("%H:%M:%S")+','+time.strftime("%H:%M:%S", time.gmtime(time.time()-start))+','+"(%d/%d)"%(num+1,T),': %.5f'%((num+1)/T*100),'%')
#     #     print("Calculating (%d/%d)"%(num+1,T),': %.5f'%((num+1)/T*100),'%')
#     Tp=sum(TP);Fn=sum(FN);Tn=sum(TN);Fp=sum(FP)
#     # Rwhite=sum(rwhite);Rblack=sum(rblack);Cwhite=sum(cwhite);Cblack=sum(cblack)
#     n=Tp+Fn+Tn+Fp
#     A=(Tp+Tn)/n
#     E=(Fp+Fn)/n
#     P=Tp/(Tp+Fp)
#     R=(Tp)/(Tp+Fn)
#     F=2*(P*R)/(P+R)
#     print('\nFunction name :',imagefolder)
#     print("                           Confusion Matrix                  ")
#     print("Accuracy  |%7.3f"%(A*100),'% |','='*round(A*100//resulution),' '*round(100//resulution-A*100//resulution)+'|')
#     print("Recall    |%7.3f"%(R*100),'% |','='*round(R*100//resulution),' '*round(100//resulution-R*100//resulution)+'|')
#     print("Precision |%7.3f"%(P*100),'% |','='*round(P*100//resulution),' '*round(100//resulution-P*100//resulution)+'|')
#     print("Error r.  |%7.3f"%(E*100),'% |','='*round(E*100//resulution),' '*round(100//resulution-E*100//resulution)+'|')
#     print("F1-score  |%7.3f"%(F*100),'% |','='*round(F*100//resulution),' '*round(100//resulution-F*100//resulution)+'|')
#     return Aa,Rr,Pp,Ee,Ff
# # =============================================================================
# # name : matplotlib
# # =============================================================================
# # plt.figure(figsize=(10*3*2,5*3*2))
# # plt.grid()
# # plt.rcParams.update({'font.size':100})
# # plt.stem(A)
# # plt.title('Accuracy')
# # scale_factor = 0.9 #highvalue-->more length
# # xmin, xmax = plt.xlim()
# # ymin, ymax = plt.ylim()
# # plt.xlim((xmin * scale_factor, xmax * scale_factor))
# # plt.ylim([0,1])
# # =============================================================================

# # =============================================================================
# # name : create point grountruth
# # =============================================================================
    
# # import cv2 
# # import numpy as np
# # import math
# # import matplotlib.pyplot as plt
# # import os
# # os.chdir(r'C:\Users\tul\Desktop')
# # from tul import *
# # import statistics as st
# # from numpy import zeros
# # import more_itertools as mit
# # import skimage.morphology, skimage.data

# # # # # #workfn
# # def workfn(event,x,y,flags,param):
# #     if event==cv2.EVENT_LBUTTONDOWN:
# #         cv2.circle(img,(x,y),2,(0,0,255),-1)
# #         print(int(x*(facn)),',',int((img.shape[0]-y)*(facn))) 
# #         # displaying the coordinates 
# #         # on the image window 
# #         font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
# #         cv2.putText(img,str(x*(int(facn)))+','+str((img.shape[0]-y)*(int(facn))),(x,y),font,0.7,(255, 0, 0),1)
# #         lst.append([int(x*(facn)),int((img.shape[0]-y)*(facn))])
# # #create Global
# # imagefolder='hand'
# # dedtinationfolder='hand_point_of_finger_GT'
# # for item in os.listdir(chfo(imagefolder)):
# #     chfo(imagefolder)           
            
# #     global lst;lst=[]
# #     #create canvas
# #     name='76.png'
# #     ima=imre(name)
# #     fing=imma(ima)
# #     img=fing
# #     fac=0.5;facn=fac**-1
# #     size_y=int(img.shape[0]*fac)
# #     size_x=int(img.shape[1]*fac)
# #     img = cv2.resize(img,(size_x,size_y))  # Resize image

# #     #assing name
# #     cv2.namedWindow('image')
# #     #call fn back
# #     cv2.setMouseCallback('image',workfn)
# #     #infinite loop
# #     while(True):
# #         cv2.imshow('image',img)
# #         #base case
# #         if cv2.waitKey(10)&0xff==27:
# #             break
# #     cv2.destroyAllWindows()

# #     chfo(dedtinationfolder)
# #     nameGT=name.split('.')[0]
# #     lsten(lst,nameGT)


# # =============================================================================
# # =============================================================================
# # import cv2 
# # import numpy as np
# # import math
# # import matplotlib.pyplot as plt
# # import os
# # os.chdir(r'C:\Users\tul\Desktop')
# # from tul import *
# # import statistics as st
# # from numpy import zeros
# # import more_itertools as mit
# # import skimage.morphology, skimage.data

# # # # # #workfn
# # def workfn(event,x,y,flags,param):
# #     if event==cv2.EVENT_LBUTTONDOWN:
# #         cv2.circle(img,(x,y),2,(0,0,255),-1)
# #         print(int(x*(facn)),',',int((img.shape[0]-y)*(facn))) 
# #         # displaying the coordinates 
# #         # on the image window 
# #         font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
# #         cv2.putText(img,str(x*(int(facn)))+','+str((img.shape[0]-y)*(int(facn))),(x,y),font,0.7,(255, 0, 0),1)
# #         lst.append([int(x*(facn)),int((img.shape[0]-y)*(facn))])
# # #create Global
# # global lst;lst=[]
# # #create canvas
# # chfo('hand')
# # name='1.png'
# # ima=imre(name)
# # fing=imma(ima)
# # img=fing
# # fac=0.5;facn=fac**-1
# # size_y=int(img.shape[0]*fac)
# # size_x=int(img.shape[1]*fac)
# # img = cv2.resize(img,(size_x,size_y))  # Resize image

# # #assing name
# # cv2.namedWindow('image')
# # #call fn back
# # cv2.setMouseCallback('image',workfn)
# # #infinite loop
# # while(True):
# #     cv2.imshow('image',img)
# #     #base case
# #     if cv2.waitKey(10)&0xff==27:
# #         break
# # cv2.destroyAllWindows()

# # chfo('hand_point_of_finger_GT')
# # nameGT=name.split('.')[0]
# # lsten(lst,nameGT)

# # =============================================================================

# #cal confusion_matrix
# #confusion_matrix(cv2.imread('g4 (1).jpg',0),cv2.imread('xxx.jpg',0))
# def confusion_matrix(GT,img):
#     import cv2 as cv   
#     from matplotlib import pyplot as plt

#     '''
#     from calmat import CM
#     G=cv2.imread('g4 (1).jpg',0)
#     i=cv2.imread('xxx.jpg',0)
#     CM(G,img)
#     '''
    
#     # GT = cv.imread('test.jpg',0)
#     GT = GT/255
#     # plt.imshow(GT,'gray')
#     # plt.show()
#     rwhite = 0
#     rblack = 0

#     [x,y]=GT.shape

#     for j in range(y):
#       for i in range(x):
#           if GT[i,j]==0:
#               rblack=rblack+1
#           else:
#               rwhite=rwhite+1
          


#     # img = cv.imread('real.jpg',0)
#     img = img/255
#     # plt.imshow(img,'gray')
#     # plt.show()
#     cwhite = 0
#     cblack = 0

#     [x,y]=img.shape

#     for j in range(y):
#       for i in range(x):
#           if img[i,j]==0:
#               cblack=cblack+1
#           else:
#               cwhite=cwhite+1
 



#     ###
#     TP=0
#     TN=0
#     FP=0
#     FN=0
#     for b in range(y):
#         for a in range(x):
#             if(GT[a,b]==1 and img[a,b]==1):
#                 TP=TP+1
#             if(GT[a,b]==0 and img[a,b]==0):
#                 TN=TN+1
#             if(GT[a,b]==1 and img[a,b]==0):
#                 FP=FP+1
#             if(GT[a,b]==0 and img[a,b]==1):
#                 FN=FN+1

        
#     # TP = float(input("True Positive is "))
#     # FN = float(input("False Negative is "))
#     # TN = float(input("True Negative is "))
#     # FP = float(input("False Positive is "))

#     n=TP+FN+TN+FP

#     A=(TP+TN)/n
#     E=(FP+FN)/n
#     P=TP/(TP+FP)
#     R=(TP)/(TP+FN)
#     F=2*(P*R)/(P+R)
#     print("\n")
                 

#     print("                 Confusion Matrix                ")

#     print("+---------------+-------------------------------+")
#     print("|               |           Predicted           |")
#     print("|    Actual     +---------------+---------------+")
#     print("|               |    Positive   |    Negative   |")
#     print("+---------------+---------------+---------------+")
#     print("|   Positive    |%14d |%14d |"%(TP,FN))
#     print("+---------------+---------------+---------------+")
#     print("|   Negative    |%14d |%14d |"%(FP,TN))
#     print("+---------------+---------------+---------------+")


#     print("+-------------------------+---------------------+")
#     print("|Ground truth white pixel |    %14d   |"%rwhite)
#     print("+-------------------------+---------------------+")
#     print("|Ground truth black pixel |    %14d   |"%rblack)
#     print("+-------------------------+---------------------+")
#     print("|Test image white pixel   |    %14d   |"%cwhite)
#     print("+-------------------------+---------------------+")
#     print("|Test image black pixel   |    %14d   |"%cblack)
#     print("+-------------------------+---------------------+")
#     print("|Totol pixel              |    %14d   |"%n)
#     print("+-------------------------+---------------------+")
#     print("|True Positive            |%18d   |"%TP)
#     print("+-------------------------+---------------------+")
#     print("|False Negative           |%18d   |"%FN)
#     print("+-------------------------+---------------------+")
#     print("|True Negative            |%18d   |"%TN)
#     print("+-------------------------+---------------------+")
#     print("|False Positive           |%18d   |"%FP)
#     print("+-------------------------+---------------------+")
#     print("|Accuracy                 |%18.3f   |"%A)
#     print("+-------------------------+---------------------+")
#     print("|Error rate               |%18.3f   |"%E)
#     print("+-------------------------+---------------------+")
#     print("|Precision                |%18.3f   |"%P)
#     print("+-------------------------+---------------------+")
#     print("|Recall                   |%18.3f   |"%R)
#     print("+-------------------------+---------------------+")
#     print("|F1-score                 |%18.3f   |"%F)
#     print("+-------------------------+---------------------+")


#     fig, axs = plt.subplots(1, 2, constrained_layout=True)
#     axs[0].imshow(GT,'gray')
#     axs[0].set_title('subplot 1')
#     axs[0].set_xlabel('Ground truth')
#     # axs[0].set_ylabel('Damped oscillation')
#     fig.suptitle('Ground truth VS Image segment', fontsize=16)

#     axs[1].imshow(img,'gray')
#     axs[1].set_xlabel('Image segmentation')
#     axs[1].set_title('subplot 2')
#     # axs[1].set_ylabel('Undamped')

#     plt.show()
    
#     return A,E,P,R,F

# #cal confusion_matrix v.2
# #confusion_matrix2(cv.imread('g1 (1).jpg',0),cv.imread('T1.jpg',0),cv.imread('KN1.jpg'))
# def confusion_matrix2(groundtruth,segmentimage,image):
#     '''
#     x(cv.imread('g1 (1).jpg',0),cv.imread('T1.jpg',0),cv.imread('KN1.jpg'))
#     '''
    
#     import cv2 as cv   
#     from matplotlib import pyplot as plt
    
#     fig, axs = plt.subplots(1, 3, constrained_layout=True)
#     axs[0].imshow(groundtruth,'gray')
#     axs[0].set_title('subplot 1')
#     axs[0].set_xlabel('Ground truth')
#     # axs[0].set_ylabel('Damped oscillation')
#     fig.suptitle('Ground truth VS Image segment', fontsize=16)

#     axs[2].imshow(image,'gray')
#     axs[2].set_xlabel('originalimage')
#     axs[2].set_title('subplot 2')
#     # axs[1].set_ylabel('Undamped')

#     axs[1].imshow(segmentimage,'gray')
#     axs[1].set_xlabel('Image segmentation ')
#     axs[1].set_title('subplot 3')
#     plt.show()
    
#     '''
#     from calmat import CM
#     G=cv2.imread('g4 (1).jpg',0)
#     i=cv2.imread('xxx.jpg',0)
#     CM(G,img)
#     '''
#     GT=groundtruth
#     # GT = cv.imread('test.jpg',0)
#     GT = GT/255
#     # plt.imshow(GT,'gray')
#     # plt.show()
#     rwhite = 0
#     rblack = 0

#     [x,y]=GT.shape

#     for j in range(y):
#       for i in range(x):
#           if GT[i,j]==0:
#               rblack=rblack+1
#           else:
#               rwhite=rwhite+1
          

#     img=segmentimage
#     # img = cv.imread('real.jpg',0)
#     img = img/255
#     # plt.imshow(img,'gray')
#     # plt.show()
#     cwhite = 0
#     cblack = 0

#     [x,y]=img.shape

#     for j in range(y):
#       for i in range(x):
#           if img[i,j]==0:
#               cblack=cblack+1
#           else:
#               cwhite=cwhite+1
 



#     ###
#     TP=0
#     TN=0
#     FP=0
#     FN=0
#     for b in range(y):
#         for a in range(x):
#             if(GT[a,b]==1 and img[a,b]==1):
#                 TP=TP+1
#             if(GT[a,b]==0 and img[a,b]==0):
#                 TN=TN+1
#             if(GT[a,b]==1 and img[a,b]==0):
#                 FP=FP+1
#             if(GT[a,b]==0 and img[a,b]==1):
#                 FN=FN+1

        
#     # TP = float(input("True Positive is "))
#     # FN = float(input("False Negative is "))
#     # TN = float(input("True Negative is "))
#     # FP = float(input("False Positive is "))

#     n=TP+FN+TN+FP

#     A=(TP+TN)/n
#     E=(FP+FN)/n
#     P=TP/(TP+FP)
#     R=TP/(TP+FN)
#     F=2*(P*R)/(P+R)
#     print("\n")
    

#     print("                 Confusion Matrix                ")

#     print("+---------------+-------------------------------+")
#     print("|               |           Predicted           |")
#     print("|    Actual     +---------------+---------------+")
#     print("|               |    Positive   |    Negative   |")
#     print("+---------------+---------------+---------------+")
#     print("|   Positive    |%14d |%14d |"%(TP,FN))
#     print("+---------------+---------------+---------------+")
#     print("|   Negative    |%14d |%14d |"%(FP,TN))
#     print("+---------------+---------------+---------------+")


#     print("+-------------------------+---------------------+")
#     print("|Ground truth white pixel |    %14d   |"%rwhite)
#     print("+-------------------------+---------------------+")
#     print("|Ground truth black pixel |    %14d   |"%rblack)
#     print("+-------------------------+---------------------+")
#     print("|Test image white pixel   |    %14d   |"%cwhite)
#     print("+-------------------------+---------------------+")
#     print("|Test image black pixel   |    %14d   |"%cblack)
#     print("+-------------------------+---------------------+")
#     print("|Totol pixel              |    %14d   |"%n)
#     print("+-------------------------+---------------------+")
#     print("|True Positive            |%18d   |"%TP)
#     print("+-------------------------+---------------------+")
#     print("|False Negative           |%18d   |"%FN)
#     print("+-------------------------+---------------------+")
#     print("|True Negative            |%18d   |"%TN)
#     print("+-------------------------+---------------------+")
#     print("|False Positive           |%18d   |"%FP)
#     print("+-------------------------+---------------------+")
#     print("|Accuracy                 |%18.3f   |"%A)
#     print("+-------------------------+---------------------+")
#     print("|Error rate               |%18.3f   |"%E)
#     print("+-------------------------+---------------------+")
#     print("|Precision                |%18.3f   |"%P)
#     print("+-------------------------+---------------------+")
#     print("|Recall                   |%18.3f   |"%R)
#     print("+-------------------------+---------------------+")
#     print("|F1-score                 |%18.3f   |"%F)
#     print("+-------------------------+---------------------+")




#     return A,E,P,R,F

# #treshold image rgb2binaryimage by otsu treshold
# def rgb2bi(img):
#     import cv2
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     # ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#     return th2

# #rename(r'C:\Users\tul\Desktop\New folder',1)
# #if it dont change number,chane 0 to 1000 and return to 0
# def rename(data_path,start):
#     import os
#     path=os.getcwd()
#     #getcwd() returns current working directory of a process.
#     #path to the data folder
#     #data_path =  r'C:\Users\tul\Desktop\testhaha'

#     data_list = os.listdir(data_path)
#     print(data_list)
#     # list all of the name file infoder

#     os.chdir(data_path)
#     #Python method chdir() changes the current working directory 
#     # to the given path.It returns None in all the cases.
#     #The base name of image files

#     for i in range(len(data_list)):
#         img_name=data_list[i]
#         # img_rename=base_name+'_{:05d}'.format(i+2)+'.jpg'
#         img_rename='{:01d}'.format(i+start)+'.png'
#         if not os.path.exists(img_rename):
#             os.rename(img_name,img_rename)
        
#     os.chdir(path)
 
# # conver code.py to .pdf 
# # code2pdf('filename')
# def code2pdf(name):
#     #  name have to be string such as code2pdf('xxx')
#     from fpdf import FPDF 
#     # save FPDF() class into  
#     # a variable pdf 
#     pdf = FPDF()    
#     a='.pdf'
#     p='.py'
#     nameopen=name+p
#     namepdf=nameopen+a
#     # Add a page 
#     pdf.add_page() 
    
#     # set style and size of font  
#     # that you want in the pdf 
#     pdf.set_font("Arial", size = 7) 
    
#     # open the text file in read mode 
#     # f = open("delete2.py", "r") 
#     # x=os.path.basename(__file__)
#     name=name+a
    
#     f = open(nameopen, "r") 
    
#     # insert the texts in pdf 
#     for x in f: 
#         pdf.cell(200, 3, txt = x, ln = 1, align = 'L') 
    
#     # save the pdf with name .pdf 
#     pdf.output(namepdf)
    
# # convert video to frame by frame
# # video2frame('vt.mp4',r'C:\Users\tul\Desktop\lofiimage')
# def video2frame(nameofvideo,directoryforsave,framepersec):
# #nameofvideo have to be .mp4
# # directoryforsave have to r'C:\Users\tul\Desktop\lofiimage'
# # importing libraries 
#     import cv2 
#     import numpy as np 
#     import os 
       
#     # Create a VideoCapture object and read from input file 
#     cap = cv2.VideoCapture(nameofvideo) 
       
#     # Check if camera opened successfully 
#     if (cap.isOpened()== False):  
#       print("false to insert video file") 
#     else:
#         print("complete to insert video file")
       
#     # Read until video is completed 
#     # Returns true if video capturing has been initialized already.
#     count=0
#     y='.jpg'
#     directory = directoryforsave
#     os.chdir(directory) 
    
#     while(cap.isOpened()): 
        
#       # Capture frame-by-frame 
#       ret, frame = cap.read() 
#       if ret == True: 
       
#         # save frame chose freq.
#         if(count%framepersec==0):
#             cv2.imwrite(str(count)+y,frame)
#         # Display the resulting frame 
#         cv2.imshow('Frame', frame) 
       
#         # Press Q on keyboard to  exit 
#         if cv2.waitKey(25) & 0xFF == ord('q'): 
#           break
#         count=count+1
       
#       # Break the loop 
#       else:  
#         break
       
#     # When everything done, release  
#     # the video capture object 
#     cap.release() 
       
#     # Closes all the frames 
#     cv2.destroyAllWindows() 
    
#     '''
#       # cap.read() = returns a bool (True/False). If frame is read correctly, it 
#         will be True. So you can check end of the video by checking this 
#         return value.
#     '''
    
# def showimage(direction):
#     import os
#     import matplotlib.image as mping    
#     import matplotlib.pyplot as plt
#     os.chdir(direction)
#     file=os.listdir(direction)
#     for i in range(len(file)):
#         #chose image
#         print('image',i)
#         img = mping.imread(file[i])
#         #show image finger
#         plt.imshow(img)
#         plt.show()
    

# def pdfwt(img,title):
#     import matplotlib.pyplot as plt
#     plt.figure(figsize=(50,50))
#     plt.imshow(img,cmap='gray')
#     plt.title(title)
#     plt.show()
    
# def imshow(img):
#     import matplotlib.pyplot as plt
#     plt.figure(figsize=(20,20))
#     plt.imshow(img,cmap='gray')
#     plt.show()
    
    
# def imsh(img):
#     import matplotlib.pyplot as plt
#     plt.rcParams.update({'font.size':30})
#     plt.figure(figsize=(20,20))
#     plt.imshow(img,cmap='gray')
#     plt.show()
    
# def s(img):
#     import matplotlib.pyplot as plt
#     plt.figure(figsize=(20,20))
#     plt.imshow(img,cmap='gray')
#     plt.show()
    
# def imsht(img,title,size=22):
#     import matplotlib.pyplot as plt
#     plt.figure(figsize=(20,20))
#     plt.rcParams.update({'font.size': size})
#     plt.imshow(img,cmap='gray')
#     plt.title(title)
#     plt.show()
    
# def montage(img1,img2):
#     import matplotlib.pyplot as plt
#     plt.subplot(121),plt.imshow(img1, cmap = 'gray')
#     plt.title('image1'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img2, cmap = 'gray')
#     plt.title('image2'), plt.xticks([]), plt.yticks([])
#     plt.show()

# def grayread(name):
#     import cv2
#     im=cv2.imread(name,0)
#     return im

# def rgbread(name):
#     import cv2
#     im=cv2.imread(name)
#     im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
#     return im

# # def imre(name):
# #     import cv2
# #     return cv2.imread(name)
    

# def imre(name):
#     import os,cv2
#     from os import path
#     if path.exists(name):
#         return cv2.imread(name)
#     else:
#         print('There are no file name :',name,'@',os.getcwd())


# def bgr2rgb(img):
#     '''img=bgr'''
#     import cv2
#     return cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    
# def rgb2bgr(img):
#     '''img=rgb'''
#     import cv2
#     return cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
    

# def blank():
#     for i in range(101):
#         print("\n")

# #create circle on image  
# #x=circle(img,20,5)
# def circle(img,radius,thickness):
#     import cv2
#     [x,y]=img.shape
#     if x%2==1:
#         x=x+1
#     if y%2==1:
#         y=y+1
#     center_coordinates = (int(y/2),int(x/2))
#     color = (1,1,1)
#     img = cv2.circle(img, center_coordinates, radius, color, thickness)
#     return img

# def plotspectrum(im_fft):
#     import matplotlib.pyplot as plt
#     import numpy as np
#     from matplotlib.colors import LogNorm
#     # A logarithmic colormap
#     plt.imshow(np.abs(im_fft), norm=LogNorm(vmin=5))
#     plt.colorbar()
    
# def rgb2gray(img):
#     import cv2
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     return img

# def reverse(im):
#     im = (255-im)
#     return im
    
# # matchimage('img1.jpg','img2.jpg')
# def imgmatch(img1,img2):
#     import math
#     import numpy as np
#     import cv2 as cv
#     from matplotlib import pyplot as plt
#     from tul import imgshow
    
#     MIN_MATCH_COUNT = 1
#     treshod=0.3
    
#     img1 = cv.imread(img1,1)  # Image
#     img2 = cv.imread(img2,1)  # testnImage
#     # Initiate SIFT detector
#     # sift = cv.SIFT_create()
    
#     sift = cv.xfeatures2d.SIFT_create()
#     # sift = cv2.xfeatures2d.SUFT_create(1000)
    
    
#     # find the keypoints and descriptors with SIFT
#     kp1, des1 = sift.detectAndCompute(img1,None)
#     imgf = cv.drawKeypoints(img1,kp1, None)
#     imgshow(imgf)
    
#     kp2, des2 = sift.detectAndCompute(img2,None)
#     imgs = cv.drawKeypoints(img2,kp2, None)
#     imgshow(imgs)
    
#     FLANN_INDEX_KDTREE = 1
#     index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#     search_params = dict(checks = 100)
#     flann = cv.FlannBasedMatcher(index_params, search_params)
#     matches = flann.knnMatch(des1,des2,k=2)
#     # store all the good matches as per Lowe's ratio test.
#     good = []
#     for m,n in matches:
#         if m.distance < 0.8*n.distance:
#             good.append(m)
            
#     if len(good)>MIN_MATCH_COUNT:
#         src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
#         dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
#         M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
#         matchesMask = mask.ravel().tolist()
#         # see https://ch.mathworks.com/help/images/examples/find-image-rotation-and-scale-using-automated-feature-matching.html for details
#         ss = M[0, 1]
#         sc = M[0, 0]
#         scaleRecovered = math.sqrt(ss * ss + sc * sc)
#         thetaRecovered = math.atan2(ss, sc) * 180 / math.pi
#         print("Calculated scale difference: %.2f \nCalculated rotation difference: %.2f" % ((scaleRecovered), thetaRecovered))
#         h,w,d = img1.shape
#         pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#         dst = cv.perspectiveTransform(pts,M)
#         img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
        
#         val=abs(1-scaleRecovered)   
#         if val>treshod:
#             print('It is not match')
#         else:
#             print("it is match")
        
#     else:
#         print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
#         matchesMask = None
    
        
#     draw_params = dict(matchColor = (0,255,0), # draw matches in green color
#                        singlePointColor = None,
#                        matchesMask = matchesMask, # draw only inliers
#                        flags = 2)
    
#     img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    
#     imgshow(img3)       
    
# def showflag(name):
#     flags = [i for i in dir(name) if i.startswith('COLOR_')]

# def imwr(name,img):
#     '''image write function
#     name=name(+.jpg)
#     img=rgb,bgr,gray'''
#     import cv2
#     # name=name+'.png'
#     name=name
#     cv2.imwrite(name,img)
        
    
# def pad(img):
#     import cv2
#     color = [0,0,0] 
#     top, bottom, left, right = [1]*4
#     img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
#     return  img_with_border

# def Createfolder(name):        
#     import os
#     if name=='d':
#         os.chdir('C:/Users/tul/Desktop')
#     else:
#         parent_dir = "C:/Users/tul/Desktop/"
#         path = os.path.join(parent_dir, name) 
#         os.mkdir(path) 
#         print("Directory '% s' created" %name) 
    
# def Desktop(name):
#     import os
#     parent_dir="C:/Users/tul/Desktop/"
#     path=os.path.join(parent_dir,name)
#     os.chdir(path)
#     print('Directory :',os.getcwd())
    
# def chfo_q(name):
#     import os
#     parent_dir="C:/Users/tul/Desktop/"
#     path=os.path.join(parent_dir,name)
#     os.chdir(path)
    
# def chfod(name='Desktop'):
#     import os
#     parent_dir="C:/Users/tul"
#     path=os.path.join(parent_dir,name)
#     os.chdir(path)
    
# def sound():
#     import os
#     import playsound
#     os.chdir(r'C:\Users\tul')
#     from playsound import playsound
#     playsound('y2mate.com - Pet the bop cat MEME.mp3')
    
# def crbr(x,y):
#     '''create black image 
#        x,y is int
#     '''
#     from numpy import zeros
#     return zeros([y,x])


# def imsp(img):
#     '''im multiply by threshold in range 0-1
#     '''
#     import cv2
#     import numpy as np
#     img1gray = rgb2gray(img)
#     ttt=img1gray/img1gray.max()
#     r,g,b=cv2.split(img)
#     red=r*ttt
#     green=g*ttt
#     blue=b*ttt
#     im=cv2.merge([red,green,blue])
#     im2 = im.astype(np.uint8)
#     return im2

# def imgxmask(img,mask):
#     '''image*mask image=rgb,mask=[0,1]'''
#     import cv2
#     import numpy as np
#     r,g,b=cv2.split(img)
#     red=mask*r
#     green=mask*g
#     blue=mask*b
#     im=cv2.merge([red,green,blue])
#     im2=im.astype(np.uint8)
#     return im2
    
    

# def skin(img):
#     '''skin detection function
#     img = bgrimg
#     '''
#     import cv2
#     import numpy as np
#     img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     kernel5=np.array(([0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]),np.uint8)

#     HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17,170,255)) 
#     HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, kernel5)
    
#     img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
#     YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
#     YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, kernel5)
    
#     global_mask=cv2.bitwise_and(YCrCb_mask,HSV_mask)
#     global_mask=cv2.medianBlur(global_mask,3)
#     global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4,4), np.uint8))
    
#     return global_mask

# def imth(img):
#     ''' thresholding by otsu 
#     img=grayimage'''
#     import cv2
#     ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     return th2


# def imma(img):
#     '''img=bgr'''
#     from tul import skin
#     import numpy as np
#     import cv2
    
#     mask=skin(img)
    
#     mask=mask/mask.max()
#     m = mask.astype(np.uint8)
    
#     blue, green, red = cv2.split(img)
#     b=blue*m
#     g=green*m
#     r=red*m
    
#     x=cv2.merge([b,g,r])
#     return x


# def imdilate(img,kernel=5,r=1):
#     '''dilation image
#     img=binary
#     kernel=int
#     r=round default=1'''
#     import cv2
#     import numpy as np
    
#     kernel = np.ones((kernel,kernel),np.uint8)
#     return cv2.dilate(img,kernel,iterations = r)

# def im_cofu_ma(GT,img):
#     from matplotlib import pyplot as plt

#     '''
#     from calmat import CM
#     G=cv2.imread('g4 (1).jpg',0)
#     i=cv2.imread('xxx.jpg',0)
#     CM(G,img)
#     '''
    
#     # GT = cv.imread('test.jpg',0)
#     GT = GT/255
#     # plt.imshow(GT,'gray')
#     # plt.show()
#     rwhite = 0
#     rblack = 0

#     [x,y]=GT.shape

#     for j in range(y):
#       for i in range(x):
#           if GT[i,j]==0:
#               rblack=rblack+1
#           else:
#               rwhite=rwhite+1
          


#     # img = cv.imread('real.jpg',0)
#     img = img/255
#     # plt.imshow(img,'gray')
#     # plt.show()
#     cwhite = 0
#     cblack = 0

#     [x,y]=img.shape

#     for j in range(y):
#       for i in range(x):
#           if img[i,j]==0:
#               cblack=cblack+1
#           else:
#               cwhite=cwhite+1
 



#     ###
#     TP=0
#     TN=0
#     FP=0
#     FN=0
#     for b in range(y):
#         for a in range(x):
#             if(GT[a,b]==1 and img[a,b]==1):
#                 TP=TP+1
#             if(GT[a,b]==0 and img[a,b]==0):
#                 TN=TN+1
#             if(GT[a,b]==1 and img[a,b]==0):
#                 FP=FP+1
#             if(GT[a,b]==0 and img[a,b]==1):
#                 FN=FN+1

        
#     # TP = float(input("True Positive is "))
#     # FN = float(input("False Negative is "))
#     # TN = float(input("True Negative is "))
#     # FP = float(input("False Positive is "))

#     n=TP+FN+TN+FP

#     A=(TP+TN)/n
#     E=(FP+FN)/n
#     P=TP/(TP+FP)
#     R=(TP)/(TP+FN)
#     F=2*(P*R)/(P+R)
#     print("\n")
                 

#     print("                 Confusion Matrix                ")

#     print("+---------------+-------------------------------+")
#     print("|               |           Predicted           |")
#     print("|    Actual     +---------------+---------------+")
#     print("|               |    Positive   |    Negative   |")
#     print("+---------------+---------------+---------------+")
#     print("|   Positive    |%14d |%14d |"%(TP,FN))
#     print("+---------------+---------------+---------------+")
#     print("|   Negative    |%14d |%14d |"%(FP,TN))
#     print("+---------------+---------------+---------------+")


#     print("+-------------------------+---------------------+")
#     print("|Ground truth white pixel |    %14d   |"%rwhite)
#     print("+-------------------------+---------------------+")
#     print("|Ground truth black pixel |    %14d   |"%rblack)
#     print("+-------------------------+---------------------+")
#     print("|Test image white pixel   |    %14d   |"%cwhite)
#     print("+-------------------------+---------------------+")
#     print("|Test image black pixel   |    %14d   |"%cblack)
#     print("+-------------------------+---------------------+")
#     print("|Totol pixel              |    %14d   |"%n)
#     print("+-------------------------+---------------------+")
#     print("|True Positive            |%18d   |"%TP)
#     print("+-------------------------+---------------------+")
#     print("|False Negative           |%18d   |"%FN)
#     print("+-------------------------+---------------------+")
#     print("|True Negative            |%18d   |"%TN)
#     print("+-------------------------+---------------------+")
#     print("|False Positive           |%18d   |"%FP)
#     print("+-------------------------+---------------------+")
#     print("|Accuracy                 |%18.3f   |"%A)
#     print("+-------------------------+---------------------+")
#     print("|Error rate               |%18.3f   |"%E)
#     print("+-------------------------+---------------------+")
#     print("|Precision                |%18.3f   |"%P)
#     print("+-------------------------+---------------------+")
#     print("|Recall                   |%18.3f   |"%R)
#     print("+-------------------------+---------------------+")
#     print("|F1-score                 |%18.3f   |"%F)
#     print("+-------------------------+---------------------+")


#     # fig, axs = plt.subplots(1, 2, constrained_layout=True)
    
#     # axs[0].imshow(GT,'gray')
#     # axs[0].set_title('subplot 1')
#     # axs[0].set_xlabel('Ground truth')
#     # # axs[0].set_ylabel('Damped oscillation')
#     # fig.suptitle('Ground truth VS Image segment', fontsize=16)

#     # axs[1].imshow(img,'gray')
#     # axs[1].set_xlabel('Image segmentation')
#     # axs[1].set_title('subplot 2')
#     # # axs[1].set_ylabel('Undamped')
#     # plt.show()
#     plt.figure(figsize=(20,20))
#     plt.rcParams.update({'font.size': 40})

#     plt.subplot(121),plt.imshow(GT, cmap = 'gray')
#     plt.title('Groundthruth'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img, cmap = 'gray')
#     plt.title('image'), plt.xticks([]), plt.yticks([])
#     plt.show()
    
    
#     value=[rwhite,rblack,cwhite,cblack,TP,FN,TN,FP,A,E,P,R,F]
#     return value

# def timenow():
#     import datetime
#     print(datetime.datetime.now().strftime("%c"))
    
    
# def chfam(path):
#     '''path='all1'
#        change all file in folder jpg --> png
#     '''
#     import os
#     chfo(path)
#     for item in os.listdir(os.getcwd()):
#         x = item.split(".")
#         if x[1]=='jpg':
#             print(item,'==>',x[0]+'.png')
#             os.rename(item,x[0]+'.png')
#         chfo(path)
        
        
        
# def bold(img):
#       import numpy as np
#       import cv2
#       kernel5=np.ones((3,3),np.uint8)
#       dilation = cv2.dilate(img,kernel5,iterations = 10)
#       return dilation
      
# def findline(img):
#     import numpy as np
#     from numpy import zeros
#     import cv2
#     axis=[]
#     for i in range(img.shape[0]):
#         for j in range(img.shape[1]):
#             if img[i,j]!=0:
#                 print(i,j)
#                 axis.append([i,j])
#                 break
#     mod=zeros([img.shape[0],img.shape[1]])
#     for k,l in axis:
#         mod[k,l]=1
#     kernel5=np.ones((3,3),np.uint8)
#     dilation1 = cv2.dilate(mod,kernel5,iterations = 5)
    
#     xx=[]
#     yx=[]
#     img2=np.transpose(img)
#     axis2=[]
#     for i in range(img2.shape[0]):
#         for j in range(img2.shape[1]):
#             if img2[i,j]!=0:
#                 print(i,j)
#                 axis2.append([i,j])
#                 break
#     mod=zeros([img2.shape[0],img2.shape[1]])
#     for k,l in axis2:
#         xx.append(k)
#         yx.append(img2.shape[0]-l)
#         mod[k,l]=1
#     kernel5=np.ones((3,3),np.uint8)
#     dilation2 = cv2.dilate(mod,kernel5,iterations = 5)

#     img3=np.flip(img,1)
#     axis=[]
#     for i in range(img3.shape[0]):
#         for j in range(img3.shape[1]):
#             if img3[i,j]!=0:
#                 print(i,j)
#                 axis.append([i,j])
#                 break
#     mod=zeros([img3.shape[0],img3.shape[1]])
#     for k,l in axis:
#         mod[k,l]=1
#     kernel5=np.ones((3,3),np.uint8)
#     dilation3 = cv2.dilate(mod,kernel5,iterations = 5)
    
#     return dilation1,np.transpose(dilation2),np.flip(dilation3,1),xx,yx

# def findpeak(signal):
#     xlst=[]
#     for i in range(len(signal)-1):
#         if  signal[i+1]<signal[i] and signal[i]>signal[i-1]:
#             #print(i)
#             xlst.append(i)
#     return xlst
            
# def findpeak2(signal):
#     xlst=[]
#     for i in range(len(signal)-1):
#         if  signal[i+1]<signal[i] and signal[i]>signal[i-1]:
#             #print(i)
#             xlst.append(signal[i])
#     return xlst

# def findflat(signal):
#     xlst=[]
#     for i in range(len(signal)-1):
#         if  signal[i-1]==signal[i]:
#             print(i)
#             xlst.append(i)
            
# def img2signal(img):
#     value=[]
#     for i in range(img.shape[1]):
#         for j in range(img.shape[0]):
#             if img[j,i]!=0:
#                 value.append([i,j])
#                 break
#     x=[]
#     y=[]
#     for a,b in value:
#         x.append(a)
#         y.append(img.shape[0]-b)
#     return x,y

# def median(lst):
#     return lst[round(len(lst)/2)-1]

# def topfinger(imgname,numberoffinger):
#        #import os
#        #os.chdir(r'C:\Users\tul\Desktop')
#        #from tul import *
#        #output=topfinger('0.jpg',1)
#        #imsh(output)
#     import cv2
#     import matplotlib.pyplot as plt
#     import os
#     os.chdir(r'C:\Users\tul\Desktop')
#     from tul import imre,imma,rgb2gray,imsh,img2signal,median,imgxmask,bgr2rgb
#     import numpy as np
#     from numpy import zeros
#     import more_itertools as mit
    
#     ima=imre(imgname)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  y[i-1]==y[i] or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5:
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     chose=[]
#     while len(chose)<numberoffinger:
#         maxnum=0
#         for i in range(len(newlst2)-1):    #find max of len num in list
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    #show position of max len
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   #assign and delete value from list
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([th2.shape[0],th2.shape[1]])
#     black=zeros([th2.shape[0],th2.shape[1]])
#     for n,m in pos:
#         for i in range(n-300,n+300):
#             if n-300<0 or n+300>black.shape[1]:
#                 continue
#             for j in range(m,m+600):
#                 if m+600>black.shape[0]:
#                     continue
#                 black[j,i]=1
#     imsh(bgr2rgb((imgxmask(ima,black))))
#     black=black*255
#     return black

# def create_ractangular(img,pos):
#     for n,m in pos:
#         for i in range(n-300,n+300):
#             if n-300<0 or n+300>img.shape[1]:
#                 continue
#             for j in range(m-200,m+600):
#                 if m+600>img.shape[0]:
#                     continue
#                 img[j,i]=1
#     return img


# def findfing1(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,imsh,img2signal,findpeak,median,create_ractangular,imgxmask,bgr2rgb

#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     black=create_ractangular(black,pos)    
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# def im_cofu_ma2(GT,img):
#     GT = GT/255
#     rwhite = 0
#     rblack = 0
#     [x,y]=GT.shape
#     for j in range(y):
#       for i in range(x):
#           if GT[i,j]==0:
#               rblack=rblack+1
#           else:
#               rwhite=rwhite+1
#     img = img/255
#     cwhite = 0
#     cblack = 0
#     [x,y]=img.shape
#     for j in range(y):
#       for i in range(x):
#           if img[i,j]==0:
#               cblack=cblack+1
#           else:
#               cwhite=cwhite+1
#     TP=0;TN=0;FP=0;FN=0
#     for b in range(y):
#         for a in range(x):
#             if(GT[a,b]==1 and img[a,b]==1):
#                 TP=TP+1
#             if(GT[a,b]==0 and img[a,b]==0):
#                 TN=TN+1
#             if(GT[a,b]==1 and img[a,b]==0):
#                 FP=FP+1
#             if(GT[a,b]==0 and img[a,b]==1):
#                 FN=FN+1
#     n=TP+FN+TN+FP
#     A=(TP+TN)/n
#     E=(FP+FN)/n
#     if (TP+FP)==0:
#         P=0
#     else:
#         P=TP/(TP+FP)
#     if (TP+FN)==0:
#         R=0
#     else:
#         R=(TP)/(TP+FN)
#     if (P+R)==0:
#         F=0
#     else:
#         F=2*(P*R)/(P+R)
#     value=[rwhite,rblack,cwhite,cblack,TP,FN,TN,FP,A,E,P,R,F]
#     return value


  
# def create_ractangular2(img,pos,width1=300,width2=300,height1=200,height2=600):
#     for n,m in pos:
#         if n-width1<0:
#             left=0
#         else:
#             left=n-width1
#         #check right
#         if n+width2>img.shape[1]:
#             right=img.shape[1]
#         else:
#             right=n+width2
#         #check up
#         if m-height1<0:
#             top=0
#         else:
#             top=m-height1
#         #check down
#         if m+height2>img.shape[0]:
#             bellow=img.shape[0]
#         else:
#             bellow=m+height2
#         # print(left,right,top,bellow)

#         for i in range(left,right):
#             for j in range(top,bellow):
#                 img[j,i]=1
#     return img

# def findfing3(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)

#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     black=create_ractangular2(black,pos)    
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# def find_LH(xaxis):
#     handlength=xaxis[-1]-xaxis[0]
#     afingerlength=round(handlength/4)
#     width1=width2=round(afingerlength/2)
#     afingerheight=round(1.75197367*afingerlength)
#     height1=round(0.3*afingerheight)
#     height2=round(0.7*afingerheight)
#     return width1,width2,height1,height2

# def findfing4(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     width1,width2,height1,height2=find_LH(x)
#     black=create_ractangular2(black,pos,width1,width2,height1,height2)       
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask


# def find_LH2(xaxis):
#     handlength=xaxis.shape[-1]-xaxis.shape[0]
#     afingerlength=1.2*round(handlength/4)
#     width1=width2=round(1.75197367*afingerlength/2)
#     afingerheight=round(1.75197367*afingerlength)
#     height1=round(0.2*afingerheight)
#     height2=round(0.8*afingerheight)
#     return width1,width2,height1,height2

# def find_LH3(xaxis):
#     handlength=xaxis[-1]-xaxis[0]
#     afingerlength=round(handlength/4)
#     width1=width2=round(1.75197367*0.7071067811865476*afingerlength/4)
#     afingerheight=round(1.75197367*afingerlength)
#     height1=round(0.2*afingerheight)
#     height2=round(0.8*afingerheight)
#     return width1,width2,height1,height2

# def findfing5(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb,find_LH2
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     width1,width2,height1,height2=find_LH2(x)
#     black=create_ractangular2(black,pos,width1,width2,height1,height2)       
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# def pointofhand1(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([th2.shape[0],th2.shape[1]])
#     for p,q in pos:
#         black[q,p]=1
#     imsh(0.1*gfing+20*bold(black))
#     x=0.1*gfing+20*bold(black)
#     xx=x*(255/x.max())
#     return xx


# def findfing2(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular,imgxmask,bgr2rgb
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)

#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     black=create_ractangular(black,pos)    
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# def findfing6(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb,find_LH2
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     width1,width2,height1,height2=find_LH3(x)
#     black=create_ractangular2(black,pos,width1,width2,height1,height2)       
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# def pointofhand2(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([th2.shape[0],th2.shape[1]])
#     for p,q in pos:
#         black[q,p]=1
#     imsh(0.1*gfing+20*bold(black))
#     x=0.1*gfing+20*bold(black)
#     xx=x*(255/x.max())
#     return xx


# def findfing7(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb,find_LH2
#     import skimage.morphology, skimage.data
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     width1,width2,height1,height2=find_LH2(x)
#     black=create_ractangular2(black,pos,width1,width2,height1,height2)       
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# def skindetection2(name):
#     import cv2
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     return th2

# def skindetection3(name):
#     import cv2
#     import skimage
#     import numpy as np
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     return th2

# def skindetection4(name):
#     import cv2
#     import skimage
#     import numpy as np
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     labels = skimage.measure.label(th2)
#     black=np.zeros([th2.shape[0],th2.shape[1]])
#     for rnd in range(1,labels.max()+1):
#         canvas=np.zeros([th2.shape[0],th2.shape[1]])
#         for i in range(th2.shape[1]):
#             for j in range(th2.shape[0]):
#                 if labels[j,i]==rnd:
#                     canvas[j,i]=255
#         if belch(canvas):
#             black=black+canvas
#     return black

# #def list_encoder(lst):
# def lsten(lst,name):
#     with open(name, "w") as file:
#             file.write(str(lst))
            
# #def list_decoder(lst):
# def lstde(name):
#     with open(name, "r") as file:
#         data2 = eval(file.readline())
#     return data2





# def checkpoint(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     from tul import imre,imma,rgb2gray,img2signal,findpeak,median,create_ractangular2,imgxmask,bgr2rgb,find_LH2
#     import skimage.morphology, skimage.data

#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(100,100))  
#     #Threshold
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     #fill hole
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     x,y=img2signal(th2)
#     ylst=[]
#     for i in range(len(y)-1):
#         if  (y[i-1]==y[i]   
#              or y[i-1]==y[i]+1 or y[i-1]==y[i]+2 or y[i-1]==y[i]+3 or y[i-1]==y[i]+4 or y[i-1]==y[i]+5 or y[i-1]==y[i]+6 or y[i-1]==y[i]+7 or y[i-1]==y[i]+8 or y[i-1]==y[i]+9 or y[i-1]==y[i]+10 
#              or y[i-1]==y[i]-1 or y[i-1]==y[i]-2 or y[i-1]==y[i]-3 or y[i-1]==y[i]-4 or y[i-1]==y[i]-5 or y[i-1]==y[i]-6 or y[i-1]==y[i]-7 or y[i-1]==y[i]-8 or y[i-1]==y[i]-9 or y[i-1]==y[i]-10): 
#             ylst.append(y[i])
#     group=[list(group) for group in mit.consecutive_groups(ylst)]
#     newlst=[]
#     for i in range(len(group)):
#         if len(group[i])!=1 and len(group[i])!=2 and len(group[i])!=3:
#             newlst.append(group[i])
#     newlst2=[]
#     for i in range(len(newlst)-1):
#         newlst2.append(newlst[i])
#     sh=[len(n) for n in newlst2]
#     number=len(findpeak(sh))
#     chose=[]
#     while len(chose)<number:
#         maxnum=0
#         for i in range(len(newlst2)-1):   
#             if len(newlst2[i])>=maxnum:
#                 maxnum=len(newlst2[i])
#         for i in range(len(newlst2)-1):    
#             if len(newlst2[i])==maxnum:
#                 position=i
#         chose.append(newlst2.pop(position))   
#     yaxis=[median(num) for num in chose]
#     dictionary=dict(zip(y,x))
#     pos=[]
#     for i in yaxis:
#         pos.append([dictionary[i],th2.shape[0]-i])
#     black=zeros([fing.shape[0],fing.shape[1]])
#     width1,width2,height1,height2=find_LH2(x)
#     chfo('hand_point_of_finger_GT')
#     pos=lstde(name.split('.')[0])
#     #2Daxis --> 1Daxis
#     for num in range(len(pos)):
#         pos[num][1]=black.shape[0]-pos[num][1]
#     black=create_ractangular2(black,pos,width1,width2,height1,height2)       
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     return outputmask
#     #output=imgxmask(ima,outputmask)


# def crop_image(name,pos,width1=300,width2=300,height1=200,height2=600):
#     import cv2
#     import os
#     img=cv2.imread(name)
#     c='C:\\Users\\tul\\Desktop\\'+'image'+name.split('.')[0]
#     os.makedirs(c)
#     #check position in range
#     cot=1
#     for n,m in pos:
#         if n-width1<0:
#             left=0
#         else:
#             left=n-width1
#         #check right
#         if n+width2>img.shape[1]:
#             right=img.shape[1]
#         else:
#             right=n+width2
#         #check up
#         if m-height1<0:
#             top=0
#         else:
#             top=m-height1
#         #check down
#         if m+height2>img.shape[0]:
#             bellow=img.shape[0]
#         else:
#             bellow=m+height2
#         print(left,right,top,bellow)
#         new=img[top:bellow,left:right] #[y,x]
#         chfo('image'+name.split('.')[0])
#         imwr(str(cot)+'.jpg',new)
#         cot=cot+1
        
# #chose only object that connected with bellow down
# #def bellow_check(img):
# def belch(img):
#     for i in range(img.shape[1]):
#     #print(kernel5[(kernel5.shape[0]-1),i])
#         if img[(img.shape[0]-1),i]!=0:
#             return 1
#     return 0

# #def left_check(img):
# def lefch(img):
#     for i in range(img.shape[0]):
#         if img[i,0]!=0:
#             return 0
#     return 1

# #def right_check(img):
# def ritch(img):
#     r=img.shape[1]-1
#     for i in range(img.shape[0]):
#         if img[i,r]!=0:
#             return 0
#     return 1


# def findfing9(name):
#     import cv2
#     import numpy as np
#     import math
#     import matplotlib.pyplot as plt
#     import statistics as st
#     from numpy import zeros
#     import more_itertools as mit
#     import skimage.morphology, skimage.data
#     from skimage import measure
#     from tul import imre,imma,rgb2gray,img2signal,findpeak2,create_ractangular2,imgxmask,find_LH2
#     ima=imre(name)
#     fing=imma(ima)
#     gfing=rgb2gray(fing)
#     blur = cv2.blur(gfing,(50,50))  
#     ret2,th2 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     labels = skimage.morphology.label(~th2)
#     labelCount = np.bincount(labels.ravel())
#     background = np.argmax(labelCount)
#     th2[labels != background] = 255
#     labels = measure.label(th2)
#     black=np.zeros([th2.shape[0],th2.shape[1]])
#     for rnd in range(1,labels.max()+1):
#         canvas=np.zeros([th2.shape[0],th2.shape[1]])
#         for i in range(th2.shape[1]):
#             for j in range(th2.shape[0]):
#                 if labels[j,i]==rnd:
#                     canvas[j,i]=255
#         if belch(canvas) and ritch(canvas) and lefch(canvas):
#             black=black+canvas
#     x,y=img2signal(black)
#     ylst=[] 
#     for i in range(len(y)-1):
#         if  (y[i]==y[i-1]): 
#             ylst.append(y[i-1])
#     l=[] 
#     for num in range(len(ylst)):
#         if ylst[num]!=ylst[num-1]:
#             l.append(ylst[num])
#     yaxis=findpeak2(l)
#     pos=[]
#     for i in yaxis:
#         lst=[]
#         for index in range(len(y)):
#             if y[index]==i:
#                 lst.append(index+x[0])
#         pos.append([lst[round(len(lst)/2)-1],th2.shape[0]-i])

#     black=zeros([th2.shape[0],th2.shape[1]])
#     for p,q in pos:
#         black[q,p]=1
#     x=0.1*gfing+20*bold(black)
#     width1,width2,height1,height2=find_LH2(x)
#     black=zeros([fing.shape[0],fing.shape[1]])
#     black=create_ractangular2(black,pos,width1,width2,height1,height2)
#     output=imgxmask(ima,black)
#     black=(black/black.max()).astype(np.uint8)
#     th2=(th2/th2.max()).astype(np.uint8)
#     outputmask=cv2.bitwise_and(th2,black)
#     output=imgxmask(ima,outputmask)
#     return outputmask

# #distance of error
# def disor3(true_pnt,test_pnt):
#     import numpy as np
#     for i in range(len(test_pnt)):
#         if i<=len(true_pnt)-1:
#             dis1=true_pnt[i][0]-test_pnt[i][0]
#             dis2=true_pnt[i][1]-test_pnt[i][1]
#             distance=np.sqrt(dis1**2+dis2**2)
#             print('distance = %8.3f '%distance, end=" ")
#             # x-axis
#             if true_pnt[i][0]>test_pnt[i][0]:
#                 print('←','%4d'%(true_pnt[i][0]-test_pnt[i][0]), end=" ")
#             elif test_pnt[i][0]==true_pnt[i][0]:
#                 print('0', end=" ")
#             else:
#                 print('→','%4d'%(np.abs(true_pnt[i][0]-test_pnt[i][0])), end=" ")
#             # y-axis
#             if true_pnt[i][1]>test_pnt[i][1]:
#                 print('↓','%4d'%(true_pnt[i][1]-test_pnt[i][1]))
#             elif test_pnt[i][1]-true_pnt[i][1]==0:
#                 print('0')
#             else:
#                 print('↑','%4d'%(np.abs(true_pnt[i][1]-test_pnt[i][1])))
#         else:
#             return
        
# #point evaluate
# def operate(name,test_pnt):    
#     import matplotlib.pyplot as plt
#     xname='x'+name
#     yname='y'+name
#     chfo('hand_point_of_finger_GT')
#     true_pnt=lstde(name)
#     X=[];Y=[];
#     for x,y in true_pnt:
#         X.append(x)
#         Y.append(y)
#     A=[];B=[];
#     for x,y in test_pnt:
#         A.append(x)
#         B.append(y)
#     chfo('ydata')
#     x=lstde(xname)
#     y=lstde(yname)
#     #chfo('')
#     plt.figure(figsize=(10,15))
#     plt.grid()
#     plt.plot(x,y)
#     plt.plot(X,Y,'o',color='b')
#     plt.plot(A,B,'x',color='red')
#     plt.savefig(name)
#     disor3(true_pnt,test_pnt)



# def disor4(name,test_pnt,savelocation='C:\\Users\\tul\\Desktop'):
#     # disor4('86.png',[[1014, 1306],[1373, 640],[1603, 449],[1777, 420]])
#     import numpy as np
#     from tul import lstde
#     import os
#     import matplotlib.pyplot as plt
#     chfo('hand_point_of_finger_GT')
#     true_pnt=lstde(name.split('.')[0])
#     X=[];Y=[];
#     for x,y in true_pnt:
#         X.append(x)
#         Y.append(y)
#     A=[];B=[];
#     for x,y in test_pnt:
#         A.append(x)
#         B.append(y)
#     chfo('ydata')
#     name=name.split('.')[0]
#     xname='x'+name
#     yname='y'+name
#     x=lstde(xname)
#     y=lstde(yname)
#     os.chdir(savelocation)
#     plt.figure(figsize=(10,15))
#     plt.grid()
#     plt.plot(x,y)
#     plt.plot(X,Y,'o',color='b')
#     plt.plot(A,B,'x',color='red')
#     plt.savefig(name)
#     for i in range(len(test_pnt)):
#         if i<=len(true_pnt)-1:
#             dis1=true_pnt[i][0]-test_pnt[i][0]
#             dis2=true_pnt[i][1]-test_pnt[i][1]
#             distance=np.sqrt(dis1**2+dis2**2)
#             print('distance = %8.3f '%distance, end=" ")
#             # x-axis
#             if true_pnt[i][0]>test_pnt[i][0]:
#                 print('←','%4d'%(true_pnt[i][0]-test_pnt[i][0]), end=" ")
#             elif test_pnt[i][0]==true_pnt[i][0]:
#                 print('0', end=" ")
#             else:
#                 print('→','%4d'%(np.abs(true_pnt[i][0]-test_pnt[i][0])), end=" ")
#             # y-axis
#             if true_pnt[i][1]>test_pnt[i][1]:
#                 print('↓','%4d'%(true_pnt[i][1]-test_pnt[i][1]))
#             elif test_pnt[i][1]-true_pnt[i][1]==0:
#                 print('0')
#             else:
#                 print('↑','%4d'%(np.abs(true_pnt[i][1]-test_pnt[i][1])))
#         else:
#             return

# def cEMH(text):
#     e,h,m=0,0,0
#     for i in text:
#         if i=='e':
#             e=e+1
#         elif i=='h':
#             h=h+1
#         elif i=='m':
#             m=m+1
#     print('e =',e,'m =',m,'h =',h)
    

# def multithreshold(img):
#     import numpy as np
#     gray=rgb2gray(img)
#     canvas=np.zeros([gray.shape[0],gray.shape[1]])
#     for i in range(gray.shape[0]):
#         for j in range(gray.shape[1]):
#             if gray[i][j]<round((1/3)*256):
#                 canvas[i][j]=0
#             elif gray[i][j]<round((2/3)*256):
#                 canvas[i][j]=1
#             else:
#                 canvas[i][j]=2
#     return canvas

# def otsu(img):
#     ''' thresholding by otsu 
#     img=grayimage'''
#     import cv2
#     ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     return th2
        
# def p(data):
#     print(data)

# # rotate image
# import imutils
# rimg = imutils.rotate(Red, angle=12)


# # def evaluatefunction(Groundtruthfolder,imagefolder,resulution=2):
# # def confusion_matrix(GT,img):
# # def confusion_matrix2(groundtruth,segmentimage,image):
# # def rgb2bi(img):
# # def rename(data_path,start):
# # def code2pdf(name):
# # def video2frame(nameofvideo,directoryforsave,framepersec):
# # def showimage(direction):
# # def pdfwt(img,title):
# # def imshow(img):
# # def imsh(img):
# # def s(img):
# # def imsht(img,title,size=22):
# # def montage(img1,img2):
# # def grayread(name):
# # def rgbread(name):
# # def imre(name):
# # def bgr2rgb(img):
# # def rgb2bgr(img):
# # def blank():
# # def circle(img,radius,thickness):
# # def plotspectrum(im_fft):
# # def rgb2gray(img):
# # def reverse(im):
# # def imgmatch(img1,img2):
# # def showflag(name):
# # def imwr(name,img):
# # def pad(img):
# # def Createfolder(name):        
# # def Desktop(name):
# # def chfo_q(name):
# # def chfod(name='Desktop'):
# # def sound():
# # *def crbr(x,y):
# # *def imsp(img):
# # *def imgxmask(img,mask):
# # *def skin(img):
# # *def imth(img):
# # *def imma(img):
# # *def imdilate(img,kernel=5,r=1):
# # def im_cofu_ma(GT,img):
# # *def timenow():
# # def chfam(path):
# # *def bold(img):
# # *def findline(img):
# # *def findpeak(signal):
# # *def findpeak2(signal):
# # *def findflat(signal): 
# # def img2signal(img):
# # def median(lst):
# # def topfinger(imgname,numberoffinger):
# # def create_ractangular(img,pos):
# # def findfing1(name):
# # def im_cofu_ma2(GT,img):
# # def create_ractangular2(img,pos,width1=300,width2=300,height1=200,height2=600):
# # def findfing3(name):
# # def find_LH(xaxis):
# # def findfing4(name):
# # def find_LH2(xaxis):
# # def find_LH3(xaxis):
# # def findfing5(name):
# # def pointofhand1(name):
# # def findfing2(name):
# # def findfing6(name):
# # def pointofhand2(name):
# # def findfing7(name):
# # def skindetection2(name):
# # def skindetection3(name):
# # def skindetection4(name):
# # *def lsten(lst,name):
# # *def lstde(name):
# # def checkpoint(name):
# # *def crop_image(name,pos,width1=300,width2=300,height1=200,height2=600):
# # def belch(img):
# # def ritch(img):
# # def findfing9(name):
# # def disor3(true_pnt,test_pnt):
# # def operate(name,test_pnt):    
# # def disor4(name,test_pnt,savelocation='C:\\Users\\tul\\Desktop'):
# # def cEMH(text):
# # *def multithreshold(img):
# # def otsu(img):
# # def p(data):