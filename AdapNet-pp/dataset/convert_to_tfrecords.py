"""Module for data conversion to TFRecords.

This module aims at facilitating the creation of TFRecords from text files
containing paths to data files.
"""

import cv2
import argparse
import numpy as np
import tensorflow as tf


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-f', '--file',
                    default='../config/test_synthetic.txt',
                    help='Text file to parse. This file should contain paths '
                         'to train and/or test data files following a SPV '
                         '(Space-Separated Values) format where the first '
                         'value should reference training data, and the second '
                         'value should reference testing data.')
PARSER.add_argument('-r', '--record',
                    default='../config/test_synthetic.record',
                    help='Output file. Path to the tensorflow record output'
                         'file')
PARSER.add_argument('-m', '--mean',
                    default=0)


def _int64_feature(data):
    """Encode int64-transformed data as a tensorflow feature message.

    Args:
        data (bool, enum, int32, uint32, int64, uint64): Input data

    Returns:
        (tf Feature): Tensorflow feature message
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[data]))


def _bytes_feature(data):
    """Encode bytes-transformed data as in a tensorflow feature message.

    Args:
        data (str, byte): Input data
    Returns:
        (tf Feature): Tensorflow feature message
    """
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[data]))


def decode(txt):
    """Parse an input text file into a list of lists of trings.

    Parses a SPV (space-separated values) file into a list where each line is
    an item, which is itself a list containing the SPV of the line. The values
    should be paths to images.

    Args:
        txt (file): Input text file with space separated values

    Returns:
        (list): Parsed file as a list of lists
    """
    with open(txt) as file_handler:
        all_list = file_handler.readlines()

    file_list = []
    for line in all_list:
        temp = line.strip('\n').split(' ')
        file_list.append(temp)

    return file_list


def convert(f, record_name, mean_flag):
    """Generate a serialized tf.record file.

    Creates a tf.record file from a parsed text file outputed by decode().
    Can additionaly create a binary numpy file containing the average values
    of each images referenced by the parsed text file.

    Args:
        f (list): Parsed file. f should be a list of lists of strings
        record_name (string): The path to the TFRecords file
        mean_flag (bool): Flag to indicated weither or not to create the mean
                          binary numpy file
    """
    count = 0.0
    writer = tf.compat.v1.python_io.TFRecordWriter(record_name)

    if mean_flag:
        mean = np.zeros(cv2.imread(f[0][0]).shape, np.float32)

    for name in f:
        modality = cv2.imread(name[0])
        modality = cv2.resize(modality, (640, 480),
                              interpolation=cv2.INTER_CUBIC)
        if mean_flag:
            mean += modality

        label = cv2.imread(name[1])
        label = cv2.resize(label, (640, 480), interpolation=cv2.INTER_CUBIC)
        label = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
        try:
            assert len(label.shape) == 2
        except Exception as exc:
            raise AssertionError("Label should be one channel !") from exc

        height = modality.shape[0]
        width = modality.shape[1]
        modality = modality.tostring()
        label = label.tostring()
        features = {'height': _int64_feature(height),
                    'width': _int64_feature(width),
                    'modality': _bytes_feature(modality),
                    'label': _bytes_feature(label),
                    }
        example = tf.train.Example(features=tf.train.Features(feature=features))
        writer.write(example.SerializeToString())  # Write record file

        if (count+1) % 1 == 0:
            print('Processed data: %d' % (count+1))

        count = count+1

    if mean_flag:
        mean = mean/count
        np.save(record_name.split('.')[0]+'.npy', mean)


def main():
    """Run main function and handle arguments."""
    args = PARSER.parse_args()
    if args.file:
        file_list = decode(args.file)
    else:
        print('--file file_address missing')
        return
    if args.record:
        record_name = args.record
    else:
        print('--record tfrecord name missing')
        return
    mean_flag = False
    if args.record:
        mean_flag = args.mean
    convert(file_list, record_name, mean_flag)


if __name__ == '__main__':
    main()
