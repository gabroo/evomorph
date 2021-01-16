import os
import re
import concurrent.futures as conc
from pathlib import Path

import pandas as pd
import numpy as np

import vtk
from vtk.util.numpy_support import vtk_to_numpy
from ipyvtk_simple.viewer import ViewInteractiveWidget

import ipyvolume as ipv
from scipy.spatial import distance_matrix

from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn import metrics

class Frame:
    def __init__(self, path, dim=(100, 100, 100)):
        reader = vtk.vtkStructuredPointsReader()
        reader.SetFileName(path)
        reader.ReadAllScalarsOn()
        reader.Update()
        out = reader.GetOutput()
        d = out.GetPointData()
        names = [d.GetArrayName(i) for i in range(3)] 
        fields =  {n: vtk_to_numpy(d.GetArray(n)) for n in names} 
        types, cells = fields['CellType'] , fields['CellId']
        
        self.types = types.reshape(*dim)
        self.cells = cells.reshape(*dim)
        self.mcs = int(re.search('Step_(\d+).vtk', path).groups()[0])
        self.dim = dim
        
    def as_points(self):
        # returns the cells as 3D points
        dim = np.array(self.dim)
        points = np.vstack(np.unravel_index(np.arange(dim.prod()), dim))
        return points.T
        
    def show(self):
        # shows this frame in an ipyvolume frame
        points = self.as_points()
        for t in np.unique(self.types):
            fig = ip
            ipv.quickscatter(celldf.x.values, celldf.y.values, celldf.z.values, size=1, color=celldf.type, marker="box")
            
    def cluster(self, eps=2):
        points = self.as_points()
        types = self.types.flatten()
        cells = points[types != 0]
        celltypes = types[types != 0]
        db = DBSCAN(eps=eps, min_samples=10).fit(cells)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        unique_labels = set(labels)
        colors = [plt.cm.Spectral(each)
                  for each in np.linspace(0, 1, len(unique_labels))]

        cluster = None
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = (labels == k)

            xyz = cells[class_member_mask & core_samples_mask]
            if cluster is None or len(cluster) < len(xyz):
                cluster = xyz

        return np.array(cluster)

    def variance_ratio(self, plot=False):
        points = self.cluster()
        com = np.mean(points, axis=0)
        model = PCA(n_components=2)
        res = model.fit(points)
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.scatter3D(points[:, 0], points[:, 1], points[:, 2], alpha=0.05)
            comp = (res.components_.T * res.explained_variance_).T
            ax.quiver3D(com[0], com[1], com[2], comp[0, 0], comp[0, 1], comp[0, 2], color='red')
            ax.quiver3D(com[0], com[1], com[2], comp[1, 0], comp[1, 1], comp[1, 2], color='green')
        return (self.mcs, res.explained_variance_ratio_)
            
        
class Movie:
    def __init__(self, path):
        self.path = os.path.join(path, 'LatticeData')
        files = os.listdir(self.path)
        print(f'reading {len(files)} frames from {self.path}')
        
        with conc.ProcessPoolExecutor() as ex:
            frames = ex.map(Frame, [os.path.join(self.path, file) for file in files if file.endswith('.vtk')])
            self.frames = sorted(frames, key=lambda x: x.mcs)

        self.t_max = len(self.frames)-1
        assert self.t_max > 0
    
    def frame_by_mcs(self, t):
        for frame in self.frames:
            if frame.mcs == t:
                return frame
        return None
    def frame_by_idx(self, i):
        if i >= 0 and i < len(self.frames):
            return self.frames[i] 
        return None
    
    def frames(self):
        return self.frames
    
    def variance_ratios(self):
        return [f.variance_ratio() for f in self.frames]

if __name__ == '__main__':
    path = Path('../threshold4k/gen_001/').resolve()
    with conc.ProcessPoolExecutor() as ex:
        movies = ex.map(Movie, [sim for sim in path.iterdir()])
    np.save(np.array([m.variance_ratios() for m in movies]))
