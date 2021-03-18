"""Test module for the AdapNet++ network.

This module provides a full testing function for tensorflow 1 models, given
a configuration file and data.
"""

import argparse
import datetime
import importlib
import os
import cv2
import yaml
import numpy as np
import tensorflow as tf
from dataset.helper import get_test_data, compute_output_matrix, compute_iou


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.sys.path.append('models')
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-c', '--config',
                    nargs='?',
                    default='config/forest_test.config',
                    help='Path to the network config file.')
PARSER.add_argument('-d', '--directory',
                    nargs='?',
                    default='',
                    help='Path to which the predictions should be saved.')


def test_func(config, directory):
    """Evaluate the AdapNet network with given test files.

    Args:
        config (dict): Config dictionnary parsed from a config file.
        directory (str): Output directory path where to save the predicted
                         segmentation images.
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = config['gpu_id']
    module = importlib.import_module('models.' + config['model'])
    model_func = getattr(module, config['model'])
    data_list, iterator = get_test_data(config)
    resnet_name = 'resnet_v2_50'
    # tf.reset_default_graph()
    with tf.variable_scope(resnet_name):
        model = model_func(num_classes=config['num_classes'], training=False)
        images_pl = tf.placeholder(tf.float32,
                                   [None, config['height'], config['width'], 3])
        model.build_graph(images_pl)

    config1 = tf.ConfigProto()
    config1.gpu_options.allow_growth = True
    sess = tf.Session(config=config1)
    sess.run(tf.global_variables_initializer())
    import_variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
    print('total_variables_loaded:', len(import_variables))
    saver = tf.train.Saver(import_variables)
    # saver = os.path.join(os.getcwd(),config['checkpoint'])+'.meta'
    # saver = tf.train.import_meta_graph(saver)
    saver.restore(sess, config['checkpoint'])
    sess.run(iterator.initializer)
    step = 0
    total_num = 0
    output_matrix = np.zeros([config['num_classes'], 3])
    while 1:
        try:
            img, label = sess.run([data_list[0], data_list[1]])
            # img = cv2.resize(img, (640,480), interpolation=cv2.INTER_CUBIC)
            # label = cv2.resize(label, (640,480),
            #                    interpolation=cv2.INTER_CUBIC)
            feed_dict = {images_pl: img}
            probabilities = sess.run([model.softmax], feed_dict=feed_dict)
            prediction = np.argmax(probabilities[0], 3)
            gt = np.argmax(label, 3)
            # prediction[gt == 0] = 0
            mymap = ([255, 255, 255], [0, 255, 0], [0, 0, 0], [0, 0, 255],
                     [255, 0, 0], [128, 128, 128], [64, 128, 64], [192, 0, 128],
                     [0, 128, 192], [0, 128, 64], [64, 0, 128], [64, 0, 192],
                     [192, 128, 64], [192, 192, 128], [64, 64, 128],
                     [128, 0, 192], [192, 0, 64], [128, 128, 64], [192, 0, 192],
                     [128, 64, 64], [64, 192, 128], [64, 64, 0], [128, 64, 128],
                     [128, 128, 192], [0, 0, 192], [192, 128, 128],
                     [64, 128, 192], [0, 0, 64], [0, 64, 64], [192, 64, 128],
                     [128, 128, 0], [192, 128, 192], [64, 0, 64], [192, 192, 0],
                     [64, 192, 0], [0, 192, 64], [0, 192, 192], [64, 0, 0])
            # mymap = mymap[:int(config['num_classes'])]
            for b in range(int(config['batch_size'])):
                pixel = np.array([0, 0, 0], np.uint8)
                w = np.array([pixel] * int(config['width']), np.uint8)
                newImg = np.array([w] * int(config['height']), np.uint8)
                for h in range(int(config['height'])):
                    for w in range(int(config['width'])):
                        newImg[h, w] = mymap[prediction[b, h, w]]
                newImg = cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)
                cv2.imshow(str(b + 1), newImg)
                if bool(directory):
                    cv2.imwrite(directory + str(b + 21) + '.png', newImg)
                cv2.waitKey(0)

            output_matrix = compute_output_matrix(gt, prediction, output_matrix)
            total_num += label.shape[0]
            if (step + 1) % config['skip_step'] == 0:
                print('%s %s] %d. iou updating'
                      % (str(datetime.datetime.now()),
                         str(os.getpid()), total_num))
                print('mIoU: ', compute_iou(output_matrix))

            step += 1

        except tf.errors.OutOfRangeError:
            print('mIoU: ', compute_iou(output_matrix),
                  'total_data: ', total_num)
            break


def main():
    """Run main function and handle arguments."""
    args = PARSER.parse_args()
    if args.config:
        file_address = open(args.config)
        config = yaml.load(file_address)
    else:
        print('--config config_file_address missing')
    test_func(config, args.directory)


if __name__ == '__main__':
    main()
