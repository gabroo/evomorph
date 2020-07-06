import os
import imageio

def make_gif(path='output/screenshots', name='output/movie.gif'):
    print('reading images ...')
    files = sorted(os.listdir(path))
    images = [imageio.imread(os.path.join(path, f)) for f in files]
    print(files[0], files[1], files[2])
    print('writing images to', name, '...')
    imageio.mimsave(name, images, fps=20)