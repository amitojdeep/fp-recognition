import matplotlib.pyplot as plt
from PIL import Image

img_path = "jpeg_rand/"
output = "plots/"
xytTest = '1_5.jpg.xyt'
xytId = '14_1.jpg.xyt'
xytPreVer = 'comp2Ver14_1_5.xyt'
imgTest = '1_5.jpg'
imgId = '14_1.jpg'



def readMinutiae(xyt_file):
    """reads x_y.jpg.xyt
    returns list of 5 element lists (x,y,theta, quality, matches = 1)"""
    with open(output + xyt_file) as fp1:
        fl = fp1.readlines()
        f = []
        for l in fl:
            l1 = l.split()
            l2 = []
            for num in l1:
                l2.append(int(num))
            #l2.append(1) # number of times a minutiae is found
            f.append(l2)
    return f

def twinPlot(xyt_file1 = xytTest, xyt_file2  = xytPreVer, img_file = imgTest):
    plt.clf()
    img = Image.open(img_path + img_file).transpose(Image.FLIP_TOP_BOTTOM)
    img.save("temp.jpg")
    im = plt.imread("temp.jpg")
    implot = plt.imshow(im, cmap='gray')
    # fig = plt.figure()

    t = readMinutiae(xyt_file1)
    x = []
    y = []
    for m in t:
        x.append(m[0])
        y.append(m[1])

    t1 = readMinutiae(xyt_file2)
    x1 = []
    y1 = []
    for m1 in t1:
        x1.append(m1[0])
        y1.append(m1[1])

    plt.axis('off')
    plt.scatter(x, y, facecolors='none', edgecolors='r', s=20)
    plt.scatter(x1, y1, color='y', s=10)
    plt.savefig("temp.jpg", bbox_inches='tight')

    ig = Image.open("temp.jpg").transpose(Image.FLIP_TOP_BOTTOM)
    #ig.save("tempPreverified.jpg")
    return ig

def singlePlot(xyt_file, img_file, test):
    #1 if plotting test, 0 for plotting id
    plt.clf()
    img = Image.open(img_path + img_file).transpose(Image.FLIP_TOP_BOTTOM)
    img.save("temp.jpg")
    im = plt.imread("temp.jpg")
    implot = plt.imshow(im, cmap='gray')
    # fig = plt.figure()

    t = readMinutiae(xyt_file)
    x = []
    y = []
    for m in t:
        x.append(m[0])
        y.append(m[1])



    plt.axis('off')
    plt.scatter(x, y, facecolors='none', edgecolors='r', s=20)
    plt.savefig("temp.jpg", bbox_inches='tight')
    ig = Image.open("temp.jpg").transpose(Image.FLIP_TOP_BOTTOM)
    #ig.save("temp" + str(test) + ".jpg")
    return ig



def combineImgs():
    img3 = singlePlot(xytTest, imgTest, 1)
    img1 = singlePlot(xytId, imgId, 0)
    img2 = twinPlot()
    images = [img1, img2 , img3]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.save(output + 'impostorFinal.jpg')

combineImgs()