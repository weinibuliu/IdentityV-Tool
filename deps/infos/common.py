from time import time,sleep
from random import randint,uniform

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
                    raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")
            context.run_pipeline("基础移动")

        direction = randint(0,3)
        duration = randint(7,12)*1000 #swipe 中 duration 单位为毫秒
        move(direction,duration)

        return True
    
class Vision_Move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        def move(direction:int,duration:int):
            match direction:
                case 0: #向左移动视角
                    context.override_pipeline({"基础视角移动":{"end": [470,255,10,10], "duration": duration}})
                case 1 : #向右移动视角
                    context.override_pipeline({"基础视角移动":{"end": [870,255,10,10], "duration": duration}})
                case _:
                    raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")
            context.run_pipeline("基础视角移动")

        direction = randint(0,1)
        move(direction,1500)
        
        return True

class Hide_Mixed_Move_Jump(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        direction = randint(0,3)
        context.tasker.controller.post_touch_down(175,515,0,50).wait()

        match direction:
            case 0:
                context.tasker.controller.post_touch_move(175,315,0,50).wait()
            case 1:
                context.tasker.controller.post_touch_move(375,515,0,50).wait()
            case 2:
                context.tasker.controller.post_touch_move(175,715,0,50).wait()
            case 3:
                context.tasker.controller.post_touch_move(25,515,0,50).wait()
            case _:
                raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")

        current_time = int(time())
        duration_time = current_time + randint(7,10)

        job_statu = None
        job_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.cached_image)
        if job_statu is not None:
            job_statu = job_statu.best_result.text

        while int(time()) <= duration_time and job_statu != "继续": #循环跳跃
            click_x = randint(1125,1195)
            click_y = randint(550,660)
            context.tasker.controller.post_touch_down(click_x,click_y,1,30)
            sleep(0.2)
            context.tasker.controller.post_touch_up(contact=1)
            sleep(uniform(0.2,3))
            job_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.cached_image)
            if job_statu is not None:
                job_statu = job_statu.best_result.text

        context.tasker.controller.post_touch_up(contact=0).wait()

        return True