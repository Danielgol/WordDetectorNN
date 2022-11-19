
import os
import argparse

import torch
from path import Path

from dataloader import DataLoaderImgFile
from eval import evaluate
from net import WordDetectorNet
from visualization import visualize_and_plot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cuda')
    args = parser.parse_args()

    net = WordDetectorNet()
    net.load_state_dict(torch.load('../model/weights', map_location=args.device))
    net.eval()
    net.to(args.device)

    loader = DataLoaderImgFile(Path('../data/test'), net.input_size, args.device)
    res = evaluate(net, loader, max_aabbs=1000)

    for i, (img, aabbs) in enumerate(zip(res.batch_imgs, res.batch_aabbs)):
        f = loader.get_scale_factor(i)
        aabbs = [aabb.scale(1 / f, 1 / f) for aabb in aabbs]
        img = loader.get_original_img(i)

        name = loader.fn_imgs[i].split("/")[-1].split(".")[0]

        if not os.path.exists("pred_labels"):
            print("pred_labels created!")
            os.makedirs("pred_labels")

        file = "pred_labels/"+name+".txt"
        open(file, 'w+')

        print(file)

        for aabb in aabbs:
            with open(file, "a+") as f:
                f.write(str(int(aabb.xmin))+" "+str(int(aabb.xmax))+" "+str(int(aabb.ymin))+" "+str(int(aabb.ymax))+"\n")
                f.close()

        #visualize_and_plot(img, aabbs)


if __name__ == '__main__':
    main()
