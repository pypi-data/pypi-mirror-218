import json,os
import pandas as pd
import pymysql


from hdfs3 import HDFileSystem
from fastparquet import write,ParquetFile



hdfsFlag = "hdfs://"
atomicFlag = "dps_atomic_spark_sink_sinkparquet"

class MissionData:
    
     __missionTuple= None
     __definition = None

     __host = ""
     __port = 3306
     __user = "root"
     __password = "root"
     __database = ""
     __charset="utf8"
        
     
     def initDb(self,host,port,user,passwd,db):
         self.__host=host
         self.__port=port
         self.__user=user
         self.__password=passwd
         self.__database=db
        
     def getMysqlConn(self):
        conn=pymysql.connect(host=self.__host,port=self.__port,user=self.__user,password=self.__password,database=self.__database,charset=self.__charset)
        print("get mysql connection :{0}".format(conn))
        return conn

            
     def setMission(self,missionCode):
        conn=self.getMysqlConn()
        cusor=conn.cursor()
        cusor.execute("select * from b_mission where mission_code=%s",missionCode)
        data=cusor.fetchone()
        self.__missionTuple=data
        self.__definition=json.loads(data[11])
        cusor.close()
        conn.close()
     def showNodes(self):
        nodes=self.__definition['nodes']
        hdfsPath = ""
        for i in nodes:
            nodeData = i['data']
            if(nodeData['id']=='startNode'):
                continue
            operations = nodeData['operations']
            if(nodeData['operations'][0]['operationDef']['id']==atomicFlag):
                print(i['id'],nodeData['operationGroupName'],nodeData['operations'][0]['params'][0]['operationParamValue'])
                
        
   
     #  下载数据到jupter 本地
     def getDataForNodeId(self,nodeId,localPath):
        print("下载文件到本地",nodeId,localPath)
        nodes=self.__definition['nodes']
        hdfsPath = ""
        for i in nodes:
            if(i['id']==nodeId):
                nodeData = i['data']
                if(nodeData['operations'][0]['operationDef']['id']==atomicFlag):
                    hdfsPath = nodeData['operations'][0]['params'][0]['operationParamValue']
                    break
        self.getHdfsData(hdfsPath,localPath)   
        
     # 获取 Hdfs 文件
     def getHdfsData(self,hdfsFullPath,localPath):
        print("获取 Hdfs 文件",hdfsFullPath,localPath)
        
        #校验路径
        if (not (hdfsFullPath.startswith(hdfsFlag))):
            raise  Exception('{} 地址错误 hdfs://ip:port/xxx'.format(hdfsPath))
            
        #拆分地址
        hdfsPath=hdfsFullPath.replace(hdfsFlag,"")
        tempPath = hdfsPath.split("/",1)
        remotePath="/"+tempPath[1]
        
        #获取客户端
        hdfsClient=self.getHdfsClinet(tempPath[0])
        
        print("hdfs 远程路径 {0}".format(remotePath))
        #print(hdfsClient.ls(remotePath))
        
        if hdfsClient.exists(remotePath):
            if hdfsClient.isdir(remotePath):
                for file in hdfsClient.ls(remotePath):
                    self.downFile(hdfsClient,file,localPath)
            else:
                self.downFile(hdfsClient,remotePath,localPath)
                
            self.disconnect(hdfsClient)
        else:
            raise  Exception('{0} 远程目录不存在{1}'.format(hdfsClient,remotePath))
     
     #下载文件
     def downFile(self,hdfsClient,filePath,localPath):
        print("{0}下载hdfs 文件{1} 到本地目录 {2}".format(hdfsClient,filePath,localPath))
        try:
            tempArray = filePath.split("/")
            fileName = tempArray[len(tempArray)-1]
            downPath = ""
            if localPath.endswith("/"):
                downPath = localPath+fileName
            else:    
                downPath = localPath+"/"+fileName
                
            hdfsClient.get(filePath,downPath)
        except SystemError as err:
            print("下载文件失败")       
     def upload(self,loadPath,hdfsFullPath):
        #校验路径
        if (not (hdfsFullPath.startswith(hdfsFlag))):
            raise  Exception('{} 地址错误 hdfs://ip:port/xxx'.format(hdfsPath))
            
        #拆分地址
        hdfsPath=hdfsFullPath.replace(hdfsFlag,"")
        tempPath = hdfsPath.split("/",1)
        remotePath="/"+tempPath[1]
        
        #获取客户端
        hdfsClient=self.getHdfsClinet(tempPath[0])

        hdfsClient.put(loadPath,remotePath)
        
        self.disconnect(hdfsClient)
        
        
     #断开连接
     def disconnect(self,hdfsClient):
        print("{0} 关闭连接".format(hdfsClient))
        hdfsClient.disconnect
            
            
     #获取 hdfs 客户端       
     def getHdfsClinet(self,hdfsInfo):
         print("获取 hdfs 客户端")
         hdfsInfoArry = hdfsInfo.split(":")
         return HDFileSystem(host=hdfsInfoArry[0], port=int(hdfsInfoArry[1]))
     
     #读取本地文件 转 pandas df
     def readLocalParquet2df(self,localPath):
         pf = ParquetFile(localPath)
         return pf.to_pandas()
        
     #读取目录下parquet 转 pandas df
     def readLocalMultParquet2df(self,localPath):
         df=None
         files=os.listdir(localPath)
         index = 1
         while(index<len(files)):
              temp=self.readLocalParquet2df(localPath+"/"+files[index])
              if(index==1):
                df=temp
              else:
                df=pd.concat([df,temp])
              index=index+1
         return df
         
       
     #读取远程文件 转 pandas df
     def readRemoteParquet2df(self,path,hdfsInfo):
         pf = ParquetFile(path, open_with=self.getHdfsClinet(hdfsInfo).open)
         return pf.to_pandas()
        
        
     #pandas df 写入parquet
     def dataframe2ParquetWrite(self,df,localPath):
         write(localPath, df)