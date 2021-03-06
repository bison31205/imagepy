# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from core.roi import polygonroi
import wx
from .polygon_tol import Polygonbuf
from core.engines import Tool

class Plugin(Tool):
    """FreeArea class plugin with events callbacks"""
    title = 'Free Area'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.oper = ''
        self.helper = Polygonbuf()
            
    def mouse_down(self, ips, x, y, btn, **key): 
        lim = 5.0/key['canvas'].get_scale() 
        ips.mark = self.helper
        if btn==1:
            if not self.doing:
                if ips.roi!= None:
                    self.curobj = ips.roi.pick(x, y, lim)
                if not self.curobj in (None,True):return
                self.oper = '+'
                if ips.roi == None:
                    ips.roi = polygonroi.PolygonRoi()
                    self.doing = True
                elif hasattr(ips.roi, 'topolygon'):
                    ips.roi = ips.roi.topolygon()
                    if key['shift']: self.oper,self.doing = '+',True
                    elif key['ctrl']: self.oper,self.doing = '-',True
                    elif self.curobj: return
                    else: ips.roi=None
                else: ips.roi = None
            if self.doing:
                self.helper.addpoint((x,y))
                self.odx, self.ody = x, y
        ips.update = True
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.doing:
            self.helper.addpoint((x,y))
            self.doing = False
            self.curobj = None
            ips.roi.commit(self.helper.pop(), self.oper)
        ips.update = True
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        lim = 5.0/key['canvas'].get_scale()
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.roi.snap(x, y, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            if self.doing:
                self.helper.addpoint((x,y))
            elif self.curobj: ips.roi.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update = True
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass