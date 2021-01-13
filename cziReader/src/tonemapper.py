import numpy as np
import czifile
import cv2
import sys
import os


def combineChannels(dic, width, height):
    out = np.zeros([width, height, 3])
    if dic.get('r') is not None:
        out[:, :, 2] = dic.get('r')
    if dic.get('g') is not None:
        out[:, :, 1] = dic.get('g')
    if dic.get('b') is not None:
        out[:, :, 0] = dic.get('b')
    return out

def tonemapRGB(imgs):
    N = 250
    nfiles = len(imgs)
    mergedImg = np.zeros([N * 4, N * nfiles, 3])
    i = 0
    for name in imgs:
        col = imgs[name]
        img_names = ['rb', 'gb', 'rg', 'rgb']
        j = 0
        for img_name in img_names:
            if img_name == 'rb':
                img = np.zeros(col.shape)
                img[:, :, 0] = col[:, :, 0]
                img[:, :, 2] = col[:, :, 2]
            if img_name == 'gb':
                img = np.zeros(col.shape)
                img[:, :, 0] = col[:, :, 0]
                img[:, :, 1] = col[:, :, 1]
            if img_name == 'rg':
                img = np.zeros(col.shape)
                img[:, :, 1] = col[:, :, 1]
                img[:, :, 2] = col[:, :, 2]
            if img_name == 'rgb':
                img = np.zeros(col.shape)
                img[:, :, 0] = col[:, :, 0]
                img[:, :, 1] = col[:, :, 1]
                img[:, :, 2] = col[:, :, 2]
            img = cv2.resize(img / 255.0, (N, N))
            mergedImg[j * N:(j + 1) * N, i * N:(i + 1) * N, :] = img
            j += 1
        i += 1

    windowName = 'rbb czi editor'
    barName = 'TarckBar'
    cv2.namedWindow(windowName, 0)
    cv2.namedWindow(barName, cv2.WINDOW_AUTOSIZE)

    origin_b = mergedImg[:, :, 0]
    origin_g = mergedImg[:, :, 1]
    origin_r = mergedImg[:, :, 2]

    def nothing(x):
        pass

    cv2.createTrackbar('R.min', barName, 0, 255, nothing)
    cv2.createTrackbar('R.max', barName, 255, 255, nothing)
    cv2.createTrackbar('G.min', barName, 0, 255, nothing)
    cv2.createTrackbar('G.max', barName, 255, 255, nothing)
    cv2.createTrackbar('B.min', barName, 0, 255, nothing)
    cv2.createTrackbar('B.max', barName, 255, 255, nothing)

    tuned_img = np.zeros(mergedImg.shape)

    while(1):
        k = cv2.waitKey(10)

        if k == 27:
            return

        r_min = cv2.getTrackbarPos('R.min', barName)
        r_max = cv2.getTrackbarPos('R.max', barName)
        g_min = cv2.getTrackbarPos('G.min', barName)
        g_max = cv2.getTrackbarPos('G.max', barName)
        b_min = cv2.getTrackbarPos('B.min', barName)
        b_max = cv2.getTrackbarPos('B.max', barName)

        r_range = max(r_max - r_min, 1)
        g_range = max(g_max - g_min, 1)
        b_range = max(b_max - b_min, 1)

        tuned_img = np.array(mergedImg)

        tuned_img[:, :, 0] = np.clip(255 / b_range * np.clip((origin_b - b_min / 255), 0, 1.0), 0, 1.0)
        tuned_img[:, :, 1] = np.clip(255 / g_range * np.clip((origin_g - g_min / 255), 0, 1.0), 0, 1.0)
        tuned_img[:, :, 2] = np.clip(255 / r_range * np.clip((origin_r - r_min / 255), 0, 1.0), 0, 1.0)
        cv2.imshow(windowName, tuned_img)

        if k == 13:
            print('tunning imgs')
            for name in imgs:
                print('saving image {}'.format(name))
                col = imgs[name]
                img_names = ['rb', 'gb', 'rg', 'rgb', 'r', 'g', 'b']
                for img_name in img_names:
                    if img_name == 'rb':
                        img = np.zeros(col.shape)
                        img[:, :, 0] = col[:, :, 0]
                        img[:, :, 2] = col[:, :, 2]
                    if img_name == 'gb':
                        img = np.zeros(col.shape)
                        img[:, :, 0] = col[:, :, 0]
                        img[:, :, 1] = col[:, :, 1]
                    if img_name == 'rg':
                        img = np.zeros(col.shape)
                        img[:, :, 1] = col[:, :, 1]
                        img[:, :, 2] = col[:, :, 2]
                    if img_name == 'rgb':
                        img = np.zeros(col.shape)
                        img[:, :, 0] = col[:, :, 0]
                        img[:, :, 1] = col[:, :, 1]
                        img[:, :, 2] = col[:, :, 2]
                    if img_name == 'r':
                        img = np.zeros(col.shape)
                        img[:, :, 2] = col[:, :, 2]
                    if img_name == 'g':
                        img = np.zeros(col.shape)
                        img[:, :, 1] = col[:, :, 1]
                    if img_name == 'b':
                        img = np.zeros(col.shape)
                        img[:, :, 0] = col[:, :, 0]
                    img[:, :, 0] = np.clip(255 / b_range * np.clip((img[:, :, 0] / 255.0 - b_min / 255), 0, 1.0), 0, 1.0)
                    img[:, :, 1] = np.clip(255 / g_range * np.clip((img[:, :, 1] / 255.0 - g_min / 255), 0, 1.0), 0, 1.0)
                    img[:, :, 2] = np.clip(255 / r_range * np.clip((img[:, :, 2] / 255.0 - r_min / 255), 0, 1.0), 0, 1.0)
                    img = img * 255.0
                    outRoot = os.path.join(root, name)
                    imgPath = os.path.join(outRoot, '{}_{}.jpg'.format(name, img_name))
                    cv2.imwrite(imgPath, img)
                    print('@{}\t channel'.format(img_name))
            print('tuned img written')

    cv2.destroyAllWindows()

if __name__ == '__main__':
    f = open('input.txt')
    lines = f.readlines()
    f.close()
    nfiles = len(lines)
    root = '../tuned'

    imgs = {}
    for i in range(nfiles):
        in_file = lines[i].strip()
        name = in_file.split('.czi')[0]
        name = name.replace(' ', '_')
        outRoot = os.path.join(root, name)
        channelsPath = os.path.join(outRoot, '{}_channels.jpg'.format(name))
        originImg = cv2.imread(channelsPath)
        imgs[name] = originImg

    tonemapRGB(imgs)
