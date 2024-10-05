from random import randint

from maa.context import Context
from maa.custom_action import CustomAction

class Move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult | bool:
        def move(direction:int=0):
            match direction:
                case 0: #向前移动
                    context.run_pipeline("移动_向前")
                case 1: #向右移动
                    context.run_pipeline("移动_向右")
                case 2: #向后移动
                    context.run_pipeline("移动_向后")
                case 3: #向左移动
                    context.run_pipeline("移动_向左")
                case _:
                    raise (f"Class Error:{__class__.__name__},please contact to the developers.")
                
        direction = randint(0,3)
        move(direction)

        return True