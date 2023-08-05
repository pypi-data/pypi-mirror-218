from __future__ import annotations
import numpy as np
from geometry import Transformation, PX, PY, PZ
from flightanalysis.state import State
from flightanalysis.base.table import Time
from .element import Element
from .loop import Loop
from flightanalysis.schedule.scoring import *



class NoseDrop(Element):
    """A nose drop is used for spin entries. It consists of a loop to a vertical downline, with an integrated
    pitch rotation in the opposite direction to the loops pitch rotation so that the body axis finishes at
    break_angle off the vertical line"""
    parameters = Element.parameters + "radius,break_angle".split(",")
    def __init__(self, speed: float, radius: float, break_angle: float, uid: str=None):
        super().__init__(uid, speed)
        self.radius=radius
        self.break_angle = break_angle

    def to_dict(self):
        return dict(
            kind=self.__class__.__name__,
            speed=self.speed,
            radius=self.radius,
            break_angle=self.break_angle,
            uid=self.uid
        )

    def create_template(self, istate: State, time: Time=None) -> State:
        _inverted = 1 if istate.transform.rotation.is_inverted()[0] else -1
        
        alpha =  np.arctan2(istate.vel.z, istate.vel.x)[0]

        return Loop(self.speed, self.radius, 0.5*np.pi*_inverted).create_template(
            istate, time
        ).superimpose_rotation(
            PY(), 
            -alpha - abs(self.break_angle) * _inverted
        ).label(element=self.uid)
    
    def describe(self):
        return "nose drop"

    def match_intention(self, transform: Transformation, flown: State) -> NoseDrop:
        _inverted = 1 if transform.rotation.is_inverted()[0] else -1
        _speed = abs(flown.vel).mean()

        loop = Loop(_speed, self.radius, 0.5*np.pi*_inverted).match_intention(
            transform, flown
        )

        alpha = np.arctan2(flown.vel.z, flown.vel.x)[-1]

        return self.set_parms(
            speed = _speed,
            radius = loop.radius,
            break_angle = abs(alpha)
        )

    def copy_direction(self, other: NoseDrop) -> NoseDrop:
        return self.set_parms(break_angle=abs(self.break_angle) * np.sign(other.break_angle))

    @property
    def intra_scoring(self) -> DownGrades:
        return DownGrades()

    @property
    def exit_scoring(self) -> DownGrades:
        return DownGrades()
