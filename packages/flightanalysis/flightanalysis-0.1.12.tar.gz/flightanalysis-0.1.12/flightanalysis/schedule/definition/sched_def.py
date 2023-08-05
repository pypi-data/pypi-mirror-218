from . import ManDef, ManInfo, ManParms
from flightanalysis import State
from typing import Dict, Tuple
from geometry import Transformation
from flightanalysis.schedule.schedule import Schedule
from flightanalysis.schedule.elements import Line
from flightanalysis.base.collection import Collection
from json import dump, load
from flightanalysis.base.numpy_encoder import NumpyEncoder


class SchedDef(Collection):
    VType=ManDef
    def add_new_manoeuvre(self, info: ManInfo, defaults=None):
        return self.add(ManDef(info,defaults))

    
    def create_schedule(self, depth: float, wind: float) -> Schedule:
        return Schedule(
            {m.uid: m.create(m.info.initial_transform(depth, wind)) for m in self}
        )      
    
    def create_template(self,depth:float=170, wind:int=-1) -> Tuple[Schedule, State]:
        templates = []
        ipos = self[0].info.initial_position(depth,wind)
        
        mans = []
        for md in self:

            itrans=Transformation(
                ipos if len(templates) == 0 else templates[-1][-1].pos,
                md.info.start.initial_rotation(wind)
            )
            man = md.create(itrans)
            templates.append(man.create_template(itrans))
            mans.append(man)
        return Schedule(mans), State.stack(templates)

    def create_el_matched_template(self, intended: Schedule):
        for md, man in zip(self, intended):
            if isinstance(man, Line):
                pass

    def update_defaults(self, sched: Schedule):
        # TODO need to consider the entry line
        for md, man in zip(self, sched):
            md.mps.update_defaults(man)

    def to_json(self, file: str) -> str:
        with open(file, "w") as f:
            dump(self.to_dict(), f, cls=NumpyEncoder, indent=2)
        return file

    @staticmethod
    def from_json(file:str):
        with open(file, "r") as f:
            return SchedDef.from_dict(load(f))
        
