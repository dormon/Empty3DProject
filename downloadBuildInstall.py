#!/usr/bin/python

import externLibraries
import myCmakeLibraries

gits = externLibraries.gits + myCmakeLibraries.gits 

import sys
import os
from subprocess import call
from subprocess import Popen, PIPE
import argparse
import re
import shutil

parser = argparse.ArgumentParser(description='Download/pull all Shadows dependencies, compile and install them.')
parser.add_argument('--threads', type=int, default=4,  help='number of threads for compilation')
parser.add_argument('--dontBuildDebug',action='store_true')
parser.add_argument('--dontBuildRelease',action='store_true')
parser.add_argument('--installDir', type=str, default="install", help='where to install all repositories')
parser.add_argument('--repoDir', type=str, default="externRepositories", help='where to download repositories')
parser.add_argument('--dontPull', action='store_true')
parser.add_argument('--clearBuild', action='store_true')

args = parser.parse_args()

threads      = args.threads
buildDebug   = not args.dontBuildDebug
buildRelease = not args.dontBuildRelease
installDir   = args.installDir
repoDir      = args.repoDir
curDir       = os.path.abspath(".")
dontPull     = args.dontPull
clearBuild   = args.clearBuild

system = sys.platform

def getGCC():
    GCCs = ["g++","g++-5","g++-6","g++-7"]
    standards = ["--std=c++14","--std=c++17"]
    
    def hasGCC(what):
        p = Popen(["which",what],stdout=PIPE,stderr=PIPE)
        p.communicate()
        return not p.returncode
    
    hasGCCs = map(lambda x:hasGCC(x),GCCs)
    
    if not reduce(lambda x,y:x or y,hasGCCs):
        print ("there is no g++")
        exit(0)
    
    def getVersion(whatGCC):
        versionLine = Popen([whatGCC,"--version"],stdout=PIPE,stderr=PIPE).communicate()[0].split("\n")[0];
        return re.sub(".*\s([0-9](\\.[0-9])+).*","\\1",versionLine)
    
    def isVersionLess(a,b):
        a = a.split(".")
        b = b.split(".")
        while len(a) < len(a):
            a += ["0"]
        while len(b) < len(a):
            b += ["0"]
        ab = zip(a,b)
        for i in ab:
            if int(i[0]) >= int(i[1]):
                return False
        return True
    
    def getNewestGCC():
        allGCCs = zip(GCCs,hasGCCs)
        existingGCCs = filter(lambda x:x[1],allGCCs)
        existingGCCs = map(lambda x:x[0],existingGCCs)
        versions = map(lambda x:getVersion(x),existingGCCs)
        gccWithVersion = zip(existingGCCs,versions)
        newestGCC = reduce(lambda x,y:x if isVersionLess(x[1],y[1]) else y,gccWithVersion)[0]
        return newestGCC
    
    gcc = getNewestGCC()
    
    def supportStandard(standard):
        return not (Popen([gcc,standard],stdout=PIPE,stderr=PIPE).communicate()[0].find("unrecognized") >= 0)
    
    supportedStandards = map(lambda x:supportStandard(x),standards)
    
    if not reduce(lambda x,y:x or y,supportedStandards):
        print ("your g++ is too old and does not support required C++ standard: ",standards[0])
        exit(0)
    
    def getNewestStandard():
        return filter(lambda x:x[1],zip(standards,supportedStandards))[-1][0]
    
    standard = getNewestStandard();
    return (gcc,standard)



gcc = ("","")
if system.find("linux") >= 0:
    gcc = getGCC()

if not os.path.isabs(installDir):
    installDir = os.path.join(os.path.abspath("."),installDir)

installDir = os.path.join(installDir,system)

if not os.path.isdir(installDir):
    os.makedirs(installDir)

if not os.path.isabs(repoDir):
    repoDir = os.path.join(os.path.abspath("."),repoDir)

if not os.path.isdir(repoDir):
    os.makedirs(repoDir)

def getGitDirectory(url):
    return url[url.rfind("/")+1:url.rfind(".")]

def clone(url,commit = ""):
    os.chdir(repoDir)
    gitDir = getGitDirectory(url)
    if not os.path.isdir(gitDir):
        print ("cloning: "+gitDir)
        call(["git","clone",url])
    else:
        print ("executing git pull on: "+gitDir)
        if not dontPull:
            os.chdir(gitDir)
            call(["git","pull"])
            os.chdir("..")

    if commit != "":
        os.chdir(gitDir)
        print ("checkout: "+commit)
        call(["git","checkout",commit])
        os.chdir("..")

    os.chdir(curDir)



debugBuildDir = "build/"+system+"/debug"
releaseBuildDir = "build/"+system+"/release"

systemSpecificDebugBuildOptions = []
systemSpecificReleaseBuildOptions = []

if system.find("linux") >= 0:
    systemSpecificDebugBuildOptions   = ["-j"+str(threads),"install"]
    systemSpecificReleaseBuildOptions = ["-j"+str(threads),"install"]
else:
    systemSpecificDebugBuildOptions = ["/p:CL_MPCount="+str(threads),"/p:Configuration=Debug"]
    systemSpecificReleaseBuildOptions = ["/p:CL_MPCount="+str(threads),"/p:Configuration=Release"]




def buildAndInstall(url,args = []):
    os.chdir(repoDir)
    dirName = getGitDirectory(url)
    os.chdir(dirName)
    if clearBuild:
       shutil.rmtree(debugBuildDir)
       shutil.rmtree(releaseBuildDir)
       #if os.path.isfile(debugBuildDir+"/CMakeCache.txt"):
       #    os.remove(debugBuildDir+"/CMakeCache.txt")
       #if os.path.isfile(releaseBuildDir+"/CMakeCache.txt"):
       #    os.remove(releaseBuildDir+"/CMakeCache.txt")
    if not os.path.isdir(debugBuildDir):
       os.makedirs(debugBuildDir)
    if not os.path.isdir(releaseBuildDir):
       os.makedirs(releaseBuildDir)

    basicArgs  = ["cmake","-DCMAKE_INSTALL_PREFIX="+installDir,"-DBUILD_SHARED_LIBS=ON"] 

    if system.find("linux") >= 0:
        basicArgs += ["-DCMAKE_CXX_COMPILER="+gcc[0],"-DCMAKE_CXX_FLAGS="+gcc[1]]
    else:
        basicArgs += ["-GVisual Studio 15 2017 Win64"]

    if buildDebug:
        call(basicArgs+args+["-H.","-B"+debugBuildDir,"-DCMAKE_BUILD_TYPE=Debug"])
        call(["cmake","--build",debugBuildDir,"--target","install","--"] + systemSpecificDebugBuildOptions)
    
    if buildRelease:
        call(basicArgs+args+["-H.","-B"+releaseBuildDir,"-DCMAKE_BUILD_TYPE=Release"])
        call(["cmake","--build",releaseBuildDir,"--target","install","--"] + systemSpecificReleaseBuildOptions)

for i in gits:
    clone(i[0],i[1])

for i in gits:
    buildAndInstall(i[0],i[2])
