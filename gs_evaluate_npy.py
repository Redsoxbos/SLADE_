import numpy as np
import os
import cv2
import argparse
from PIL import Image
from torchvision import transforms

def compute_errors(gt, pred):
    """Computation of error metrics between predicted and ground truth depths
    """
    thresh = np.maximum((gt / pred), (pred / gt))
    a1 = (thresh < 1.25     ).mean()
    a2 = (thresh < 1.25 ** 2).mean()
    a3 = (thresh < 1.25 ** 3).mean()

    rmse = (gt - pred) ** 2
    rmse = np.sqrt(rmse.mean())

    rmse_log = (np.log(gt) - np.log(pred)) ** 2
    rmse_log = np.sqrt(rmse_log.mean())

    abs_rel = np.mean(np.abs(gt - pred) / gt)

    sq_rel = np.mean(((gt - pred) ** 2) / gt)

    return abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3

def Average(lst):
    return sum(lst) / len(lst)

def main(config):
    gt = config.gt
    pred = config.pred
    arg_min = config.min
    arg_max = config.max

    
    metric={}
    abs_rel_list= []
    sq_rel_list= []
    rmse_list= []
    rmse_log_list= []
    a1_list= []
    a2_list= []
    a3_list= []
    pred_list = sorted(os.listdir(pred))
    gt_list = sorted(os.listdir(gt))
    
    print(arg_max)
    for i in range(len(gt_list)):
        

        pred_depth = np.load(pred + gt_list[i][:-4] + "_raw.npy")*4.1339

        gt_depth = np.load(gt + gt_list[i][:-4] + ".npy")
        #gt_depth = gt_depth[coord[1]:coord[3], coord[0]:coord[2]]
        #gt_depth = Image.fromarray(gt_depth)
        #gt_depth = resize(gt_depth)
        #gt_depth = np.array(gt_depth)
        mask = np.logical_and(gt_depth>arg_min,gt_depth<arg_max)

        gt_ma = gt_depth[mask]

        pred_ma=pred_depth[mask]
        pred_ma[pred_ma<arg_min] = arg_min
        pred_ma[pred_ma>arg_max] = arg_max

        abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3 =compute_errors(gt_ma,pred_ma)
        abs_rel_list.append(abs_rel)

        #eval_dict['RMSE'].append(RMSE_value)

        sq_rel_list.append(sq_rel)
        rmse_list.append(rmse)
        rmse_log_list.append(rmse_log)
        a1_list.append(a1)
        a2_list.append(a2)
        a3_list.append(a3)
    print(f'abs_rel: {Average(abs_rel_list)} \n sq_rel: {Average(sq_rel_list)} \n rmse: {Average(rmse_list)} \n rmse_log: {Average(rmse_log_list)} \n a1: {Average(a1_list)} \n a2: {Average(a2_list)} \n a3: {Average(a3_list)} \n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gt', type=str)
    parser.add_argument('--pred', type=str)
    parser.add_argument('--min', type=float, default=0.000001)
    parser.add_argument('--max', type=float, default=40)

    config = parser.parse_args()    
    main(config)