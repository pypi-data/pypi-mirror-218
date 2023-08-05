from __future__ import absolute_import

import click
import pkg_resources

import xxxchat.utils.logger as logger
from xxxchat.configuration.profile_config import add_profile, add_default_profile
from xxxchat.utils.CommonUtil import waiting_stop
from xxxchat.xxx.CommandChat import CommandChat

VERSION = pkg_resources.require("xxx-chat")[0].version


@click.group()
@click.version_option(version=VERSION, prog_name='xxx-chat')
def commandchat_operator():
    pass


@click.command()
@click.option('-profile', help='Enable profile name')
def configure(profile):
    if profile is not None:
        add_profile(profile)
    else:
        add_default_profile()


@click.command()
@click.argument('message')
@click.option('-id', help=' enter chat id, something like context')
@click.option('-profile', help='Enable profile name')
def chat(message, id, profile):
    try:
        CommandChat(profile=profile, chat_log_id=id).chat(message)
    except Exception as e:
        logger.log_g(str(e))
        waiting_stop()


commandchat_operator.add_command(configure)
commandchat_operator.add_command(chat)


def main():
    commandchat_operator()
