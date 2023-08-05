#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import pytest

from sts import loopdev


def test_loopdev():  # noqa: ANN201
    dev = loopdev.create_loopdev()
    if not dev:
        print("SKIP: Could not create loop device")
        return

    if not loopdev.delete_loopdev(dev):
        pytest.fail("FAIL: Could not delete loop device")

    assert 1
