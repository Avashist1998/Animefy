import torch
import os
import numpy as np
import argparse
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.utils as vutils
from network.Transformer import Transformer
import time

def imageConverter(input_dir='input_img',load_size=1080,model_path='./pretrained_model',style='Hayao',output_dir='Output_img',input_file='4--24.jpg'):
    gpu = -1
    file_name = input_file
    ext = os.path.splitext(file_name)

    if not os.path.exists(output_dir): os.mkdir(output_dir)

    # load pretrained model
    model = Transformer()
    model.load_state_dict(torch.load(os.path.join(model_path, style + '_net_G_float.pth')))
    model.eval()

    #check if gpu available
    if gpu > -1:
        print('GPU mode')
        model.cuda()
    else:
        # print('CPU mode')
        model.float()
    
    # load image
    input_image = Image.open(os.path.join(input_dir, file_name)).convert("RGB")
    # resize image, keep aspect ratio
    h = input_image.size[0]
    w = input_image.size[1]
    # TODO should change this usage and make it more elegant
    ratio = h *1.0 / w 
    if w >1080 or h >1080:
        load_size = 1080
    if load_size != -1:
        if ratio > 1:
            h = int(load_size)
            w = int(h*1.0/ratio)
        else:
            w = int(load_size)
            h = int(w * ratio)
        input_image = input_image.resize((h, w), Image.BICUBIC)
    input_image = np.asarray(input_image)
    # RGB -> BGR
    input_image = input_image[:, :, [2, 1, 0]]
    input_image = transforms.ToTensor()(input_image).unsqueeze(0)
    # preprocess, (-1, 1)
    input_image = -1 + 2 * input_image 
    if gpu > -1:

        input_image = Variable(input_image, requires_grad=False).cuda()
    else:
        input_image = Variable(input_image, requires_grad=False).float()
    # forward
    output_image = model(input_image)
    output_image = output_image[0]
    # BGR -> RGB
    output_image = output_image[[2, 1, 0], :, :]
    print(output_image.shape)
    # deprocess, (0, 1)
    output_image = output_image.data.cpu().float() * 0.5 + 0.5
    # save
    final_name = file_name[:-4] + '_' + style + '.jpg'
    output_path = os.path.join(output_dir,final_name)
    vutils.save_image(output_image, output_path)
    
    return final_name

if __name__ == "__main__":
    t1 = time.time()
    print(imageConverter(style='Paprika', load_size=-1, input_file='IMG_8316.png', input_dir='static/Input_img'))
    print("The total time it took to run the program is {}".format(time.time()-t1))


# The program takes about 1 min and 35 seconds for an image of size 1080x720