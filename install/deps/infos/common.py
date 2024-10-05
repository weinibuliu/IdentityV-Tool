from random import randint

from maa.context import Context
from maa.custom_action import CustomAction

class Move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        def move(direction:int=0,duration:int=10000):
            match direction:
                case 0: #向前移动
                    context.override_pipeline({"基础移动":{"end": [175,415,10,10], "duration": duration}})
                case 1: #向右移动
                    context.override_pipeline({"基础移动":{"end": [275,515,10,10], "duration": duration}})
                case 2: #向后移动
                    context.override_pipeline({"基础移动":{"end": [175,615,10,10], "duration": duration}})
                case 3: #向左移动
                    context.override_pipeline({"基础移动":{"end": [75,515,10,10], "duration": duration}})
                case _:
                    raise (f"Class Error:{__class__.__name__},please contact to the developers.")
            context.run_pipeline("基础移动")

        direction = randint(0,3)   
        move(direction,10000)

        return True
    
class Vision_move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        def move(direction:int,duration:int):
            match direction:
                case 0: #向左移动视角
                    context.override_pipeline({"基础视角移动":{"end": [470,255,10,10], "duration": duration}})
                case 1 : #向右移动视角
                    context.override_pipeline({"基础视角移动":{"end": [870,255,10,10], "duration": duration}})
                case _:
                    raise (f"Class Error:{__class__.__name__},please contact to the developers.")
            context.run_pipeline("基础视角移动")

        direction = randint(0,1)
        move(direction,3000)
        
        return True