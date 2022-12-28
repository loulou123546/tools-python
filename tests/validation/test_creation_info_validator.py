#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import datetime
from typing import List

import pytest

from src.model.document import CreationInfo
from src.model.version import Version
from src.validation.creation_info_validator import validate_creation_info
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor, get_external_document_ref, get_creation_info


def test_valid_creation_info():
    creation_info = CreationInfo("SPDX-2.3", "SPDXRef-DOCUMENT", "document name", "https://some.uri",
                                 [get_actor(), get_actor()], datetime(2022, 1, 1), "creator_comment",
                                 "CC0-1.0", [get_external_document_ref(), get_external_document_ref()], Version(6, 3),
                                 "doc_comment")
    validation_messages: List[ValidationMessage] = validate_creation_info(creation_info)

    assert validation_messages == []


@pytest.mark.parametrize \
        ("creation_info_input, spdx_id, expected_message",
         [(get_creation_info(spdx_version="version-2.3"), "SPDXRef-DOCUMENT",
           'spdx_version must be of the form "SPDX-[major].[minor]" but is: version-2.3'),
          (get_creation_info(spdx_id="SPDXRef-doc"), "SPDXRef-doc",
           'spdx_id must be "SPDXRef-DOCUMENT", but is: SPDXRef-doc'),
          (get_creation_info(data_license="MIT"), "SPDXRef-DOCUMENT",
           'data_license must be "CC0-1.0", but is: MIT'),
          (get_creation_info(document_namespace="some_namespace"), "SPDXRef-DOCUMENT",
           "document_namespace must be a valid URI specified in RFC-3986, but is: some_namespace"),
          ])
def test_invalid_creation_info(creation_info_input, expected_message, spdx_id):
    validation_messages: List[ValidationMessage] = validate_creation_info(creation_info_input)

    expected = ValidationMessage(expected_message, ValidationContext(spdx_id, None, SpdxElementType.DOCUMENT))

    assert validation_messages == [expected]