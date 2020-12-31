# Copyright © 2020, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The DELTA (Deep Earth Learning, Tools, and Analysis) platform is
# licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#pylint:disable=redefined-outer-name
"""
Test for worldview class.
"""
import tensorflow as tf

import delta.config.extensions as ext

def test_efficientnet():
    l = ext.layer('EfficientNet')
    n = l((None, None, 8))
    assert len(n.layers) == 334
    assert n.layers[0].input_shape == [(None, None, None, 8)]
    out_shape = n.compute_output_shape((None, 512, 512, 8)).as_list()
    assert out_shape == [None, 16, 16, 352]

def test_gaussian_sample():
    l = ext.layer('GaussianSample')
    n = l()
    assert n.get_config()['kl_loss']
    result = n((tf.zeros((1, 3, 3, 3)), tf.ones((1, 3, 3, 3))))
    assert result.shape == (1, 3, 3, 3)
    assert isinstance(n.callback(), tf.keras.callbacks.Callback)

def test_ms_ssim():
    l = ext.loss('ms_ssim')
    assert l(tf.zeros((1, 180, 180, 1)), tf.zeros((1, 180, 180, 1))) == 0.0
    l = ext.loss('ms_ssim_mse')
    assert l(tf.zeros((1, 180, 180, 1)), tf.zeros((1, 180, 180, 1))) == 0.0

def test_mapped():
    mcce = ext.loss('MappedCategoricalCrossentropy')
    z = tf.zeros((3, 3, 3, 3), dtype=tf.int32)
    o = tf.ones((3, 3, 3, 3), dtype=tf.float32)
    assert tf.reduce_sum(mcce([0, 0]).call(z, o)) == 0.0
    assert tf.reduce_sum(mcce([1, 0]).call(z, o)) > 10.0

def test_sparse_recall():
    m0 = ext.metric('SparseRecall')(0)
    m1 = ext.metric('SparseRecall')(1)
    z = tf.zeros((3, 3, 3, 3), dtype=tf.int32)
    o = tf.ones((3, 3, 3, 3), dtype=tf.int32)

    m0.reset_state()
    m1.reset_state()
    m0.update_state(z, z)
    m1.update_state(z, z)
    assert m0.result() == 1.0
    assert m1.result() == 0.0

    m0.reset_state()
    m1.reset_state()
    m0.update_state(o, z)
    m1.update_state(o, z)
    assert m0.result() == 0.0
    assert m1.result() == 0.0