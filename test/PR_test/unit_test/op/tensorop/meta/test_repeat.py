import unittest

import tensorflow as tf

from fastestimator.op.tensorop.meta import Repeat
from fastestimator.op.tensorop import LambdaOp


class TestRepeat(unittest.TestCase):
    def test_single_repeat_int_tf(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=1)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(2, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(1, output[1])

    def test_multi_repeat_int_tf(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=5)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(6, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(25, output[1])

    def test_single_repeat_fn_interior_value_tf(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y: y < 1)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(2, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(1, output[1])

    def test_multi_repeat_fn_interior_value_tf(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y: y < 25)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(6, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(25, output[1])

    def test_repeat_fn_exterior_value_tf(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y, z: y + z < 25)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x', 'z'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1]), 10 + tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(5, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(16, output[1])

    def test_single_repeat_int_static(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda y: (y + 1, y * y), mode='eval')
        repeat_op = Repeat(add_op, repeat=1)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        x = [tf.ones([1])]
        output = tf.function(lambda y: repeat_op.forward(data=y, state={"mode": "eval"}))
        output(x)  # build the graph
        output = output(x)
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(2, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(1, output[1])

    def test_multi_repeat_int_static(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda z: (z + 1, z * z), mode='eval')
        repeat_op = Repeat(add_op, repeat=5)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        x = [tf.ones([1])]
        output = tf.function(lambda y: repeat_op.forward(data=y, state={"mode": "eval"}))
        output(x)  # build the graph
        output = output(x)
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(6, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(25, output[1])

    def test_single_repeat_fn_interior_value_static(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda z: (z + 1, z * z), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y: y < 1)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        x = [tf.ones([1])]
        output = tf.function(lambda y: repeat_op.forward(data=y, state={"mode": "eval"}))
        output(x)  # build the graph
        output = output(x)
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(2, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(1, output[1])

    def test_multi_repeat_fn_interior_value_static(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda z: (z + 1, z * z), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y: y < 25)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        x = [tf.ones([1])]
        output = tf.function(lambda y: repeat_op.forward(data=y, state={"mode": "eval"}))
        output(x)
        output = output(x)
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(6, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(25, output[1])

    def test_repeat_fn_exterior_value_static(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda w: (w + 1, w * w), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y, z: y + z < 25)
        repeat_op.build('tf')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x', 'z'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        x = [tf.ones([1]), 10 + tf.ones([1])]
        output = tf.function(lambda y: repeat_op.forward(data=y, state={"mode": "eval"}))
        output(x)
        output = output(x)
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(5, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(16, output[1])

    def test_single_repeat_int_torch(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=1)
        repeat_op.build('torch')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(2, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(1, output[1])

    def test_multi_repeat_int_torch(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=5)
        repeat_op.build('torch')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(6, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(25, output[1])

    def test_single_repeat_fn_interior_value_torch(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y: y < 1)
        repeat_op.build('torch')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(2, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(1, output[1])

    def test_multi_repeat_fn_interior_value_torch(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y: y < 25)
        repeat_op.build('torch')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(6, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(25, output[1])

    def test_repeat_fn_exterior_value_torch(self):
        add_op = LambdaOp(inputs='x', outputs=('x', 'y'), fn=lambda x: (x + 1, x * x), mode='eval')
        repeat_op = Repeat(add_op, repeat=lambda y, z: y + z < 25)
        repeat_op.build('torch')
        with self.subTest('Check op inputs'):
            self.assertListEqual(repeat_op.inputs, ['x', 'z'])
        with self.subTest('Check op outputs'):
            self.assertListEqual(repeat_op.outputs, ['x', 'y'])
        with self.subTest('Check op mode'):
            self.assertSetEqual(repeat_op.mode, {'eval'})
        output = repeat_op.forward(data=[tf.ones([1]), 10 + tf.ones([1])], state={"mode": "eval"})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output value (x)'):
            self.assertEqual(5, output[0])
        with self.subTest('Check output value (y)'):
            self.assertEqual(16, output[1])
