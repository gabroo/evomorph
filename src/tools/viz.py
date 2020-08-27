import os
import imageio

def make_gif(imgdir, filename, fps=20):
    files = sorted(os.listdir(imgdir))
    images = [imageio.imread(os.path.join(imgdir, f)) for f in files]
    imageio.mimwrite(filename, images, format='gif', fps=fps)
