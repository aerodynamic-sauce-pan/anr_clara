"""Module for training tensorflow models.

This module contains tool methods to help train tensorflow models easily.
Namely, it contains methods to fetch train/test data & data batches, and to
compute metrics such as IoU.
"""

import numpy as np
import tensorflow as tf


def get_train_batch(config):
    """Return and training iterator.

    Returns an iterator on the training batches.

    Args:
        config (dict): Dictionary containing the model's configuration
                       arguments.

    Returns:
        (Iterator): Iterator on the training batches
    """
    filenames = [config['train_data']]
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(lambda x: parser(x, config['num_classes']))
    dataset = dataset.shuffle(buffer_size=100)
    dataset = dataset.batch(config['batch_size'])
    dataset = dataset.repeat(100)
    dataset = dataset.prefetch(1)
    iterator = dataset.make_one_shot_iterator()
    return iterator


def get_test_batch(config):
    """Return and testing iterator.

    Returns an iterator on the testing batches.

    Args:
        config (dict): Dictionary containing the model's configuration
                       arguments.

    Returns:
        (Iterator): Iterator on the testing batches
    """
    filenames = [config['test_data']]
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(lambda x: parser(x, config['num_classes']))
    dataset = dataset.batch(config['batch_size'])
    iterator = dataset.make_initializable_iterator()
    return iterator


def get_train_data(config):
    """Return and training iterator and the next elements.

    Returns both an iterator on the training batches and the next elements (data
    and labels) to load.

    Args:
        config (dict): Dictionary containing the model's configuration
                       arguments.

    Returns:
        (tuple): Tuple composed of an iterator on the training batches and the
                 next training data and label.
    """
    iterator = get_train_batch(config)
    dataA, label = iterator.get_next()
    return [dataA, label], iterator


def get_test_data(config):
    """Return and testing iterator and the next elements.

    Returns both an iterator on the testing batches and the next elements (data
    and labels) to load.

    Args:
        config (dict): Dictionary containing the model's configuration
                       arguments.

    Returns:
        (tuple): Tuple composed of an iterator on the testing batches and the
                 next testing data and label.
    """
    iterator = get_test_batch(config)
    dataA, label = iterator.get_next()
    return [dataA, label], iterator


def compute_output_matrix(label_max, pred_max, output_matrix):
    """Compute the rates output matrix.

    The output matrix is a numpy 2D-array of shape [number of classes]x[3]
    (true positive rate, false positive rate, false negative rate). Its
    purpose is to provide metrics on the different segmentation classes.

    Args:
        label_max (ndarray): Labels array, np.argmax(one_hot_encoded_label, 3)
                             of shape (B,H,W).
        pred_max (ndarray): Predictions array, np.argmax(softmax, 3) of shape
                            (B,H,W).
        output_matrix (ndarray): Rates matrix of shape (nb_classes, 3).
                                 If the function is called for the first time,
                                 output_matrix is an array of zeros.

    Returns:
        output_matrix (ndarray): Rates matrix of shape (nb_classes, 3) updated
                                 with TP, FP & FN rates.
    """
    for i in range(output_matrix.shape[0]):
        temp = pred_max == i
        temp_l = label_max == i
        tp = np.logical_and(temp, temp_l)
        temp[temp_l] = True  # Taking advantage of numpy arrays
        fp = np.logical_xor(temp, temp_l)
        temp = pred_max == i
        temp[fp] = False
        fn = np.logical_xor(temp, temp_l)
        output_matrix[i, 0] += np.sum(tp)
        output_matrix[i, 1] += np.sum(fp)
        output_matrix[i, 2] += np.sum(fn)
    return output_matrix


def compute_iou(output_matrix):
    """Compute the Intersection over Union metric on the rates matrix.

    Args:
        output_matrix (ndarray): Rates matrix of shape (nb_classes, 3)
                                 containing TP, FP & FN rates.

    Returns:
        (ndarray): IoU in percentages (doesn't count label id 0 contribution
                   as it is assumed to be void).
    """
    tp_ = output_matrix[1:, 0]
    tp_fp_fn = (np.sum(output_matrix[1:, :], 1).astype(np.float32)+1e-10)
    return np.sum(tp_/tp_fp_fn)/(output_matrix.shape[0]-1)*100


def parser(proto_data, num_classes):
    """Parse a dataset loaded from a TFRecord file.

    Args:
        proto_data (TFRecordDataset): Input dataset loaded from a TFRecord file
                                      as TFRecordDataset.
        num_classes (int): Number of classes in the dataset.

    Returns:
        (tuple): Modalities (RGB images) and labels returns respectively as
                 float32 and int32.
    """
    features = {'height': tf.FixedLenFeature((), tf.int64, default_value=0),
                'width': tf.FixedLenFeature((), tf.int64, default_value=0),
                'modality': tf.FixedLenFeature((), tf.string, default_value=""),
                'label': tf.FixedLenFeature((), tf.string, default_value="")
                }
    parsed_features = tf.parse_single_example(proto_data, features)
    modality = tf.decode_raw(parsed_features['modality'], tf.uint8)
    label = tf.decode_raw(parsed_features['label'], tf.uint8)

    height = tf.cast(parsed_features['height'], tf.int32)
    width = tf.cast(parsed_features['width'], tf.int32)
    label = tf.reshape(label, [height, width, 1])
    label = tf.one_hot(label, num_classes)
    label = tf.squeeze(label, axis=2)
    modality = tf.reshape(modality, [height, width, 3])

    return tf.cast(modality, tf.float32), tf.cast(label, tf.int32)
