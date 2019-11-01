#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Regents of the University of Ottawa and the Center

import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from os import curdir
from os.path import join as pjoin
import json
import os
import sys
import base64
import ssl
import SocketServer
import glob
from xml.etree import ElementTree as ET
import xml.dom.minidom as minidom
import datetime

key = ""
CERTFILE_PATH = "./TAserver.pem"

class PathFinder(object):
    @staticmethod
    def pathfinder():
        listpat = []
        for root,dirs,files in os.walk(os.getcwd()):
            for file in files:
               if file.endswith(('.xml')) :
                  #print (os.path.join(root,file))
                  listpat.append(os.path.join(root,file))
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),'mup')):
            listpat.append(root)
        ListPath = []
        for i in range(len(listpat)):
            temp = listpat[i]
            temp = temp.replace("\\", "/" )
            temp = temp.replace('.xml', '')
            cwd = os.getcwd()
            cwd = cwd.replace("\\", "/" )
            ListPath.append(temp.replace(cwd,''))
        list_path = list()
        for item in ListPath:
            list_path.append(item.rsplit('/', 1)[0])
        list_path = set(list_path)
        list_path = list(set(list_path))
        return list_path
    @staticmethod
    def ResPathfinder():
        ResListPath = []
        P = PathFinder()
        ListPath = P.pathfinder()
        for item in ListPath:
            if item.startswith('/rsps') or ('/lsa/' in item):
                ResListPath.append(item)
        return filter(None, ResListPath)
    @staticmethod
    def mupPathfinder():
        ResListPath = []
        P = PathFinder()
        ListPath = P.pathfinder()
        for item in ListPath:
            if item.startswith('/mup'):
                ResListPath.append(item)
        return filter(None, ResListPath)
    

class CreditReader(object):
    @staticmethod
    def ReadCredit():
        with open('credentials.json') as json_data:
            d = json.load(json_data)
        CreditList = []
        for i in range(len(d)):
            First = d[i]["Username"].encode('ascii','ignore')
            Second =d[i]["Password"].encode('ascii','ignore') 
            crd = First + ":" + Second
            crd = base64.b64encode(crd)
            crd =  'Basic ' + crd
            CreditList.append(crd)
        return CreditList

class ListMakerClass(object):
    @staticmethod
    def ListMaker(directory, List, File, href, results, subscribable, start, after):
        direc = directory + href
        print direc
        xml_dir = list()
        for root, dirs, files in os.walk(direc):
            for file in files:
                if file.endswith(File + ".xml"):
                    xml_dir.append(os.path.join(root, file))

        if results == None:
            results = len(xml_dir)
        if start == None:
            start = 0
        if after == None:
            after = 0
            
        if start + results > len(xml_dir):
            results = len(xml_dir) - start
        if start > len(xml_dir):
            start = len(xml_dir) - 1
            results = 1
        if after > len(xml_dir):
            after = len(xml_dir)

        xml_dir = xml_dir[start:results]
        href = list(href)
        del(href[-1])
        href = "".join(href)
        hrefNew = list(href)
        del(hrefNew[0])
        hrefNew = "".join(hrefNew)
        File = List.split('List')[0]
        EDCL = ET.Element("{http://zigbee.org/sep}" + List, all = str(len(xml_dir)), href = href, results = str(results), subscribable = subscribable)
        for xml_file in xml_dir:
            Href = xml_file
            Href = Href.replace(directory,'')
            Href = Href.replace('\\'+ File + '.xml','')
            Href = Href.replace('/'+ File + '.xml','')
            Href = Href.replace('\\','/')

            ET.register_namespace('','http://zigbee.org/sep')
            data = ET.parse(xml_file).getroot()

            for result in data.iter('{http://zigbee.org/sep}' + File):
                EDC = ET.SubElement(EDCL, '{http://zigbee.org/sep}' + File, href = Href)
                EDC.extend(result)
        if EDCL != None:
            tree = ET.ElementTree(EDCL)
            tree.write(os.path.join(directory, hrefNew ,List+".xml"), xml_declaration=False, method='xml', encoding='utf-8')
            return ET.tostring(EDCL, 'utf-8')

    @staticmethod
    def ListPath(path): #TODO
        hrefList = {"fsa":"FunctionSetAssignmentsList",
                    "edev":"EndDeviceList",
                    "rsps":"ResponseSetList", 
                    "rsp":"ResponseList", 
                    "dr":"DemandResponseProgramList", 
                    "edc":"EndDeviceControlList", 
                    "upt":"UsagePointList", 
                    "mr":"MeterReadingList", 
                    "rs":"ReadingSetList", 
                    "r":"ReadingList", 
                    "mup":"MirrorUsagePointList"}
        a = path.split('/')
        List = hrefList[a[-1]]
        href = ''
        for item in a:
            href = href + item + '/'       
        File = List.split('List')[0]
        return href, List, File

    @staticmethod
    def FilePath(path): 
        hrefs = {"fsa":"FunctionSetAssignments",
                 "edev":"EndDevice",
                 "sub":"Subscription", 
                 "ntfy":"Notification", 
                 "rsps":"ResponseSet", 
                 "rsp":"Response", 
                 "dr":"DemandResponseProgram", 
                 "edc":"EndDeviceControl", 
                 "upt":"UsagePoint", 
                 "mr":"MeterReading", 
                 "rs":"ReadingSet", 
                 "r":"Reading", 
                 "mup":"MirrorUsagePoint", 
                 "rg":"Registration",
                 "lsa":"LoadShedAvailability",
                 "rt":"ReadingType"}
        a = path.split('/')
        if a[-2] in hrefs:
            File = hrefs[a[-2]]+".xml"
        else:
            File = hrefs[a[-1]]+".xml"

        href = ''
        for item in a:
            href = href + item + '/'
    
        path = href + File
        return File, href, path
    
