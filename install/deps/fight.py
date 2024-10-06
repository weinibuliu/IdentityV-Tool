from json import load,loads
from time import sleep,time,localtime,strftime
from pathlib import Path
from random import randint,shuffle

from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition

from .infos import base_roi
from .infos import common
from .infos import Opera_Singer

#获取路径
main_path = Path.cwd()

#传出 custom 信息
def rec_name_list() -> list[str]:
    return []
def rec_list() -> list:
    return []
def act_name_list() -> list[str]:
    return ["Fight","Move","Vision_move","Thumb_ups"] + ["Check_weekly"] + ["OS_round"]
def act_list() -> list:
    Move = common.Move
    Vision_move = common.Vision_move
    OS_round = Opera_Singer.OS_round
    return [Fight(),Move(),Vision_move(),Thumb_ups()] + [Check_weekly()] + [OS_round()]

def get_roi_base_on_state(roi_state:str):
    match roi_state:
        case "PC16_9":
            roi = base_roi.PC16_9
        case "Android16_9":
            roi = base_roi.Android16_9
        case _:
            raise("roi 声明参数异常，请联系开发者。")
        
    return roi

class Fight(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        current_real_time = strftime("%H:%M:%S",localtime(time()))
        model_list = "匹配模式"
        character_list = "歌剧演员"
        with open(f"{main_path}/config/fight_config.json","r",encoding="utf-8") as f:
            data = load(f)
            
            base_options = data["基础设置"]
            character_list = list(base_options["角色队列"])
            character_list_random = bool(base_options["角色队列乱序"])
            model_list = list(base_options["模式队列"])
            model_list_random = bool(base_options["模式队列乱序"])
            thumbs_up = bool(base_options["启用赛后点赞"])
            desktop_notice = bool(base_options["启用桌面通知"])
            email_notice = bool(base_options["启用邮件通知"])

            stop_options = data["停止相关设置"]
            up_weekly = bool(stop_options["启用周上限限制"])
            reputation_limit = int(stop_options["最低人品值"])
            time_limit = bool(stop_options["启用时间限制"])
            limit_time = int or float or str(stop_options["限制时间"])
            times_limit = bool(stop_options["启用次数限制"])
            limit_times = int(stop_options["限制次数"])
            
            check_options = data["检测频率设置"]
            check_reputation_rate = check_options["检测人品值频率"]
            check_weely_rate = check_options["检测周上限频率"]

            stop_dict = {"周上限限制": up_weekly, "时间限制": time_limit, "次数限制": times_limit}
            del_list = []
            for key ,value in stop_dict.items():
                if value == False:
                    del_list.append(key)
            for key in del_list:
                del stop_dict[key]
            for key,value in ["时间限制","次数限制"],[limit_time,limit_times]:
                if key in stop_dict.keys():
                    stop_dict[key] = value

        context.override_pipeline({"fight_检测人品值": {"custom_recognition_param": {"lowest" : reputation_limit}}})
        context.override_pipeline({"匹配成功":{"post_delay": 7000, "next": []}})

        def fight_main(character:str):
            fight_start_time = time()
            time_diff = 0
            match character:
                case "歌剧演员":
                    context.run_pipeline("歌剧演员_获取影跃位置")
                    context.run_pipeline("歌剧演员_获取普攻位置")
                    while time_diff < 235:
                        context.run_pipeline("随机移动")
                        context.run_pipeline("随机视角移动")

                        for i in range(randint(10,20)):
                            context.run_pipeline("歌剧演员_循环")
                            i += 1
                            fight_now_time = time()
                            time_diff = fight_now_time - fight_start_time
                            if time_diff >= 235:
                                break

                        check_fight_statu = context.run_recognition("fight_赛后_继续_仅识别",image=context.tasker.controller.cached_image).best_result.text
                        if check_fight_statu == "继续":
                            break
                        
                        fight_now_time = time()
                        time_diff = fight_now_time - fight_start_time
                        context.run_pipeline("随机视角移动")

                case _:
                    raise (f"Class Error:{__class__.__name__},please contact to the developers.")
                
            if time_diff >= 235:
                context.run_pipeline("fight_打开设置")
                context.run_pipeline("fight_赛后_继续")

        def fight_hide_main():
            pass

        def ready(model:str,character:str) -> None:
            context.override_pipeline({"检测是否进入游戏": {"next" :[], "on_error": []}})
            context.run_pipeline("fight_点击书")
            sleep(0.5)
            context.run_pipeline(f"fight_{model}")
            sleep(0.5)
            if model == "匹配模式" or model == "排位模式":
                context.run_pipeline("fight_点击监管者")
                sleep(0.5)
                context.run_pipeline("fight_开始匹配")
                if model == "排位模式":
                    context.run_pipeline("确认禁用")
                context.override_pipeline({"fight_选择角色":{"template":f"characters//{character}.png"}})
                context.run_pipeline("fight_切换角色")

            elif model == "捉迷藏":
                context.run_pipeline("fight_准备开始")

            else:
                raise (f"Class Error:{__class__.__name__},please contact to the developers.")

        def main(desktop_notice:bool=desktop_notice,email_notice:bool=email_notice,
                 model_list:list=model_list,model_list_random:bool=model_list_random,
                 character_list:list=character_list,character_list_random:bool=character_list_random,
                 thumbs_up:bool=thumbs_up,
                 reputation_limit:int=reputation_limit,up_weekly:bool=up_weekly,
                 time_limit:bool=time_limit,limit_time:int|float=limit_time,
                 times_limit:bool=times_limit,limit_times:int=limit_times,
                 ) -> None:


            character_list_len = len(character_list)
            if character_list_len == 1:
                pass

            def list_ramdon(m_list_random:bool=model_list_random,c_list_random:bool=character_list_random): #模式、角色队列乱序
                if m_list_random == True:
                    shuffle(model_list)
                if c_list_random == True:
                    shuffle(character_list)

            if thumbs_up == False:
                context.override_pipeline({"fight_赛后_继续": {"next": ["fight_赛后_返回大厅"]}})
            else:
                context.override_pipeline({"fight_点赞": {"custom_action_param": {"model": model}}})


            while True:
                list_ramdon()
                for character in character_list:
                    for model in model_list:
                        ready(model,character)
                        if model == "匹配模式" or model == "排位模式":
                            fight_main(character)
                        elif model == "捉迷藏":
                            pass
                        else:
                            raise (f"Class Error:{__class__.__name__},please contact to the developers.")

        main()
        
        return True
    
class Thumb_ups(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        model = loads[argv.custom_action_param]["model"]
        if model == "匹配模式":
            gamer_list = list[1,2,3,4]
            shuffle(gamer_list)
            for i in gamer_list:
                match i:
                    case 1:
                        context.override_pipeline({f"{model}点赞":{"roi": [300,490,45,45]}})
                    case 2:
                        context.override_pipeline({f"{model}点赞":{"roi": [550,490,45,45]}})
                    case 3:
                        context.override_pipeline({f"{model}点赞":{"roi": [805,490,45,45]}})
                    case 4:
                        context.override_pipeline({f"{model}点赞":{"roi": [1075,490,45,45]}})
                    case _:
                        raise (f"Class Error:{__class__.__name__},please contact to the developers.")
                context.run_pipeline(f"{model}点赞")   
        elif model == "捉迷藏":
            gamer_list = list[1,2]
            shuffle(gamer_list)
            for i in gamer_list:
                match i:
                    case 1:
                        pass
                    case 2:
                        pass
                    case _:
                        raise (f"Class Error:{__class__.__name__},please contact to the developers.")
        else:
            raise (f"Class Error:{__class__.__name__},please contact to the developers.")

        return True

class Check_reputation(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg) -> CustomRecognition.AnalyzeResult:
        roi_state = loads(argv.custom_recognition_param)["roi_state"]
        roi = get_roi_base_on_state(roi_state)
        
        lowest = loads(argv.custom_recognition_param)["lowest"]

        Get_reputation_pipe = {"Get_reputation":{
            "timeout": 3000,
            "recognition": "OCR",
            "roi": roi.roi_getreputation,
            "only_rec": True
            }}
        
        rec_result = context.run_recognition("Get_reputation",argv.image,pipeline_override = Get_reputation_pipe)
        rec_result = rec_result.best_result.text

        if rec_result <= lowest:
            context.override_pipeline({"fight_检测人品值": {"next":["fight_人品值低_桌面提醒"]}})

        return super().analyze(context, argv)
    
class Check_weekly(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg) -> None:
        pass
        return None
    

class Fight_Config_Check(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        return True