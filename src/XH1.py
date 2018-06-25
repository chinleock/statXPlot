## Class XH1
import math, os, sys
import numpy as np
import matplotlib.pyplot as plt
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

        ## Draw option
        self.ylog      = False
        self.linewidth = 0
        #self.edgecolor = 1
    
    def Fill(self, x, weights=None):
        
        ## Fill histogram
        lowerflow = 0.
        upperflow = 0.
        if weights is None:
            hist, self.bin_edges = np.histogram(x, bins=self.bins, range=(self.xmin, self.xmax))
            lowerflow = len(x[x<self.bin_edges[0]])
            upperflow = len(x[x>self.bin_edges[self.bins]])
            ### Fill errors
            self.errors = np.hstack([self.errors, np.sqrt(lowerflow)])
            self.errors = np.hstack([self.errors, np.sqrt(hist)])
            self.errors = np.hstack([self.errors, np.sqrt(upperflow)])
        else:
            x_wrt = np.hstack([x, weights])
            
            hist_sumw2 = np.array([])
            hist, self.bin_edges = np.histogram(x, bins=self.bins, range=(self.xmin, self.xmax), weights=weights)
            for bin in range(self.bins):
                sumw2 = 0.
                for wrt in x_wrt[(x_wrt[:,0]>=self.bin_edges[bin]) & (x_wrt[:,0]<self.bin_edges[bin+1]) ][:,1]:
                    print( self.bin_edges[bin], self.bin_edges[bin+1])
                    sumw2 += wrt*wrt
                hist_sumw2 = np.hstack([hist_sumw2, sumw2])
            
            lowerflow_sumw2 = 0.
            upperflow_sumw2 = 0.
            for wrt in x_wrt[x_wrt[:,0]<self.bin_edges[0]][:,1]: 
                lowerflow += wrt
                lowerflow_sumw2 += wrt*wrt 
            for wrt in x_wrt[x_wrt[:,0]>self.bin_edges[self.bins]][:,1]: 
                upperflow += wrt
                upperflow_sumw2 += wrt*wrt
            ### Fill errors
            self.errors = np.hstack([self.errors, np.sqrt(lowerflow_sumw2)])
            self.errors = np.hstack([self.errors, np.sqrt(hist_sumw2)])
            self.errors = np.hstack([self.errors, np.sqrt(upperflow_sumw2)])          
        
        self.hist = np.hstack([self.hist, lowerflow])
        self.hist = np.hstack([self.hist, hist])
        self.hist = np.hstack([self.hist, upperflow])
        return self
    
    def Draw(self, overflow=False):
        print(self.errors[1:-1])
        print(np.array(self.errors[1:-1]).shape)
        plt.figure(figsize=(16,10))
        plt.bar(self.bin_edges[:-1], self.hist[1:-1], width=self.GetBinWidth(), align='edge', yerr=self.errors[1:-1], 
                log=self.ylog, 
                linewidth=self.linewidth)
        plt.xlim(self.xmin, self.xmax)


    def Clone(self, name=''):
        h = XH1(name, self.bins, self.xmin, self.xmax)
        h.hist      = self.hist
        h.bin_edges = self.bin_edges
        h.errors    = self.errors
        return h
    
    def SetName(self, name):
        self.name = name
        return self
       

    # def Fit(self):
    # def ReBin(self):
    # def Integral(self):
    ## Add error propagation in +-*/
    # def GetEntries(self):
    # def GetMax(self):
    # def GetMin(self):


    def GetBinWidth(self):
        if self.bins > 1:
            return self.bin_edges[1]-self.bin_edges[0]
        else:
            return 0

    def GetBinContent(self, bin):
        if not is_inBins(bin, self.bins): return 0
        return np.asscalar(self.hist[bin])
    
    def GetBinContentByEdge(self, edge):
        if not is_inEdges(edge, self.bin_edges): return 0
        idx = np.argwhere(self.bin_edges == edge)
        return np.asscalar(self.hist[idx])

    def GetBinError(self, bin):
        if not is_inBins(bin, self.bins): return 0
        return np.asscalar(self.errors[bin])
    
    def GetBinErrorByEdge(self, edge):
        if not is_inEdges(edge, self.bin_edges): return 0
        idx = np.argwhere(self.bin_edges == edge)
        return np.asscalar(self.errors[idx])
    
    def Scale(self, value ):
        self.hist   = self.hist   * value
        self.errors = self.errors * value
        return self


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

