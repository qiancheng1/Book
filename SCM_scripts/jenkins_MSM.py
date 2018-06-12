#!/usr/bin/python
import os
import getopt
import sys
import subprocess
import shutil
import socket
import time
import re
import fileinput
import zipfile
import random
import time

today=time.strftime('%Y%m%d')
hostname=socket.gethostname()
pwd=os.getcwd()
mirror_path={"SOFT35-11":'/home1/SW3/mirror',"SOFT35-12":'/home/jenkins/mirror',"SOFT35-15":'/home1/SW3/mirror',"SOFT35-16":'/home1/SW3/mirror',"SOFT35-17":'/home1/SW3/mirror'}
args_list=sys.argv
args_obj=""
CODE_DIR="CODE"
incre_no=""

def in_check(VAR,VAR_LIST):
    if VAR not in VAR_LIST:
        print '{0} not in {1}'.format(VAR,str(VAR_LIST))
        sys.exit()

class Args(object):
    bool_stat = ['true','false']
    def __init__(self,PROJECT_NAME,CODE_URL,CODE_BRANCH,CODE_XML,CLEAN_CODE,BUILD_PROJECT,IN_VERSION,OUT_VERSION,INCREMENTAL_VERSION,VARIANT,HARD_VER,SIGN,SAVE_TYPE,OTAPACKAGE,MODULE,DOWNLOAD_TYPE):
        self.PROJECT_NAME = PROJECT_NAME
        self.CODE_URL = CODE_URL
        self.CODE_BRANCH = CODE_BRANCH
        self.CODE_XML = CODE_XML
        self.CLEAN_CODE = CLEAN_CODE
        if CLEAN_CODE not in Args.bool_stat:
            print CLEAN_CODE,'value error'
            sys.exit()
        self.BUILD_PROJECT = BUILD_PROJECT
        self.IN_VERSION = IN_VERSION
        self.OUT_VERSION = OUT_VERSION
        self.INCREMENTAL_VERSION = INCREMENTAL_VERSION
        self.VARIANT = VARIANT
        self.HARD_VER = HARD_VER
        self.SIGN = SIGN
        self.SAVE_TYPE=SAVE_TYPE
        self.OTAPACKAGE = OTAPACKAGE
        self.MODULE = MODULE
        self.DOWNLOAD_TYPE = DOWNLOAD_TYPE
    def args_check(self):
        PROJECT_NAME_LIST=['E300L']
        BUILD_PROJECT_LIST=['E300L_WW','E300L_CN','E300L_IN']
        VARIANT_LIST=['user','eng','debug']
        SIGN_LIST=['','unsign']
        SAVE_TYPE_LIST=['dailybuild','factory','preofficial','temp']
        BOOL_LIST=['true','false']
        MODULE_LIST=['all','overall']
        DOWNLOAD_TYPE_LIST=['qf','xtt']
        in_check(self.PROJECT_NAME,PROJECT_NAME_LIST)
        in_check(self.BUILD_PROJECT,BUILD_PROJECT_LIST)
        in_check(self.VARIANT,VARIANT_LIST)
        in_check(self.SIGN,SIGN_LIST)
        in_check(self.SAVE_TYPE,SAVE_TYPE_LIST)
        in_check(self.OTAPACKAGE,BOOL_LIST)
        in_check(self.MODULE,MODULE_LIST)
        in_check(self.DOWNLOAD_TYPE,DOWNLOAD_TYPE_LIST)
        

