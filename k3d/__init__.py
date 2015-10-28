from ipywidgets import DOMWidget
from IPython.display import display
from traitlets import Unicode, Dict, Int
from objects import Objects


class K3D(DOMWidget):
    _view_module = Unicode('nbextensions/k3d_widget/view', sync=True)
    _view_name = Unicode('K3DView', sync=True)
    _model_module = Unicode('nbextensions/k3d_widget/model', sync=True)
    _model_name = Unicode('K3DModel', sync=True)

    height = Int(sync=True)
    object = Dict(sync=True)

    def __init__(self, height = 512):
        super(K3D, self).__init__()

        self.__objects = Objects(self.__show)
        self.height = height
        self.on_displayed(lambda x: self.__objects.flush())

    def __add__(self, obj):
        self.__objects.add(obj)
        return self

    def display(self):
        display(self)

    def __show(self, obj):
        self.object = obj

    @staticmethod
    def torus_knot(position):
        return {
            "type": "TorusKnot",
            "modelViewMatrix": [
                1.0, 0.0, 0.0, position,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
            ],
            "color": 0xff00ff,
            "knotsNumber": 16,
            "radius": 7,
            "tube": 2
        }
