# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from typing import List, Optional, Union

import numpy as np
from sklearn.metrics import precision_score

from fastestimator.backend.to_number import to_number
from fastestimator.trace.trace import Trace
from fastestimator.util import Data


class Precision(Trace):
    """Computes precision for classification task and report it back to logger.

    Args:
        true_key: Name of the keys in the ground truth label in data pipeline.
        pred_key: Name of the keys in predicted label. Defaults to None.
        mode: Restrict the trace to run only on given modes {'train', 'eval', 'test'}. None will always execute.
            Defaults to 'eval'.
        output_name: Name of the key to store to the state. Defaults to "precision".
    """
    def __init__(self,
                 true_key: str,
                 pred_key: str,
                 mode: Union[str, List[str]] = ["eval", "test"],
                 output_name: str = "precision"):
        super().__init__(inputs=(true_key, pred_key), outputs=output_name, mode=mode)
        self.binary_classification = None

    @property
    def true_key(self):
        return self.inputs[0]

    @property
    def pred_key(self):
        return self.inputs[1]

    def on_epoch_begin(self, data: Data):
        self.y_true = []
        self.y_pred = []

    def on_batch_end(self, data: Data):
        groundtruth_label = to_number(data[self.true_key])
        if groundtruth_label.shape[-1] > 1 and len(groundtruth_label.shape) > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = to_number(data[self.pred_key])
        binary_classification = prediction_score.shape[-1] == 1
        if binary_classification:
            prediction_label = np.round(prediction_score)
        else:
            prediction_label = np.argmax(prediction_score, axis=-1)
        assert prediction_label.size == groundtruth_label.size
        self.binary_classification = binary_classification or prediction_score.shape[-1] == 2
        self.y_pred += list(prediction_label.ravel())
        self.y_true += list(groundtruth_label.ravel())

    def on_epoch_end(self, data: Data):
        if self.binary_classification:
            score = precision_score(np.ravel(self.y_true), np.ravel(self.y_pred), average='binary')
        else:
            score = precision_score(np.ravel(self.y_true), np.ravel(self.y_pred), average=None)
        data.write_with_log(self.outputs[0], score)
