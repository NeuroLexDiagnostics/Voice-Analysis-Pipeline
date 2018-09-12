import pandas as pd
import mysql.connector
import sys
import tempfile
import xlrd
import os
import re
import json
import datetime
import requests
from requests import Request, Session
import time
import numpy as np
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR,SVC
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error
# from keras.models import Sequential
# from keras.layers.core import Activation, Dense, Dropout, Flatten, Permute, Reshape
# from keras.layers import Conv2D, MaxPooling1D, Conv1D
# from keras.optimizers import SGD
# from keras.wrappers.scikit_learn import KerasClassifier


class DB_Interface(object):
    def __init__(self):
        self.cnx = self.mysqlConnect()

    def mysqlConnect(self,**kwargs):
        '''
        Conects to mysql db using custom credentials or default ones.
        Return connection object. Needs to be closed after db work is complete
        '''
        if len(kwargs) == 0:
            config = {
            'user': 'msdv_user',
            'password': '8bDztx2qx4',
            'host': 'sc-msdvchar-dev',
            'database':' msdv_char_data',
            'raise_on_warnings': True,
            'connect_timeout':1000000
            }
        else:
            config = kwargs

        cnx = mysql.connector.connect(**config)
        return cnx

    def mysqlClose(self):
        ''' Takes mysql connection object and closes the connection'''
        cnx = self.cnx
        cnx.close()
        return

    def createTable(self,table_name,col_dict):

        ctsql = "CREATE TABLE "+ table_name +" ("
        for k,v in col_dict.items():

            ctsql += k+' '+v+','
        ctsql = ctsql[:-1]
        ctsql += ')'
        # execute sql
        cursor = self.cnx.cursor()
        cursor.execute(ctsql)
        cursor.close()
        return
    def parse_file_name(self,file_name,df):
        '''
        Checks if file already contains certain information

        Then fills in the gap with missing information:

        Ex: Board(s) + PVT + Chip #/ECID

        ---- ECID = P150 --- similar naming is ECID NOT Board
        BOARD CAN BE ESTABLISHED AS SLT
        '''
        ecid = None
        chip_id = None
        pass_bit = 1
        cols = df.columns.tolist()
        file_split = file_name.split('_')
        if 'ECID' not in cols and 'CHIP_ID' not in cols:

            if file_name[0] == 'P' and file_name[1].isdigit() and file_name[2].isdigit() :
                ecid = "_".join(file_split[0:3])
                print(ecid)
            for part in file_split:

                if 'ecid' in part.lower():
                    part = part[4:]
                    ecid = part
                if 'chip' in part.lower():
                    part = part[4:]
                    chip_id = part
            if ecid == None and chip_id == None:
                pass_bit = 0
                print("There is neither an ECID/Chip ID parsable/in the file. Please include this information")
            else:
                if ecid != None:
                    df['ECID'] = ecid
                if chip_id != None:
                    df['CHIP_ID'] = chip_id
                print("Chip_ID and/or ECID are present. Information is good!")
        else:
            print("File has either ECID or Chip, which is okay!")

        board1 = None
        board2 = None

        if 'BOARD1' not in cols:
            if 'slt' in file_name.lower():
                board1 = 'SLT'
            else:
                for part in file_split:
                    if part[0] == 'P':
                        board1 = 'SLT'
                        break
                    print(sys.exit())
                    if part[0] == 'e':
                        if len(part) == 5:
                            cbit = 1
                            for char in part[1:]:
                                if char.isdigit() == False:
                                    cbit = 0
                            if cbit == 0:
                                continue
                            else:
                                if board1 == None:
                                    board1 = part
                                elif board2 == None:
                                    board2 = part
                        else:
                            continue

            if board1 == None:
                pass_bit = 0
                print("There is no board information associated with this file. Please include this information!")
            else:
                df['Board1'] = board1
                df['Board2'] = board2
                print("Board Information is good!")

        proc = None
        volt = None
        temp = None
        if 'PROC' in cols:
            proc = 1
        if 'DVDD' in cols:
            volt = 1
        if 'TEMP' in cols:
            temp = 1
        for part in file_split:
            if 'PROC' not in cols:
                if 'proc' in part:
                    proc = part[4:]
                    df['PROC'] = proc
            if 'DVDD' not in cols and 'pmu' not in file_name:
                if 'p' in part and 'v' in part:
                    p = part.index('p')
                    if part[p-1].isdigit() and part[p+1].isdigit() and part[p+2].isdigit() and part[p+3].isdigit():
                        volt = int(part[p-1] + part[p+1:p+4])
                        df['DVDD'] = volt
            if 'TEMP' not in cols:
                if 'C' in part:
                    temp = part[:-1]
                    df['TEMP'] = temp
        if proc == None:
            df['PROC'] = 'NN'
        if volt == None:
            df['DVDD'] = 1000
        if temp == None:
            df['TEMP'] = 25
        if pass_bit == 0:
            print("Please account for missing information as specified above")
            sys.exit(1)
        else:
            print("Information is all set, ok procede with upload")
            return df

    def check_override(self,table_name,file_name):
        ov_bit = 0
        stmt = "SELECT * FROM " + table_name
        tb_data = pd.read_sql(stmt,self.cnx)
        file_list = tb_data['SRCFILE'].unique()
        for fi in file_list:
            if file_name in fi:
                b = input("Enter 1 for yes, 0 for no: The data you've provided is duplicate. Would you like to override?")
                if b == '1':
                    ov_bit = 1
                    break
                elif b == '0':
                    ov_bit = 2
        return ov_bit

    def excel_to_df(self,excelfile):
        xl_file = pd.ExcelFile(excelfile)
        sheet_names = xl_file.sheet_names
        dfList = []
        t_sheet_names = [x.lower() for x in sheet_names]
        numSheets = len(t_sheet_names)
        if 'setup' in t_sheet_names:
            numSheets -= 1
        if 'summary' in t_sheet_names:
            numSheets -= 1
        for s in sheet_names:
            if s.lower() == 'setup' or s.lower() == 'summary':
                continue
            df = xl_file.parse(s)
            if numSheets > 1:
                proc = input("What is the Process of this Sheet")
                df['PROC'] = proc
                volt = input("What is the Voltage of this Sheet")
                df['DVDD'] = volt
                temp = input("What is the Temperature of this Sheet")
                df['TEMP'] = temp
            dfList.append(df)
        df = pd.concat(dfList)
        return df

    def upload_from_local(self,local_path,local_file,user,team,project,filetype):
        '''
        Uploads a file from local path. In the event there is missing data in the sharepoint accessible location
        - LOCAL PATH MUST HAVE FOLLOWING FOLDER NAMING --
        <CHIP>_<INTERFACE>_DATA
        '''
        if '.csv' not in local_file and '.xlsx' not in local_file and 's2p' not in local_file:
            print("The file you are working to upload is not a csv, xlsx, or s2p")

        list_of_files = os.listdir(local_path)
        if len(list_of_files) == 0:
            print("Local Path is incorrect.")
            sys.exit(1)
        if local_file not in list_of_files:
            print("File not at given sharepoint path.")
            sys.exit(1)
        #Parse Path:
        path = local_path.strip("./")
        path = path.split('_')
        print(path)
        loi = ['UPHY','MEM','MIPI','DISP','PLL']
        chip = ['TU102','TU104','TU106','TU116','TU117']

        if path[0] in chip and path[1] in loi and path[2] == "DATA":
            table_name = path[0] + '_' + path[1] + '_' + filetype + '_DATA'
        else:
            print("Incorrect Folder Path")
            sys.exit(1)

        legend = 'MSDV_DB_LEGEND'
        cnx = self.cnx
        stmt = "SELECT * FROM " + legend
        legend_df = pd.read_sql(stmt,cnx)
        if '.csv' in local_file:
            if local_path[-1] != '/':
                csv_file = local_path + '/' + local_file
            else:
                csv_file = local_path + local_file
            df = pd.read_csv(csv_file)
        elif '.xlsx' in local_file:
            if local_path[-1] != '/':
                excel_file = local_path + '/' + local_file
            else:
                excel_file = local_path + local_file
            df = self.excel_to_df(excel_file)
        elif '.s2p' in local_file:
            if local_path[-1] != '/':
                s2pfile = local_path + '/' + local_file
            else:
                s2pfile = local_path + local_file
            df = self.parseS2P(s2pFile,path[0],user,team,path[1])
        else:
            print("File is not of proper file type. Skipping upload of file")
            return
        date = datetime.datetime.now()
        time = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
        df['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['SRCFILE'] = local_path + '/' + local_file
        df['ENG'] = user
        df['CHIP'] = path[0].upper()
        df['TEAM'] = team
        df['DATE'] = time
        df = self.parse_file_name(local_file,df)
        df = df.dropna(axis=0,how='all')

        if table_name not in legend_df['TABLE_NAME'].values.tolist():
            columns = list(df.columns.values)
            for col in range(len(columns)):
                columns[col] = re.sub(r'\(.*\)', '',columns[col])
            field = ["text"] * len(columns)
            col_dict = dict(zip(columns,field))
            self.createTable(table_name,col_dict)
            cursor = cnx.cursor()
            sql_text="desc " + legend
            cursor.execute(sql_text)
            data_col_names = [column[0] for column in cursor.fetchall()]
            col_names = ','.join(map(str,data_col_names))
            valuestr = ''
            for count in data_col_names:
                valuestr += "%s,"
            valuestr = valuestr[:-1]
            d = [table_name,path[0],path[1],project,filetype]

            udsql = r"INSERT INTO "+ legend +" ("+ col_names +") VALUES (" + valuestr +")"
            cursor.execute(udsql,d)
            cursor.close()
        ov_bit = self.check_override(table_name,local_file)
        cursor = cnx.cursor()
        stmt = "desc " + table_name
        cursor.execute(stmt)
        col_names = [column[0] for column in cursor.fetchall()]
        miss_list = self.compare_cols(df.columns,col_names)
        if ov_bit == 0 or ov_bit == 1:
            #Data is not duplicate
            if ov_bit == 1:
                ### Delete Data
                self.overrideDataByFile(table_name,local_path,local_file)
                return
                #PUSH DATA TO SQL
            self.pushToSQL(df,table_name)
        else:
            #Data is not going to be overridden, exit.
            print("Data is duplicated, but will not be overridden.")
            return
    def upload(self,sp_path,sp_file,user,team,project,filetype):
        if '.csv' not in sp_file and '.xlsx' not in sp_file and 's2p' not in sp_file:
            print("The file you are working to upload is not a csv, xlsx, or s2p")
        self.sp = SP_Interface(sp_path,0)
        list_of_files = self.sp.fileList

        if self.sp.checkPath(sp_path) == 1:
            #Check File

            if sp_file not in list_of_files:
                print("File not at given sharepoint path.")
                sys.exit(1)
        else:
            print("Sharepoint Path to File is Incorrect.")
            sys.exit(1)
        tpath = sp_path.split('/') #THis is assuming that the data follows the current file structure
        table_name = tpath[3].upper() + '_' + tpath[4].upper() + '_' + filetype + '_DATA'
        # FIND PROPER TABLE - How to fget file type
        legend = 'MSDV_DB_LEGEND'
        cnx = self.cnx
        stmt = "SELECT * FROM " + legend
        legend_df = pd.read_sql(stmt,cnx)
        lpath = tempfile.gettempdir()
        lpath = tempfile.mkdtemp()
        self.sp.downloadFile(sp_path,sp_file,lpath)
        if '.csv' in sp_file:
            csvFile = os.listdir(lpath)[0]
            csvFile = lpath + '/' + csvFile
            df = pd.read_csv(csvFile)
        if '.xlsx' in sp_file:
            excelfile = lpath + '/' + os.listdir(lpath)[0]
            df = self.excel_to_df(excelfile)
        if '.s2p' in sp_file:
            s2pFile = lpath + '/' + os.listdir(lpath)[0]
            df = self.parseS2P(s2pFile,chip,user,team,interface)

        date = datetime.datetime.now()

        time = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
        df['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['SRCFILE'] = sp_path + '/' + sp_file
        df['ENG'] = user
        df['CHIP'] = tpath[3].upper()
        df['TEAM'] = team
        df['DATE'] = time

        df = self.parse_file_name(sp_file,df)
        df = df.dropna(axis=0,how='all')

        if table_name not in legend_df['TABLE_NAME'].values.tolist():
            columns = list(df.columns.values)
            for col in range(len(columns)):
                columns[col] = re.sub(r'\(.*\)', '',columns[col])
            field = ["text"] * len(columns)
            col_dict = dict(zip(columns,field))
            self.createTable(table_name,col_dict)
            cursor = cnx.cursor()
            sql_text="desc " + legend
            cursor.execute(sql_text)
            data_col_names = [column[0] for column in cursor.fetchall()]
            col_names = ','.join(map(str,data_col_names))
            valuestr = ''
            for count in data_col_names:
                valuestr += "%s,"
            valuestr = valuestr[:-1]
            d = [table_name,tpath[3],tpath[4],project,filetype]

            udsql = r"INSERT INTO "+ legend +" ("+ col_names +") VALUES (" + valuestr +")"
            cursor.execute(udsql,d)
            cursor.close()
        ov_bit = self.check_override(table_name,sp_file)
        cursor = cnx.cursor()
        stmt = "desc " + table_name
        cursor.execute(stmt)
        col_names = [column[0] for column in cursor.fetchall()]
        miss_list = self.compare_cols(df.columns,col_names)
        if ov_bit == 0 or ov_bit == 1:
            #Data is not duplicate
            if ov_bit == 1:
                ### Delete Data
                self.overrideDataByFile(table_name,sp_path,sp_file)
                return
                #PUSH DATA TO SQL
            self.pushToSQL(df,table_name)
        else:
            #Data is not going to be overridden, exit.
            print("Data is duplicated, but will not be overridden.")
            return


    def compare_cols(self,df_cols,col_list):
        l = []
        for col in df_cols:
            if col not in col_list:
                l.append(col)
        return l
    def pushToSQL(self,df,table_name):
        df = df.where((pd.notnull(df)), None)
        cursor = self.cnx.cursor()
        sql_text="desc " + table_name
        cursor.execute(sql_text)
        data_col_names = [column[0] for column in cursor.fetchall()]
        print('Uploading data to SQL database')

        data = []
        for index, row in df.iterrows():
            data.append([])
            for name in data_col_names:
                if name not in df:
                    data[index].append(None)
                else:
                    data[index].append(row[name])
        data = [x for x in data if (x != [] and len(x) == len(data_col_names))]

        #DELETE ANY ROWS WITH NOT ENUGH DATA

        col_names = ','.join(map(str,data_col_names))
        valuestr = ''

        if data == []:
            return
        for count in data[0]:
            valuestr += "%s,"
        valuestr = valuestr[:-1]

        udsql = r"INSERT INTO "+table_name+" ("+col_names+") VALUES ("+valuestr+")"
        cursor.executemany(udsql,data[0:])
        time.sleep(5)
        self.cnx.commit()
        cursor.close()
        print("Data Successfully Pushed Into Database!\n")

    def addColumnToTable(self,table_name,col_name,col_val=None):
        '''
        Check if column is already in table.
        Prompt user if they want to add column: must retype the column
        '''
        print("Adding Column " + col_name +" to Table " + table_name + "with value" + str(col_val))
        cnx = self.cnx
        cursor = cnx.cursor()
        stmt ="desc " + table_name
        cursor.execute(stmt)
        table_col_dict = [column[0] for column in cursor.fetchall()]
        if col_name not in table_col_dict:
            inp = input('To verify that you want to add the column, please retype the column name: ')
            if inp != col_name:
                print("Input doesn't match the column name. Please try again.")
                sys.exit(1)
            else:
                if col_val == None:
                    txt = 'NULL'
                else:
                    txt = "'" + col_val + "'"
                stmt = "ALTER TABLE " + table_name+ " ADD COLUMN " + col_name +" text NOT NULL"
                cursor.execute(stmt)
                cnx.commit()
        else:
            print("Column already exists in specific table.")
            sys.exit(1)
        print("Column Successfully Added")

    def deleteColumnFromTable(self,table_name,col_name):
        print("Deleting Column " + col_name +"from Table " + table_name)
        cnx = self.cnx
        cursor = cnx.cursor()
        stmt ="desc " + table_name
        cursor.execute(stmt)
        table_col_dict = [column[0] for column in cursor.fetchall()]
        if col_name not in table_col_dict:
            print("Column does not exist in table " + table_name +".Please check the column name you entered.")
            sys.exit(1)
        else:
            inp = input('To verify that you want to delete the column, please retype the column name: ')
            if inp != col_name:
                print("Input doesn't match the column name.")
                sys.exit(1)
            else:
                inp = input("Are you sure you want to delete the column?Type yes if true.: ")
                if inp == 'yes':
                    stmt = "ALTER TABLE " + table_name +  " DROP COLUMN " + col_name
                    cursor.execute(stmt)
                    cnx.commit()
                else:
                    print("Column will not be deleted.")
                    sys.exit(1)
        print("Column Successfully Deleted")

    def deleteDatabyFile(self,table_name,file_name):
        print("Deleting File " + file_name + " from Table " + table_name)
        cnx = self.cnx
        stmt =" SELECT SRCFILE FROM " + table_name
        src_df = pd.read_sql(stmt,cnx)
        file_list = src_df['SRCFILE'].unique()
        if col_name not in file_list:
            print("Column does not exist in table " + table_name +".Please check the column name you entered.")
            sys.exit(1)
        else:
            inp = input('To verify that you want to delete the column, please retype the column name: ')
            if inp != col_name:
                print("Input doesn't match the column name.")
                sys.exit(1)
            else:
                inp = input("Are you sure you want to delete the column?Type yes if true.: ")
                if inp == 'yes':
                    stmt = "ALTER TABLE " + table_name +  " DROP COLUMN " + col_name
                    cursor.execute(stmt)
                    cnx.commit()
                else:
                    print("Column will not be deleted.")
                    sys.exit(1)
        print("Column Successfully Deleted")

    def changeDataValue(self,table_name,file_name,sp_path,col_name,value):
        '''
        Changes column value by file
        - Validate Table
        - Validate Column
        - Validate File Name
        '''
        print("Changing Data for File " + file_name + " in table " + table_name + " Column " + col_name + " to Value " + value)
        cnx = self.cnx
        cursor = cnx.cursor()
        stmt = "desc " + table_name
        cursor.execute(stmt)
        table_col_dict = [column[0] for column in cursor.fetchall()]
        if col_name not in table_col_dict:
            print("Column does not exist in table " + table_name +".Please check the column name you entered.")
            sys.exit(1)
        else:
            # inp = input('To verify that you want to change the value in the column, please retype the column name: ')
            # if inp != col_name:
            #     print("Input doesn't match the column name.")
            #     sys.exit(1)
            # else:
            #     inp = input("Are you sure you want to modify the column?Type yes if true.: ")
            #     if inp == 'yes':
            stmt = "UPDATE msdv_char_data." + table_name + " SET " + col_name + "='" + value +"' WHERE SRCFILE='" + sp_path +'/' + file_name + "'"
            print(stmt)
            cursor.execute(stmt)
            cnx.commit()
                # else:
                #     print("Column will not be modified.")
                #     sys.exit(1)
        ###stmt = "UPDATE TABLE " + table_of_file + " SET " + mod_col + "='" + val +"' WHERE SRCFILE='" + mod_file + "'"
    def overrideDataByFile(self,table_name,file_path,file_name):
        cnx = self.cnx
        cursor = cnx.cursor()
        stmt = "SELECT * FROM " + table_name
        df = pd.read_sql(stmt,cnx)
        files = df.SRCFILE.values.tolist()
        obit = 0
        for fi in files:
            if file_name in fi:
                obit = 1
            else:
                continue
        if obit == 1:
            stmt = "DELETE FROM " + table_name + " WHERE SRCFILE like '%" + file_path + '/' + file_name + "%'"
            print(stmt)
            cursor.execute(stmt)
            cnx.commit()
            self.pushToSQL(df,table_name)
        else:
            print(file_name + "not in specified table, please write a proper file name")

    def getLegendData(self):
        table = 'MSDV_DB_LEGEND'
        stmt = "SELECT * from " + table
        legend_df = pd.read_sql(stmt,self.cnx)
        return legend_df

    def getDataByECID(self,ecid_val):
        '''
        Get all Data Corresponding to ECID per table, create mapping per table to ecid.
            - this is to reduce the amount of latency such a command would garner
        '''
    def getDataByLog(self,log_name):
        '''
        Get all Data Corresponding to log per table, create mapping per table to log.
            - this is to reduce the amount of latency such a command would garner
        '''
    def getTableData(self,table_name):
        tb_list = self.list_tables()
        if table_name not in tb_list:
            print("Table Name Provided is not in Database.")
            sys.exit(1)
        else:
            stmt = "SELECT * FROM " + table_name
            df = pd.read_sql(stmt,self.cnx)
            return df

    def getInterfaceData(self,interface_name):
        dip_list = self.list_design_ip()
        if interface_name not in dip_list:
            print("Interface Provided is not in Database.")
            sys.exit(1)
        else:
            leg_df = self.getLegendData()
            tables = leg_df[leg_df['DESIGN_IP']== interface_name]['TABLE_NAME'].values.tolist()
            dfList = []
            for table in tables:
                stmt = "SELECT * FROM " + table
                df = pd.read_sql(stmt,self.cnx)
                dfList.append(df)
            return pd.concat(dfList)

    def getFileTypeData(self,file_type):
        ft_list = self.list_filetype()
        if file_type not in ft_list:
            print("File Type Provided is not in Database.")
            sys.exit(1)
        else:
            ft_df = self.getLegendData()
            tables = ft_df[ft_df['FILE_TYPE']==file_type]['TABLE_NAME'].values.tolist()
            dfList = []
            for table in tables:
                stmt = "SELECT * FROM " + table
                df = pd.read_sql(stmt,self.cnx)
                dfList.append(df)
            return pd.concat(dfList)

    def getChipData(self,chip_name):
        chip_list = self.list_chip()
        if chip_name not in chip_list:
            print("Chip Name Provided is not in Database.")
            sys.exit(1)
        else:
            leg_df = self.getLegendData()
            tables = leg_df[leg_df['CHIP'] == chip_name]['TABLE_NAME'].values.tolist()
            dfList = []
            for table in tables:
                stmt = "SELECT * FROM " + table
                df = pd.read_sql(stmt,self.cnx)
                dfList.append(df)
            return pd.concat(dfList)

    def getProjectData(self,project_name):
        proj_list = self.list_project()
        if project_name not in proj_list:
            print("Project Name Provided is not in Database.")
            sys.exit(1)
        else:
            leg_df = self.getLegendData()
            tables = leg_df[leg_df['PROJECT'] == project_name]['TABLE_NAME'].values.tolist()
            dfList = []
            for table in tables:
                stmt = "SELECT * FROM " + table
                df = pd.read_sql(stmt,self.cnx)
                dfList.append(df)
            return pd.concat(dfList)

    def list_design_ip(self):
        return self.getLegendData()['DESIGN_IP'].unique()
    def list_tables(self):
        return self.getLegendData()['TABLE_NAME'].unique()
    def list_filetype(self):
        return self.getLegendData()['FILE_TYPE'].unique()
    def list_chip(self):
        return self.getLegendData()['CHIP'].unique()
    def list_project(self):
        return self.getLegendData()['PROJECT'].unique()

class SP_Interface():
    def __init__(self,sp_path,fbit):
        '''
        Initiate with Access Token. Get SP PATH, checks SP PATH,
        Loads in files. If path doesnt have any files, system exit.
        '''
        self.fbit = fbit
        self.sp_path = sp_path
        self.access_token = self.getAccessToken()
        self.fileList = self.grabSrc(self.sp_path,self.fbit)
        if self.fileList == []:
            print("Sharepoint Path is Empty. Exiting with status 1")
            sys.exit(1)

    def getAccessToken(self):
        '''
        Client Id:  	       4e41e5aa-2340-4709-951e-7176f27fcd73
        Client Secret:  	   tLB8LstnOU99E32pLFOObSqsbhbQfDe1ui5MVxhWqq0=
        Title:  	           msdv-pySP-1
        App Domain:  	          www.nvidia.com
        Redirect URI:  	          https://nvidia.sharepoint.com/sites/msdv_workspace/default.aspx
        '''

        clientid = "4e41e5aa-2340-4709-951e-7176f27fcd73"
        secret = "tLB8LstnOU99E32pLFOObSqsbhbQfDe1ui5MVxhWqq0="
        redirecturi = "hrrps://localhost"

        url = "https://nvidia.sharepoint.com/sites/msdv_workspace/"
        domain = "nvidia.sharepoint.com"

        identifier = "00000003-0000-0ff1-ce00-000000000000"

        realm = "43083d15-7273-40c1-b7db-39efd9ccc17a"
        bodyy = r"grant_type=client_credentials&client_id=4e41e5aa-2340-4709-951e-7176f27fcd73%4043083d15-7273-40c1-b7db-39efd9ccc17a&client_secret=tLB8LstnOU99E32pLFOObSqsbhbQfDe1ui5MVxhWqq0%3d&redirect_uri=hrrps%3a%2f%2flocalhost&resource=00000003-0000-0ff1-ce00-000000000000%2fnvidia.sharepoint.com%4043083d15-7273-40c1-b7db-39efd9ccc17a"

        s = Session()

        req = Request('POST', "https://accounts.accesscontrol.windows.net/"+realm+"/tokens/OAuth/2", data=bodyy,headers={'Content-type':"application/x-www-form-urlencoded"})
        prepped = s.prepare_request(req)
        resp = s.send(prepped)

        xx = json.dumps(str(resp.content)[2:-1])
        yy = json.loads(xx)
        zz = json.loads(yy)
        zzat = zz['access_token']
        return zzat

    def downloadFile(self,spPath,spFile,localpath):
        '''
        Download SP file to local directory

        - get file contents as bytes
        - write bytes to file
        '''

        url = "https://nvidia.sharepoint.com/sites/msdv_workspace/"

        requrl = url + "_api/web/getfolderbyserverrelativeurl('"+spPath+"')/files/getbyurl('"+spFile+"')/$value"
        # requrl = url + "_api/web/getfolderbyserverrelativeurl('"+spPath+"/"+spFile+"')/$value"
        method = 'GET'
        headers = {
            'Authorization' : "Bearer " + self.access_token,
            'Accept' : "application/json"
            # 'binaryStringResponseBody' : 'True'
        }
        try:
            s = Session()
            req = Request(method, requrl, headers=headers)
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            if resp.status_code != 200:
                raise ValueError('File Not Downloaded!! Likely a typo in path or filename.', resp.status_code)
        except ValueError as err:
            print("Error, Status_code")
            print(err.args)
            return resp.status_code

        # byteData = bytearray(resp.content)
        byteData = resp.content

        with open(localpath+"\\"+spFile, 'wb') as writeFile:
            writeFile.write(byteData)

        return resp.status_code

    def grabSrc(self,spPath,fbit):
        '''

        '''
        url = "https://nvidia.sharepoint.com/sites/msdv_workspace/"
        if fbit == 0:
            requrl = url + "_api/web/GetFolderByServerRelativeUrl('"+ spPath+"')/Files"
        if fbit == 1:
            requrl = url + "_api/web/GetFolderByServerRelativeUrl('"+ spPath+"')/Folders"
        method = 'Get'
        headers = {
            'Authorization' : "Bearer " + self.access_token,
            'Accept' : "application/json"
            # 'binaryStringResponseBody' : 'True'
        }
        s = Session()
        req = Request(method,requrl,headers=headers)
        prepped = s.prepare_request(req)
        resp = s.send(prepped)
        data = resp.content
        data1 = json.loads(data)
        files = []
        for i in range(len(data1['value'])):
            files.append(data1['value'][i]['Name'])
        return files

    def checkPath(self,spPath):
        files = self.grabSrc(spPath,0)
        if files == []:
            return 0
        else:
            return 1

class Analytics_Interface(object):
    '''
    Enable the following:
    - Grab All Data for Model(s)
    -
    '''
    def __init__(self,data,enc_list,targets,ml_bit):
        self.ml_bit = ml_bit # 0 = classification, 1 = prediction
        self.enc_list = enc_list
        self.cnx = self.mysqlConnect()
        if targets == None:
            self.targets = 'flag'
        else:
            self.targets = targets
        self.X_train,self.y_train,self.X_test,self.y_test,self.X_val,self.y_val = self.train_test_validation(data)

    def split_data(self,df):
        y = df[self.targets].values.tolist()
        X = df.drop(self.targets,axis=1)
        return X,y

    def SKFOLD_train_test_validation(self,df):
        print("YO")
    def train_test_validation(self,df):
        print(r"Data Split into 60% Training : 20 % Test : 20 % Validation")
        train , validate , test = np.split(df.sample(frac=1),[int(.6*len(df)), int(.8*len(df))])
        X_train, y_train = self.split_data(train)
        X_train, y_train = self.preprocess_data(X_train,y_train)
        X_test, y_test = self.split_data(test)
        X_test, y_test = self.preprocess_data(X_test,y_test)
        X_val, y_val = self.split_data(validate)
        X_val, y_val = self.preprocess_data(X_val,y_val)
        return X_train,y_train,X_test,y_test,X_val,y_val

    def mysqlConnect(self,**kwargs):
        '''
        Conects to mysql db using custom credentials or default ones.
        Return connection object. Needs to be closed after db work is complete
        '''
        if len(kwargs) == 0:
            config = {
            'user': 'msdv_user',
            'password': '8bDztx2qx4',
            'host': 'sc-msdvchar-dev',
            'database':' msdv_char_data',
            'raise_on_warnings': True,
            'connect_timeout':1000000
            }
        else:
            config = kwargs

        cnx = mysql.connector.connect(**config)
        return cnx

    def mysqlClose(self):
        ''' Takes mysql connection object and closes the connection'''
        cnx = self.cnx
        cnx.close()
        return

    def encode_data(self,data,labels):
        '''
        Encode(s) Qualitative data fairly well defined by enc_list
        Encoding also includes encoding labelling; if not in enc_list, just use labelEncoder
        '''
        if self.ml_bit == 0:
            enc_list = self.enc_list
            le = LabelEncoder()
            labels = le.fit_transform(labels.values.tolist())
            self.classes = le.classes_
            (self.classes)
        if self.enc_list != None:
            data = data.drop(self.enc_list,axis=1)
            #data = pd.get_dummies(data,columns=enc_list)
        return data, labels

    def isFloat(self,str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def numerical_check(self,data):
        '''
        Validate(s) the dataframe for numerical content. Remove(s) column(s) not deemed of qualitative value
        '''
        for column in data:
            if self.isFloat(column[0]) == False and column[0].isdigit() == False:
                data = data.drop(column,axis=1)
        return data

    def preprocess_data(self,data,labels):
        '''
        Preprocesses and encodes data primed for usage by Machine Learning Algorithms
        Notes:
        * All Fields passed into different method(s) must be of numerical value(s)
        * All Labels can and should be labelled to classes
        '''
        #data = self.numerical_check(data)
        data,labels = self.encode_data(data,labels)
        data = data.fillna(0)
        return data,labels

    def pca_feat_select(self):
        '''
        Implements a PCA based feature selection algorithm
        '''
        X = self.data
        Y = self.labels
        tot_comp = len(X.columns)
        pca = PCA(n_components = tot_comp)
        pca.fit(X)
        var = np.cumsum(np.round(pca.explained_variance_ratio_,decimals=4)*100)
        num_comps=None
        for i in range(len(var)):
            print(var[i])
            if var[i] >= 95:
                num_comps = i
                break
        if num_comps == None:
            num_comps = tot_comp
        pca = PCA(n_components = num_comps)
        X_train = pca.fit_transform(X)
        return X_train

    def rf_feat_select(self):
        X = self.data
        Y = self.labels

        '''
        Implements a Random Forest Based feature selection algorithm
        '''
    def feature_selection(self,params=None):


        '''
        Performs feature selection. If parameters are specified, it checks that the
        parameters exists for given feature set(s), and returns if there's any extraneous parameters, or specified parameters
        which do not exist.

        Otherwise, it will utilize a set of feature selection algorithm(s); primarly PCA,RF weightage algorithms, to narrow down features.
        - This method can also be used to validate previous assumptions in data.
        '''
        if params != None:
            print("Use Parameters to fit upon current feature set")
        else:
            self.X_train = pca_feat_select()
            self.Y_train = self.labels
            return self.X_train, self.Y_Train

    def run_model(self,model_bit):
        if model_bit == 0:
            clf = self.grid_svm()
        if model_bit == 1:
            clf = self.grid_rf()
        if model_bit == 2:
            clf = self.grid_ann()
        clf.fit(self.X_train,self.y_train)
        y_test_pred = clf.predict(self.X_test)
        y_val_pred = clf.predict(self.X_val)
        if self.ml_bit == 0:
            test_accuracy = np.mean(y_test_pred == self.y_test)
            val_accuracy = np.mean(y_val_pred == self.y_val)
            print("Test Accuracy: " , test_accuracy)
            print("Validation Accuracy" , val_accuracy)
        else:
            test_rmse = mean_squared_error(self.y_test,y_test_pred,multioutput='uniform_average')
            val_rmse = mean_squared_error(self.y_val,y_val_pred,multioutput='uniform_average')
            print("Test Mean Error: " , test_rmse)
            print("Validation Mean Error:" , val_rmse)
    def grid_svm(self):
        # tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
        #      'C': [1, 10, 100, 1000]},
        #     {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
        # tuned_parameters=[{'kernel':['rbf'],'gamma':[1e-3,1e-4],'C':[1,10,100]},
        # {'kernel': ['linear'], 'C': [1, 10, 100]}]
        tuned_parameters=[{'kernel':['rbf'],'gamma':[1e-3,1e-4],'C':[1,10,100,1000]}]
        print("Performs SVM")
        if self.ml_bit == 0:
            clf = GridSearchCV(SVC(),tuned_parameters)
        else:
            clf = GridSearchCV(SVR(),tuned_parameters)
        print("SVM fit on data")
        return clf
    def grid_rf(self,data,label):
        tuned_parameters = [{'n_estimators':[10,100,250,500,1000,2000],'max_features':['auto','sqrt'],'max_depth':[2,5,10,20],'min_samples_split':[2,5,10],'min_samples_leaf':[1,2,4]}]
        print("Performs Random Forest")
        if self.ml_bit == 0:
            clf = GridSearchCV(RandomForestClassifier(),tuned_parameters)
        else:
            clf = GridSearchCV(RandomForestRegressor(),tuned_parameters)
        print("Random Forest fit on data")
        return clf

    # def nn_model(self):
    #     model = Sequential()
    #     model.add(Conv1D(4, 2 ,activation='relu',input_shape=(54,1)))
    #     model.add(Conv1D(4, 2 , activation='relu'))
    #     model.add(MaxPooling1D(pool_size=2))
    #     model.add(Dropout(0.25))
    #     model.add(Conv1D(8,2, activation='relu'))
    #     model.add(Conv1D(8,2, activation='relu'))
    #     model.add(MaxPooling1D(pool_size=2))
    #     model.add(Dropout(0.25))
    #     model.add(Flatten())
    #     model.add(Dense(64, activation='relu'))
    #     model.add(Dropout(0.5))
    #
    #     if self.ml_bit == 0:
    #         model.add(Dense(3, activation='softmax'))
    #         sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    #         model.compile(loss='categorical_crossentropy',scoring=['accuracy'], optimizer=sgd)
    #
    #     else:
    #         model.add(Dense(output_dim,activation='linear'))
    #         model.compile(loss='mse',metrics=['accuracy'], optimizer='adam')
    #     return model
    # def grid_ann(self,data,label):
    #     print("Performs NN")
    #     tuned_parameters =  {"epochs":[10,100],
    #                                  "batch_size":[32,64,128,256]}
    #     model = KerasClassifier(build_fn=self.nn_model(),verbose=0)
    #     clf = GridSearchCV(estimator=model,param_grid=tuned_parameters,n_jobs=-1,return_train_score=True)
    #     print("NN fit on data")
    #     return clf
