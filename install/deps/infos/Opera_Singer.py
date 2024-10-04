from time import sleep
from random import randint
from maa.context import Context
from maa.custom_action import CustomAction

class o_s_move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult | bool:
        def move(direction:int=0,duration:int=10):
            match direction:
                case 0: #向前移动
                    context.override_pipeline({"歌剧演员_移动":{"end": [175,415,10,10], "duration": duration}})
                case 1: #向右移动
                    context.override_pipeline({"歌剧演员_移动":{"end": [275,515,10,10], "duration": duration}})
                case 2: #向后移动
                    context.override_pipeline({"歌剧演员_移动":{"end": [175,615,10,10], "duration": duration}})
                case 3: #向左移动
                    context.override_pipeline({"歌剧演员_移动":{"end": [75,515,10,10], "duration": duration}})
                case _:
                    raise (f"Class Error:{__class__.__name__},please contact to the developers.")
        direction = randint(0,3)
        move(direction,10)
        
        return True

class o_s_round(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        context.run_pipeline("歌剧演员_影跃")
        sleep(1)
        context.run_pipeline("歌剧演员_普攻")
        sleep(1.2)
        
        return True