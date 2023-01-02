# Copyright (c) 2022, Pavel Mokeev, Dmitrii Iarosh, Anastasiia Kornilova
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
import numpy as np
import pytest

from evops.metrics import mean, iou
from fixtures import clean_env


def test_mean_simple_array(clean_env):
    pred_labels = np.array([1, 1, 1])
    gt_labels = np.array([1, 1, 1])

    metric = iou
    tp_condition = "iou"

    assert 1.0 == pytest.approx(mean(pred_labels, gt_labels, metric, tp_condition))


def test_mean_part_result(clean_env):
    pred_labels = np.array([1, 2, 1, 1, 1])
    gt_labels = np.array([1, 1, 1, 1, 1])

    metric = iou
    tp_condition = "iou"

    assert 0.8 == pytest.approx(mean(pred_labels, gt_labels, metric, tp_condition))


def test_mean_half_result(clean_env):
    pred_labels = np.array([1, 2, 1, 2])
    gt_labels = np.array([1, 1, 1, 1])

    metric = iou
    tp_condition = "iou"

    assert 0.0 == pytest.approx(mean(pred_labels, gt_labels, metric, tp_condition))


def test_mean_null_result(clean_env):
    pred_labels = np.array([0, 0, 0, 0])
    gt_labels = np.array([1, 1, 1, 1])

    metric = iou
    tp_condition = "iou"

    assert 0 == pytest.approx(mean(pred_labels, gt_labels, metric, tp_condition))


def test_mean_pred_labels_assert(clean_env):
    with pytest.raises(AssertionError) as excinfo:
        pred_labels = np.ones((3, 3, 3))
        gt_labels = np.array([1])

        metric = iou
        tp_condition = "iou"
        mean(pred_labels, gt_labels, metric, tp_condition)

    assert str(excinfo.value) == "Incorrect predicted label array size, expected (n)"


def test_mean_gt_labels_assert(clean_env):
    with pytest.raises(AssertionError) as excinfo:
        pred_labels = np.array([1])
        gt_labels = np.ones((3, 3, 3))

        metric = iou
        tp_condition = "iou"
        mean(pred_labels, gt_labels, metric, tp_condition)

    assert str(excinfo.value) == "Incorrect ground truth label array size, expected (n)"


def test_mean_iou_real_data(clean_env):
    pred_labels = np.load("tests/data/pred_0.npy")
    gt_labels = np.load("tests/data/gt_0.npy")

    metric = iou
    tp_condition = "iou"

    assert 0.99 == pytest.approx(
        mean(pred_labels, gt_labels, metric, tp_condition), 0.01
    )