class AuthHandler(SimpleHTTPRequestHandler):
    def dumpRequest(self):
        print('    Got HTTP %s from %s' % (self.command, self.client_address))
        print('    Path=%s' % (self.path,))
        print('    Version=%s' % (self.request_version,))
        print('    Headers=%s' % (self.headers,))
		
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print "send header"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "send authentication"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        print  self.dumpRequest()
        MainWadlList = ['/edev', '/rsps', '/rsp', '/dr', '/edc', '/upt', '/mr', '/rs', '/r', '/mup', '/fsa']
        
        P = PathFinder()
        ListPath = P.pathfinder()
        Cr = CreditReader()
        CreditList = Cr.ReadCredit() 
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') in CreditList:
            try:
                if "/"+("dr/1/edc".split('?',1)[0]).split('/')[-1] in MainWadlList: #(ListPath + MainWadlList):
                    TempPath = self.path.split('?',1)[0]
                    if '/' + (TempPath.rsplit('/', 1)[-1]) in MainWadlList:
                        results = None
                        start = None
                        after = None
                        if '?s' in (self.path) or '?a' in (self.path):
                            Query = self.path.split('?',1)[1]
                            try:
                                start = int(Query[Query.find('s=')+len('s='):Query.rfind('&')])
                            except:
                                start = 0
                                pass
                            try:
                                after = int(Query[Query.find('&a=')+len('&a='):Query.rfind('&')])
                            except:
                                after = 0
                                pass
                            try:
                                limit = int(Query[Query.find('&l=')+len('&l='):Query.rfind('')])
                            except:
                                limit = 1
                                pass
                            results = limit
                            LMC = ListMakerClass()
                            href, List, File = LMC.ListPath(TempPath)
                            if ('?s' not in (self.path) and '?l' not in (self.path)) or \
                               ('?s' not in (self.path) and '?a' not in (self.path)) or \
                               ('?s' not in (self.path) and '?l' not in (self.path) and '?a' not in (self.path)):
                                self.send_response(422)
                                self.send_header('Content-type', 'text/xml')
                                self.end_headers()
                                self.wfile.write(fh.read().encode())
                        else:
                            LMC = ListMakerClass()
                            href, List, File = LMC.ListPath(TempPath)

                        TempPath = list(TempPath)    
                        del(TempPath[0])
                        TempPath = "".join(TempPath)
                        TempPath = TempPath + '/' + List + '.xml'
                        get_path = pjoin(curdir, TempPath)
                        subscribable = "0"
                        LMC.ListMaker(os.getcwd(), List, File, href, results, subscribable, start, after)
                        
                        with open(get_path) as fh:
                            self.send_response(200)
                            self.send_header('Content-type', 'text/xml')
                            self.end_headers()
                            self.wfile.write(fh.read().encode())
                    elif ('/' + TempPath.split('/')[1]) in MainWadlList:
                        TempPath = list(TempPath)
                        del(TempPath[0])
                        TempPath = "".join(TempPath)
                        LMC = ListMakerClass()
                        File, href, path = LMC.FilePath(TempPath)
                        get_path = pjoin(curdir, path)
                        with open(get_path) as fh:
                            self.send_response(200)
                            self.send_header('Content-type', 'text/xml')
                            self.end_headers()
                            self.wfile.write(fh.read().encode())
                    else:
                        self.send_response(406)
                        self.send_header('Content-type', 'text/xml')
                        self.end_headers()
                else:
                    self.send_response(405)
                    self.send_header('Content-type', 'text/xml')
                    self.end_headers()
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                #self.wfile.write(fh.read().encode())
                pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass

    def do_PUT(self):
        global key
        print  self.dumpRequest()
        MainWadlList = ["ResponseSetList","ResponseList","DrResponse","DemandResponseProgramList",\
                        "LoadShedAvailability","ReadingType","Reading","MirrorUsagePoint"]

        Cr = CreditReader()
        CreditList = Cr.ReadCredit()
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') in CreditList:
            TempPath = self.path
            if TempPath.endswith('/'):
                TempPath = list(TempPath)
                del(TempPath[-1])
                TempPath = "".join(TempPath)
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            root = ET.fromstring(data)
            Tag = (root.tag).rsplit("}")[-1]
            href = root.attrib['href']
            try:
                subscrib =int(root.attrib['subscribable'])
            except:
                pass
            if Tag in MainWadlList:
                TempPath = list(TempPath)
                del(TempPath[0])
                TempPath = "".join(TempPath)
                get_path = pjoin(curdir, TempPath)
                if os.path.exists(get_path):
                    get_path = get_path + "/" + Tag + ".xml"
                    with open(get_path, 'w') as fh:
                        fh.write(data.decode())
                    self.send_response(201)
            else:
                self.send_response(204)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass

    def do_POST(self):
        global key
        print  self.dumpRequest()
        MainWadlList = ["EndDeviceList","ResponseList","UsagePointList","MeterReadingList","ReadingSetList",\
                        "ReadingList","MirrorUsagePointList","MirrorUsagePoint",] 
        Cr = CreditReader()
        CreditList = Cr.ReadCredit()
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') in CreditList:
            TempPath = self.path
            if TempPath .endswith('/'):
                TempPath = list(TempPath)
                del(TempPath[-1])
                TempPath = "".join(TempPath)
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            root = ET.fromstring(data)
            Tag = (root.tag).rsplit("}")[-1]
            href = root.attrib['href']             
            subscrib =int(root.attrib['subscribable'])
            if Tag in MainWadlList:
                TempPath = list(TempPath)
                #TempPath = list(href)
                del(TempPath[0])
                TempPath = "".join(TempPath)
                get_path = pjoin(curdir, TempPath)
                if not os.path.exists(get_path):
                    os.makedirs(get_path)
                    get_path = get_path + "/" + Tag + ".xml"
                    with open(get_path, 'w') as fh:
                        fh.write(data.decode())
                    self.send_response(204)
                else:
                    get_path = get_path + "/" + Tag + ".xml"
                    with open(get_path, 'w') as fh:
                        fh.write(data.decode())
                    self.send_response(201)
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()
                pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass

    def do_DELETE(self):
        global key
        print  self.dumpRequest()
        MainWadlList = ["edev", "rg", "dstat", "di", "lsa", "upt", "cdp"]
        SubWadlList = ["sub", "rsp", "rsp", "rsp", "rsp", "upt", "mr", "rs", "r", "mup"]

        Cr = CreditReader()
        CreditList = Cr.ReadCredit()
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') in CreditList:
            TempPath = self.path
            if TempPath .endswith('/'):
                TempPath = list(TempPath)
                del(TempPath[-1])
                TempPath = "".join(TempPath)
            if ((TempPath.rsplit('/', 1)[-1]) in MainWadlList) or \
               ((TempPath.rsplit('/')[-2]) in SubWadlList):
                TempPath = list(TempPath)
                del(TempPath[0])
                TempPath = "".join(TempPath)
                Del_path = pjoin(curdir, TempPath)
                print Del_path
                try:
                    for root, dirs, files in os.walk(Del_path):
                        for f in files:
                            if f.endswith(".xml"):
                                os.remove(os.path.join(root, f))
                    self.send_response(200)
                except OSError:
                    self.send_response(204)
                    pass
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/xml')
                self.end_headers()                
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass
        
def run(PORT):

    server_address = ("", PORT)
    BaseHTTPServer.HTTPServer.allow_reuse_address = True
    httpd = BaseHTTPServer.HTTPServer(server_address, AuthHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./TAserver.pem', ssl_version=ssl.PROTOCOL_TLSv1_2, server_side=True,\
                                   cert_reqs = ssl.CERT_REQUIRED, ca_certs="./ca-certificates.crt", do_handshake_on_connect=True, suppress_ragged_eofs=True)
	
    print('http server is running at: ', httpd.socket.getsockname())
    try:
        httpd.serve_forever(0.5)
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "usage Server.py [port]"
        sys.exit()
    https_port = int(sys.argv[1])

    if len(sys.argv) == 3:
        change_dir = sys.argv[2]
        print "Changing dir to {cd}".format(cd=change_dir)
        os.chdir(change_dir)
    run(https_port)