import os
import imageio

def make_gif(path='output/screenshots', name='output/movie.gif'):
    print('reading images ...')
    files = os.listdir(path)
    images = [imageio.imread(os.path.join(path, f)) for f in files]
    print('writing images to', name, '...')
    imageio.mimsave(name, images, fps=300)