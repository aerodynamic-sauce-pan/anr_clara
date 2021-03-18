"""Train module for the AdapNet++ network.

This module provides a full training function for tensorflow 1 models, given
a configuration file and data.
"""

import os
import re
import argparse
import datetime
import importlib

import yaml
import tensorflow as tf
from dataset.helper import get_train_data


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-c', '--config',
                    default='config/cityscapes_train.config',
                    help='Path to the network config file.')


def train_func(config):
    """Train the AdapNet model following the config parameters.

    Args:
        config (dict): Config dictionnary parsed from a config file.
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = config['gpu_id']
    module = importlib.import_module('models.'+config['model'])
    model_func = getattr(module, config['model'])
    data_list, _ = get_train_data(config)
    global_step = tf.Variable(0, trainable=False, name='Global_Step')

    with tf.variable_scope('resnet_v2_50'):
        model = model_func(num_classes=config['num_classes'],
                           learning_rate=config['learning_rate'],
                           decay_steps=config['max_iteration'],
                           power=config['power'],
                           global_step=global_step)
        images_pl = tf.placeholder(tf.float32, [None, config['height'],
                                                config['width'], 3])
        labels_pl = tf.placeholder(tf.float32, [None, config['height'],
                                                config['width'],
                                                config['num_classes']])
        model.build_graph(images_pl, labels_pl)
        model.create_optimizer()

    config1 = tf.ConfigProto()
    config1.gpu_options.allow_growth = True
    sess = tf.Session(config=config1)
    sess.run(tf.global_variables_initializer())
    step = 0
    total_loss = 0.0
    t0 = None
    ckpt_path = os.path.dirname(os.path.join(config['checkpoint'],
                                             'checkpoint'))
    ckpt = tf.train.get_checkpoint_state(ckpt_path)
    if ckpt and ckpt.model_checkpoint_path:
        saver = tf.train.Saver(max_to_keep=1000)
        saver.restore(sess, ckpt.model_checkpoint_path)
        step = int(ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1])+1
        sess.run(tf.assign(global_step, step))
        print('Model Loaded')

    else:
        if 'intialize' in config:
            reader = tf.train.NewCheckpointReader(config['intialize'])
            var_str = reader.debug_string()
            name_var = re.findall('[A-Za-z0-9/:_]+ ', var_str)
            import_variables = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
            initialize_variables = {}
            for var in import_variables:
                if var.name+' ' in name_var:
                    initialize_variables[var.name] = var

            saver = tf.train.Saver(initialize_variables)
            saver.restore(save_path=config['intialize'], sess=sess)
            print('Pretrained Intialization')
        saver = tf.train.Saver(max_to_keep=1000)

    while 1:
        try:
            img, label = sess.run([data_list[0], data_list[1]])
            feed_dict = {images_pl: img, labels_pl: label}
            loss_batch, _ = sess.run([model.loss, model.train_op],
                                     feed_dict=feed_dict)

            total_loss += loss_batch

            if (step + 1) % config['save_step'] == 0:
                saver.save(sess, os.path.join(config['checkpoint'],
                                              'model.ckpt'), step)

            if (step + 1) % config['skip_step'] == 0:
                left_hours = 0

                if t0 is not None:
                    delta_t = (datetime.datetime.now() - t0).seconds
                    left_time = delta_t * (config['max_iteration'] - step)
                    left_time /= config['skip_step']
                    left_hours = left_time/3600.0

                t0 = datetime.datetime.now()
                total_loss /= config['skip_step']
                print('%s %s] Step %s, lr = %f '
                      % (str(datetime.datetime.now()), str(os.getpid()), step,
                         model.lr.eval(session=sess)))
                print('\t loss = %.4f' % (total_loss))
                print('\t estimated time left: %.1f hours. %d/%d'
                      % (left_hours, step, config['max_iteration']))
                print('\t', config['model'])
                total_loss = 0.0

            step += 1
            if step > config['max_iteration']:
                saver.save(sess, os.path.join(config['checkpoint'],
                                              'model.ckpt'), step-1)
                print('training_completed')
                break

        except tf.errors.OutOfRangeError:
            print('Epochs in dataset repeat < max_iteration')
            break


def main():
    """Run main function and handle arguments."""
    args = PARSER.parse_args()
    if args.config:
        file_address = open(args.config)
        config = yaml.load(file_address)
    else:
        print('--config config_file_address missing')
    train_func(config)


if __name__ == '__main__':
    main()
