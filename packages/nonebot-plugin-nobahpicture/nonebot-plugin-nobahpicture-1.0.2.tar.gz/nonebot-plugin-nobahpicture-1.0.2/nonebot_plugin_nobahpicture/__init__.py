import asyncio
from re import I, sub
from typing import Any, Tuple, Union, Annotated

from nonebot import on_regex, get_driver, on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.params import Command, RegexGroup
from nonebot.plugin import PluginMetadata
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (GROUP, PRIVATE_FRIEND, Bot, Event,
                                         Message, MessageSegment,
                                         GroupMessageEvent,
                                         PrivateMessageEvent)

from .rules import rule, plugin_rule
from .config import Config
from .get_picture import GetPicture

global_config = get_driver().config
config = Config.parse_obj(global_config)


__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-nobahpicture',
    description='获取碧蓝档案涩图',
    usage='https://github.com/Lptr-byte/nonebot-plugin-nobahpicture',
    homepage='https://github.com/Lptr-byte/nonebot-plugin-nobahpicture',
    type='application',
    supported_adapters={'nonebot.adapters.onebot.v11'},
    extra={
        'author': 'Hanasa',
        'version': '1.0.2',
        'priority': 1,
    },
)


change_plugin_state = on_command(('Ba涩图', '开启'), rule=to_me(), aliases={('Ba涩图', '禁用')},
                                 permission=SUPERUSER)
save_picture_state = on_command(('Ba涩图保存功能', '开启'), rule=to_me(), aliases={('Ba涩图保存功能', '关闭')},
                                permission=SUPERUSER)
give_me_picture = on_regex(r'^(来点Ba涩图)\s?([x|X|*]?\d+[张|个|份]?)?\s?(.*)?',
                           rule=plugin_rule, flags=I,
                           permission=PRIVATE_FRIEND | GROUP)


@change_plugin_state.handle()
async def _(cmd: Tuple[str, str] = Command()):
    _, action = cmd
    if action == '开启':
        config.plugin_enabled = True
    elif action == '禁用':
        config.plugin_enabled = False
    await change_plugin_state.finish(f'Ba涩图插件已{action}')


@save_picture_state.handle()
async def _(cmd: Tuple[str, str] = Command()):
    _, action = cmd
    if action == '开启':
        config.save_enabled = True
    elif action == '关闭':
        config.save_enabled = False
    await save_picture_state.finish(f'Ba涩图插件保存功能已{action}')


@give_me_picture.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent],
            regex_group: Annotated[tuple[Any, ...], RegexGroup()]):
    args = list(regex_group)
    logger.debug(f'args={args}')
    num = args[1]
    tag = args[2]
    #处理数据
    num = int(sub(r'\D', '', num)) if num else 1
    num = min(num, config.max_picture)
    tag = tag if tag else ''
    get_pic = GetPicture(pic_num=num, user_tag=tag, save=config.save_enabled)
    await get_pic.get_picture()
    image_urls = []
    image_urls = get_pic.get_urls()
    del get_pic
    for url in image_urls:
        try:
            await bot.send(event, MessageSegment.image(url))
        except:
            await bot.send(event, MessageSegment.text('发送图片失败……'))
            logger.error('发送图片失败……')
    await give_me_picture.finish()