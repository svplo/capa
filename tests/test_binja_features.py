# Copyright (C) 2020 FireEye, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
import logging

import fixtures
from fixtures import *

logger = logging.getLogger(__file__)

# We need to skip the binja test if we cannot import binaryninja, e.g., in GitHub CI.
binja_present: bool = False
try:
    import binaryninja

    try:
        binaryninja.load(source=b"\x90")
    except RuntimeError as e:
        logger.warning("Binary Ninja license is not valid, provide via $BN_LICENSE or license.dat")
    else:
        binja_present = True
except ImportError:
    pass


@pytest.mark.skipif(binja_present is False, reason="Skip binja tests if the binaryninja Python API is not installed")
@fixtures.parametrize(
    "sample,scope,feature,expected",
    fixtures.FEATURE_PRESENCE_TESTS,
    indirect=["sample", "scope"],
)
def test_binja_features(sample, scope, feature, expected):
    fixtures.do_test_feature_presence(fixtures.get_binja_extractor, sample, scope, feature, expected)


@pytest.mark.skipif(binja_present is False, reason="Skip binja tests if the binaryninja Python API is not installed")
@fixtures.parametrize(
    "sample,scope,feature,expected",
    fixtures.FEATURE_COUNT_TESTS,
    indirect=["sample", "scope"],
)
def test_binja_feature_counts(sample, scope, feature, expected):
    fixtures.do_test_feature_count(fixtures.get_binja_extractor, sample, scope, feature, expected)
