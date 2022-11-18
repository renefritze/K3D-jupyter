import os
from pathlib import Path

import pytest
import sys
from PIL import Image
from base64 import b64encode
from io import BytesIO
from pixelmatch.contrib.PIL import pixelmatch


def prepare():
    while len(pytest.plot.objects) > 0:
        pytest.plot -= pytest.plot.objects[-1]

    pytest.plot.clipping_planes = []
    pytest.plot.colorbar_object_id = 0
    pytest.plot.grid_visible = True
    pytest.plot.camera_mode = 'trackball'
    pytest.plot.camera = [2, -3, 0.2,
                          0.0, 0.0, 0.0,
                          0, 0, 1]
    pytest.headless.sync(hold_until_refreshed=True)
    pytest.headless.camera_reset()


def compare(name, only_canvas=True, threshold=0.2, camera_factor=1.0):
    pytest.headless.sync(hold_until_refreshed=True)

    if camera_factor is not None:
        pytest.headless.camera_reset(camera_factor)

    screenshot = pytest.headless.get_screenshot(only_canvas)

    result = Image.open(BytesIO(screenshot))
    img_diff = Image.new("RGBA", result.size)
    reference = None

    base_path = Path(__file__).resolve().absolute().parent
    references = base_path / 'references'
    png = f'{name}.png'

    if os.path.isfile(references / png):
        reference = Image.open(references / png)
    else:
        if sys.platform == 'win32':
            if os.path.isfile(references / 'win32' / png):
                reference = Image.open(references / 'win32' / png)
        else:
            if os.path.isfile(references / 'linux' / png):
                reference = Image.open(references / 'linux' / png)

    if reference is None:
        reference = Image.new("RGBA", result.size)

    mismatch = pixelmatch(result, reference, img_diff, threshold=threshold, includeAA=True)

    if mismatch >= threshold:
        results = base_path / 'results'
        with open(results / f'{name}.k3d', 'wb') as f:
            f.write(pytest.plot.get_binary_snapshot(1))
        result.save(results / f'{name}.png')
        reference.save(results / f'{name}_reference.png')
        img_diff.save(results / f'{name}_diff.png')

        print(name, mismatch, threshold)
    assert mismatch < threshold
