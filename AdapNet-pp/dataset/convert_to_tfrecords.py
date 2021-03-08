''' AdapNet:  Adaptive  Semantic  Segmentation
              in  Adverse  Environmental  Conditions
 Copyright (C) 2018  Abhinav Valada, Johan Vertens , Ankit Dhall and Wolfram Burgard
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.'''

import argparse
import cv2
import numpy as np
import tensorflow as tf


def _int64_feature(data):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[data]))

def _bytes_feature(data):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[data]))

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-f', '--file', default = '../config/test_synthetic.txt')
PARSER.add_argument('-r', '--record', default = '../config/test_synthetic.record')
PARSER.add_argument('-m', '--mean', default = 0)

def decode(txt):
    with open(txt) as file_handler:
        all_list = file_handler.readlines()

    file_list = []
    for line in all_list:
        temp = line.strip('\n').split(' ')
        file_list.append(temp)

    return file_list

def convert(f, record_name, mean_flag):
    count = 0.0
    writer = tf.compat.v1.python_io.TFRecordWriter(record_name)

    if mean_flag:
        mean = np.zeros(cv2.imread(f[0][0]).shape, np.float32)

    for name in f:
        print(name[0])
        modality = cv2.imread(name[0])
        modality = cv2.resize(modality, (640, 480), interpolation=cv2.INTER_CUBIC)
        if mean_flag:
            mean += modality
        
        label = cv2.imread(name[1])
        label = cv2.resize(label, (640, 480), interpolation=cv2.INTER_CUBIC)
        label = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
        try:
            assert len(label.shape)==2
        except:
            raise( AssertionError( "Label should be one channel!" ) )
            
        height = modality.shape[0]
        width = modality.shape[1]
        modality = modality.tostring()
        label = label.tostring()
        features = {'height':_int64_feature(height),
                    'width':_int64_feature(width),
                    'modality':_bytes_feature(modality),
                    'label':_bytes_feature(label),
                   }
        example = tf.train.Example(features=tf.train.Features(feature=features))
        writer.write(example.SerializeToString())

        if (count+1)%1 == 0:
            print('Processed data: %d'%(count))

        count = count+1

    if mean_flag:
        mean = mean/count
        np.save(record_name.split('.')[0]+'.npy', mean)

def main():
    args = PARSER.parse_args()
    if args.file:
        file_list = decode(args.file)
    else:
        print ('--file file_address missing')
        return
    if args.record:
        record_name = args.record
    else:
        print ('--record tfrecord name missing')
        return
    mean_flag = False
    if args.record:
        mean_flag = args.mean
    convert(file_list, record_name, mean_flag)

if __name__ == '__main__':
    main()
