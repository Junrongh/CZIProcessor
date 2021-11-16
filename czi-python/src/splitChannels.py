import numpy as np
import czifile
import cv2
import os

def splitChannels(img, name):
    nchannels = img.shape[1]
    channels_info = {
        '0': 'blue'
    }
    if 'green' in name:
        channels_info['1'] = 'green'
        if 'red' in name:
            channels_info['2'] = 'red'
    elif 'red' in name:
        channels_info['1'] = 'red'

    dic = {}
    k = 0
    for i in range(nchannels):
        channel = img[0, k, 0, 0, :, :, 0]
        channel = cv2.convertScaleAbs(channel, alpha=(255.0/4095.0))

        if np.min(channel > 5.0):
            dic['bright'] = channel.astype('uint8')
        else:
            dic[channels_info[str(k)]] = channel.astype('uint8')
            k += 1

    return dic


if __name__ == '__main__':
    f = open('input.txt')
    lines = f.readlines()
    f.close()
    nfiles = len(lines)

    root = '../tuned'
    cziRoot = '../data'
    if not os.path.isdir(root):
        os.mkdir(root)

    for i in range(nfiles):
        in_file = lines[i].strip()
        name = in_file.split('.czi')[0]
        name = name.replace(' ', '_')
        outRoot = os.path.join(root, name)
        cziFileRoot = os.path.join(cziRoot, in_file)
        if not os.path.isdir(outRoot):
            os.mkdir(outRoot)

        img = czifile.imread(cziFileRoot)

        a, channels, b, c, m, n, d = img.shape
        print("Image info: {}".format(name))
        print("    this image has {} channels".format(channels))
        print("    with width {} and height {}".format(m, n))

        data = splitChannels(img, name)
        brightFieldPath = os.path.join(outRoot, '{}_brightField.jpg'.format(name))
        cv2.imwrite(brightFieldPath, data.get('bright'))

        img = np.zeros([m, n, 3])
        if data.get('blue') is not None:
        	img[:, :, 0] = data.get('blue')
        if data.get('green') is not None:
        	img[:, :, 1] = data.get('green')
        if data.get('red') is not None:
        	img[:, :, 2] = data.get('green')
        channelPath = os.path.join(outRoot, '{}_channels.jpg'.format(name))
        cv2.imwrite(channelPath, img)