def args_parse():
    print 'START TO PARSE ARGS'
    opt,args = getopt.getopt(args_list[1:],"h",["project-name=","code-url=","code-branch=","code-xml=","clean-code=","build-project=","ver=",'variant=','hard-ver=','sign=','save-type=','otapackage=','module=','download_type='])
    for key,value in opt:
        if key == "-h" or key == "--help":
            print "no help message hahahahhaha"
            sys.exit()
        elif key == "--project-name":
            PROJECT_NAME=value
        elif key == "--code-url":
            CODE_URL=value
        elif key == "--code-branch":
            CODE_BRANCH=value
        elif key == "--code-xml":
            CODE_XML=value
        elif key == "--clean-code":
            CLEAN_CODE=value
        elif key == "--build-project":
            BUILD_PROJECT=value
        elif key == "--ver":
            VERSION=value
            if VERSION:
                IN_VERSION=VERSION.split()[0]
                OUT_VERSION=VERSION.split()[1]
                INCREMENTAL_VERSION=VERSION.split()[2]
            else:
                IN_VERSION=""
                OUT_VERSION=""
                INCREMENTAL_VERSION=""

        elif key == "--variant":
            VARIANT=value
        elif key == "--hard-ver":
            HARD_VER=value
        elif key == "--sign":
            SIGN=value
        elif key == '--save-type':
            SAVE_TYPE=value
        elif key == '--otapackage':
            OTAPACKAGE=value
        elif key == '--module':
            MODULE=value
        elif key == '--download_type':
            DOWNLOAD_TYPE=value

    global args_obj
    args_obj=Args(PROJECT_NAME,CODE_URL,CODE_BRANCH,CODE_XML,CLEAN_CODE,BUILD_PROJECT,IN_VERSION,OUT_VERSION,INCREMENTAL_VERSION,VARIANT,HARD_VER,SIGN,SAVE_TYPE,OTAPACKAGE,MODULE,DOWNLOAD_TYPE)
    args_obj.args_check()
         
def down_load_code(url,branch,xml):
    print "START TO DOWNLOAD CODE"
    os.chdir(pwd)
    if os.path.exists(CODE_DIR) and args_obj.CLEAN_CODE == "true":
        shutil.rmtree(CODE_DIR)
    try:
        os.mkdir(CODE_DIR)
    except OSError,e:
        print e
    os.chdir(CODE_DIR)
    if hostname in mirror_path:
#little bug here
        if os.path.exists(mirror_path[hostname]+'/300_mirror_repo'):
            os.chdir(mirror_path[hostname]+'/300_mirror_repo')
            result=subprocess.Popen('repoc sync -j3',shell=True)
            result.wait()
            time.sleep(5)
            os.chdir(os.path.join(pwd,CODE_DIR))
           # result1=subprocess.Popen('repoc init -u {0} -b {1} -m {2} --no-repo-verify --reference={3}/300_mirror_repo'.format(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML,mirror_path[hostname]),shell=True)
            subprocess.call('repoc init -u {0} -b {1} -m {2} --no-repo-verify --reference={3}/300_mirror_repo'.format(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML,mirror_path[hostname]),shell=True)
            #result1.wait()
        else:
            #result1=subprocess.Popen('repoc init -u {0} -b {1} -m {2} --no-repo-verify'.format(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML),shell=True)
            subprocess.call('repoc init -u {0} -b {1} -m {2} --no-repo-verify'.format(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML),shell=True)
            #result1.wait()
    else:
        #result1=subprocess.Popen('repoc init -u {0} -b {1} -m {2} --no-repo-verify'.format(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML),shell=True)
        subprocess.call('repoc init -u {0} -b {1} -m {2} --no-repo-verify'.format(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML),shell=True)
        #result1.wait()

    time.sleep(1)
    #result2=subprocess.Popen('repoc sync -cj4',shell=True)
    subprocess.call('repoc sync -cj4',shell=True)
    #result2.wait()

