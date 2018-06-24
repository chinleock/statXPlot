## Class XH1
import math, os, sys
import numpy as np
from XDebug import *
        
class XH1:
    def __init__(self, name, bins, xmin, xmax):
        self.name = name
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax
        self.hist = np.array([])
        self.bin_edges = np.array([])
        self.errors = np.array([])
    
    def Fill(self, x, weights=None):
        
        ## Fill histogram
        lowerfloat = 0.
        upperfloat = 0.
        if weights is None:
            hist, self.bin_edges = np.histogram(x, bins=self.bins, range=(self.xmin, self.xmax))
            lowerfloat = len(x[x<self.bin_edges[0]])
            upperfloat = len(x[x>self.bin_edges[self.bins]])
            ### Fill errors
            self.errors = np.hstack([self.errors, np.sqrt(lowerfloat)])
            self.errors = np.hstack([self.errors, np.sqrt(hist)])
            self.errors = np.hstack([self.errors, np.sqrt(upperfloat)])
        else:
            x_wrt = np.hstack([x, weights])
            
            hist_sumw2 = np.array([])
            hist, self.bin_edges = np.histogram(x, bins=self.bins, range=(self.xmin, self.xmax), weights=weights)
            for bin in range(self.bins-1):
                sumw2 = 0.
                for wrt in x_wrt[(x_wrt[:,0]>=self.bin_edges[bin]) & (x_wrt[:,0]<self.bin_edges[bin+1]) ][:,1]:
                    sumw2 += wrt*wrt
                hist_sumw2 = np.hstack([hist_sumw2, sumw2])
            
            lowerfloat_sumw2 = 0.
            upperfloat_sumw2 = 0.
            for wrt in x_wrt[x_wrt[:,0]<self.bin_edges[0]][:,1]: 
                lowerfloat += wrt
                lowerfloat_sumw2 += wrt*wrt 
            for wrt in x_wrt[x_wrt[:,0]>self.bin_edges[self.bins]][:,1]: 
                upperfloat += wrt
                upperfloat_sumw2 += wrt*wrt
            ### Fill errors
            self.errors = np.hstack([self.errors, np.sqrt(lowerfloat_sumw2)])
            self.errors = np.hstack([self.errors, np.sqrt(hist_sumw2)])
            self.errors = np.hstack([self.errors, np.sqrt(upperfloat_sumw2)])          
        
        self.hist = np.hstack([self.hist, lowerfloat])
        self.hist = np.hstack([self.hist, hist])
        self.hist = np.hstack([self.hist, upperfloat])
        
        return self
    
    def Clone(self, name=''):
        h = XH1(name, self.bins, self.xmin, self.xmax)
        h.hist      = self.hist
        h.bin_edges = self.bin_edges
        h.errors    = self.errors
        return h
    
    def SetName(self, name):
        self.name = name
        return self
        
    def GetBinContent(self, bin):
        if not is_inBins(bin, self.bins): return 0
        return np.asscalar(self.hist[bin])
    
    def GetBinContentByEdge(self, edge):
        if not is_inEdges(edge, self.bin_edges): return 0
        idx = np.argwhere(self.bin_edges == edge).reshape(1)
        return np.asscalar(self.hist[idx])


    def Add(self, h1, scale=1.):
        if not is_samebins(self.bins, h1.bins): return self
        self.hist = self.hist + scale*h1.hist
        return self
    
    def Divide(self, h1, scale=1.):
        if not is_samebins(self.bins, h1.bins): return self
        self.hist = self.hist/(scale*h1.hist)
        return self
    
    def Multiply(self, h1, scale=1.):
        if not is_samebins(self.bins, h1.bins): return self
        self.hist = self.hist*scale*h1.hist
        return self
        
    def __add__(self, h1):
        if not is_samebins(self.bins, h1.bins): return self
        h = self.Clone()
        h.hist = h.hist + h1.hist
        return h
    
    def __sub__(self, h1):
        if not is_samebins(self.bins, h1.bins): return self
        h = self.Clone()
        h.hist = h.hist - h1.hist
        return h
    
    def __truediv__(self, h1):
        if not is_samebins(self.bins, h1.bins): return self
        h = self.Clone()
        h.hist = h.hist/h1.hist
        return h
    
    def __mul__(self, h1):
        if not is_samebins(self.bins, h1.bins): return self
        h = self.Clone()
        h.hist = h.hist*h1.hist
        return h

    
        