def modifed_auto_args():
    print('START TO MODIFIED AUTO ARGS')
    os.chdir(os.path.join(pwd,CODE_DIR))
    shutil.copy('vendor/wind/scripts/Auto_MSM89XX_E300L_V1.0.sh','auto.sh')
    for ih in fileinput.input('auto.sh',inplace=True):
        if len(re.findall(r'^BUILD_PROJECT=.+',ih)):
            new_line=re.sub(r'^BUILD_PROJECT=.+','BUILD_PROJECT={0}'.format(args_obj.BUILD_PROJECT),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^PRODUCT_NAME=.+',ih)):
            new_line=re.sub(r'^PRODUCT_NAME=.+','PRODUCT_NAME={0}'.format(args_obj.BUILD_PROJECT),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^BUILD_PROJECT_NAME=.+',ih)):
            new_line=re.sub(r'^BUILD_PROJECT_NAME=.+','BUILD_PROJECT_NAME={0}'.format(args_obj.BUILD_PROJECT),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^IN_VERSION=.*',ih)):
            new_line=re.sub(r'^IN_VERSION=.*','IN_VERSION={0}'.format(args_obj.IN_VERSION),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^OUT_VERSION=.*',ih)):
            new_line=re.sub(r'^OUT_VERSION=.*','OUT_VERSION={0}'.format(args_obj.OUT_VERSION),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^INCREMENTAL_VERSION=.*',ih)):
            new_line=re.sub(r'^INCREMENTAL_VERSION=.*','INCREMENTAL_VERSION={0}'.format(args_obj.INCREMENTAL_VERSION),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^VARIANT=.*',ih)):
            new_line=re.sub(r'^VARIANT=.*','VARIANT={0}'.format(args_obj.VARIANT),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^MODULE=.*',ih)):
            new_line=re.sub(r'^MODULE=.*','MODULE={0}'.format(args_obj.MODULE),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^RELEASE_PROJECT=.*',ih)):
            new_line=re.sub(r'^RELEASE_PROJECT=.*','RELEASE_PROJECT={0}'.format(args_obj.BUILD_PROJECT),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^RELEASE_TYPE=.*',ih)):
            new_line=re.sub(r'^RELEASE_TYPE=.*','RELEASE_TYPE={0}'.format(args_obj.MODULE),ih)
            sys.stdout.write(new_line)
        elif len(re.findall(r'^DOWNLOAD_TYPE=.*',ih)):
            new_line=re.sub(r'^DOWNLOAD_TYPE=.*','DOWNLOAD_TYPE={0}'.format(args_obj.DOWNLOAD_TYPE),ih)
            sys.stdout.write(new_line)
        else:
            sys.stdout.write(ih)
    
def modified_hard_version():
    print "START TO MODIFIED HARD VERSION"
    os.chdir(os.path.join(pwd,CODE_DIR))
    if args_obj.BUILD_PROJECT == 'E300L_IN':
        os.chdir('device/wind/E300L_WW')
    else:
        os.chdir('device/wind/{0}'.format(args_obj.BUILD_PROJECT))
    if args_obj.HARD_VER:
        if args_obj.BUILD_PROJECT == 'E300L_IN':
            for ih in fileinput.input('E300L_WW.mk',inplace=True):
                if len(re.findall(r'WIND_PRODUCT_HARDWARE :=',ih)) != 0:
                    new_line=re.sub(r"WIND_PRODUCT_HARDWARE :=.*",'WIND_PRODUCT_HARDWARE := {0}'.format(args_obj.HARD_VER),ih)
                    sys.stdout.write(new_line)
                else:
                    sys.stdout.write(ih)
        else:
            for ih in fileinput.input('{0}.mk'.format(args_obj.BUILD_PROJECT),inplace=True):
                if len(re.findall(r'WIND_PRODUCT_HARDWARE :=',ih)) != 0:
                    new_line=re.sub(r"WIND_PRODUCT_HARDWARE :=.*",'WIND_PRODUCT_HARDWARE := {0}'.format(args_obj.HARD_VER),ih)
                    sys.stdout.write(new_line)
                else:
                    sys.stdout.write(ih)

def clean_bbtd():
    os.chdir('/data/mine/test/MT6572/jenkins/')
    print 'start to clean bbtd'
    for i in os.listdir(os.curdir):
        if os.path.isfile(i):
            os.remove(i)
        else:
            shutil.rmtree(i)

    os.chdir(pwd);os.chdir(CODE_DIR)
    time.sleep(10)

def successful_check(filename):
    old_pwd=os.getcwd()
    os.chdir('build-log')
    p1=subprocess.call('tail -n 10 {0} > result.log'.format(filename),shell=True)
    ex=False
    with open('result.log') as f:
        for i in f.readlines():
            result_len=re.findall(r'successfully',i)
            if result_len:
                ex=True
    if not ex:
        print('version build failed !!!!!')
        sys.exit()
    os.chdir(old_pwd)

def version_build():
    print "START TO BUILD VERSION"
    os.chdir(pwd);os.chdir(CODE_DIR)
    if os.path.isfile('/home/jenkins/project.info'):
        os.remove('/home/jenkins/project.info')

    new_project_info()
    os.chdir(pwd);os.chdir(CODE_DIR)
    if os.path.isfile('auto.sh'):
        result1=subprocess.Popen('./auto.sh',shell=True,stdin=subprocess.PIPE)
        if args_obj.OTAPACKAGE == 'true':
            result1.stdin.write('2 3'+os.linesep)
            result1.wait()
            successful_check('android.log')
            successful_check('otapackage.log')
        else:
            result1.stdin.write('2'+os.linesep)
            result1.wait()
            successful_check('android.log')
    else:
        print "error no auto.sh"
        sys.exit()
    if args_obj.MODULE != 'overall':
        clean_bbtd()

def release_version():
    print "START TO RELAESE VERSION"
    os.chdir(os.path.join(pwd,CODE_DIR))
    if args_obj.MODULE == 'all':
        if args_obj.VARIANT == 'eng':
            result1=subprocess.Popen('./release_version.sh {0} {1}'.format(args_obj.BUILD_PROJECT,args_obj.DOWNLOAD_TYPE),shell=True)
            result1.wait()
        elif args_obj.VARIANT == 'user':
            result1=subprocess.Popen('./release_version.sh {0} user'.format(args_obj.BUILD_PROJECT),shell=True)
            result1.wait()
    elif args_obj.MODULE == 'overall':
        if args_obj.VARIANT == 'eng':
            result1=subprocess.Popen('./release_version.sh {0} overall'.format(args_obj.BUILD_PROJECT),shell=True)
            result1.wait()
        elif args_obj.VARIANT == 'user':
            result1=subprocess.Popen('./release_version.sh {0} overall user'.format(args_obj.BUILD_PROJECT),shell=True)
            result1.wait()
    time.sleep(5)

def make_zip(source_dir,output_filename):
    zipf=zipfile.ZipFile(output_filename,'w',allowZip64=True,compression=zipfile.ZIP_DEFLATED)
    for path,sondir,filenames in os.walk(source_dir):
        if filenames:
            for filename in filenames:
                print 'Adding ',filename
                zipf.write(path+os.path.sep+filename)
    zipf.close()

def new_project_info():
    os.chdir('/home/jenkins/')
    with open('project.info','w') as pf:
        pf.write('type={0}'.format(args_obj.SAVE_TYPE)+os.linesep)
        pf.write('project={0}'.format(args_obj.PROJECT_NAME)+os.linesep)
        pf.write('custom={0}'.format(args_obj.BUILD_PROJECT.split('_')[1])+os.linesep)

        if args_obj.SAVE_TYPE in ('preofficial','factory','temp'):
            if os.path.exists('/jenkins/{0}_version/{1}/{2}/{3}'.format(args_obj.SAVE_TYPE,args_obj.PROJECT_NAME,args_obj.BUILD_PROJECT.split('_')[1],args_obj.IN_VERSION)):
                pf.write('version={0}_{1}'.format(args_obj.IN_VERSION,int(random.random()*1000))+os.linesep)
            else:
                pf.write('version={0}'.format(args_obj.IN_VERSION)+os.linesep)
        elif args_obj.SAVE_TYPE == 'dailybuild':
            if os.path.exists('/jenkins/{0}_version/{1}/{2}_dailybuild/{3}'.format(args_obj.SAVE_TYPE,args_obj.PROJECT_NAME,args_obj.BUILD_PROJECT.split('_')[1],today)):
                pf.write('version={0}_{1}'.format(today,int(random.random()*1000))+os.linesep)
            else:
                pf.write('version={0}'.format(today)+os.linesep)
            pf.write('option=custom:{0}_dailybuild'.format(args_obj.BUILD_PROJECT.split('_')[1])+os.linesep)
        pf.flush()

def normal_zip_version():
    os.chdir(os.path.join(pwd,CODE_DIR))
    make_zip(args_obj.IN_VERSION+'_DL','{0}.zip'.format(args_obj.IN_VERSION+'_DL'))
    shutil.copy('{0}.zip'.format(args_obj.IN_VERSION+'_DL'),'/data/mine/test/MT6572/jenkins/')
    shutil.rmtree(args_obj.IN_VERSION+'_DL')
    os.remove(args_obj.IN_VERSION+'_DL'+'.zip')

def archive_version():
    print "START TO ARCHIVE VERSION"
    os.chdir(os.path.join(pwd,CODE_DIR))
    global incre_no
    incre_no=args_obj.OUT_VERSION.split('-')[1]

    os.chdir(os.path.join(pwd,CODE_DIR))
    if os.path.exists(args_obj.IN_VERSION+'_DL'):
        shutil.rmtree(args_obj.IN_VERSION+'_DL')
    os.mkdir(args_obj.IN_VERSION+'_DL')
    for i in os.listdir('/data/mine/test/MT6572/jenkins/'):
        shutil.move('/data/mine/test/MT6572/jenkins/{0}'.format(i),'{0}/{1}'.format(args_obj.IN_VERSION+'_DL',i))

    new_project_info()

    if args_obj.DOWNLOAD_TYPE == 'qf':
        normal_zip_version()
    else:
        pass
    time.sleep(20)

def release_ota():
    print "START TO RELEASE OTA"
    if os.path.isfile('/home/jenkins/project.info'):
        os.rename('/home/jenkins/project.info','/home/jenkins/project.info_back')
    os.chdir(os.path.join(pwd,CODE_DIR))
    if args_obj.BUILD_PROJECT == 'E300L_IN':
        os.chdir('out/target/product/E300L_WW/system/')
    else:
        os.chdir('out/target/product/{0}/system/'.format(args_obj.BUILD_PROJECT))
    UL_type=''
    UL_sku=''
    UL_device='ASUS_X00P'
    for ih in fileinput.input('build.prop'):
        if len(re.findall(r'ro.build.type=.*',ih)):
            UL_type=ih.split('=')[1][:-1]
        elif len(re.findall(r'ro.build.asus.sku=.*',ih)):
            UL_sku=ih.split('=')[1][:-1]
    if not UL_type or not UL_sku:
        print('UL rename failed!!!')
        sys.exit()

    os.chdir(os.path.join(pwd,CODE_DIR))
    
    result1=subprocess.Popen('./release_version.sh {0} ota'.format(args_obj.BUILD_PROJECT),shell=True)
    result1.wait()
    time.sleep(5)
    if os.path.exists('ota_dir'):
        shutil.rmtree('ota_dir')
    os.mkdir('ota_dir')
    for i in os.listdir('/data/mine/test/MT6572/jenkins/'):
        if len(re.findall(r'ota',i)):
            shutil.move('/data/mine/test/MT6572/jenkins/{0}'.format(i),'ota_dir/UL-ASUS_X00P-{0}-{1}-{2}.zip'.format(UL_sku,incre_no,UL_type))
        else:
            shutil.move('/data/mine/test/MT6572/jenkins/{0}'.format(i),'ota_dir/'+i)
    
    if os.path.isfile('/home/jenkins/project.info_back'):
        os.rename('/home/jenkins/project.info_back','/home/jenkins/project.info')

    for i in os.listdir('ota_dir'):
        shutil.copy('ota_dir/'+i,'/data/mine/test/MT6572/jenkins/{0}'.format(i))
   
def do_snapshot():
    os.chdir(os.path.join(pwd,CODE_DIR))
    result1=subprocess.Popen('repoc manifest -ro manifest-{0}_{1}.xml'.format(args_obj.IN_VERSION,today),shell=True)
    result1.wait()
    shutil.copy('manifest-{0}_{1}.xml'.format(args_obj.IN_VERSION,today),'/data/mine/test/MT6572/jenkins/manifest-{0}_{1}.xml'.format(args_obj.IN_VERSION,today))

if __name__ == '__main__':
    args_parse()
    down_load_code(args_obj.CODE_URL,args_obj.CODE_BRANCH,args_obj.CODE_XML)
    #modified_hard_version()
    #modifed_auto_args()
    #version_build()
    #do_snapshot()
    #release_version()
    #archive_version()
    #release_ota()
