# script to push repos to github
from time import localtime, strftime
import os
import fire
import subprocess

# vars
name = os.environ['USER']
time = strftime("%Y-%m-%d %H:%M:%S", localtime())
dotLoc = '/home/{}/m/dot'.format(name)
vimLoc = '/home/{}/m/vim'.format(name)
dotList = [
    '/home/{}/.vimrc'.format(name),
    '/home/{}/.config/ion/initrc'.format(name),
    '/home/{}/.config/alacritty/alacritty.yml'.format(name),
    '/home/{}/.tmux.conf.local'.format(name),
]


def sub(command, loc):
    p = subprocess.Popen(
        command,
        cwd=loc,
        stdout=subprocess.PIPE
    )
    for line in iter(p.stdout.readline, b''):
        print('>>> {}'.format(line.rstrip().decode('utf-8')))


def rsyncList(loc):
    return [[
        'rsync',
        '-av',
        '-P',
        '--outbuf=L',
        '{}'.format(l),
        '{}'.format(loc)] for l in dotList]


def push(loc):
    sub(['git', 'add', '-A'], loc)
    sub(['git', 'commit', '-m', '"{}"'.format(time)], loc)
    sub(['git', 'push'], loc)


def dot():
    [sub(l, dotLoc) for l in rsyncList(dotLoc)]
    push(dotLoc)


def vim():
    push(vimLoc)


def all():
    dot()
    vim()


if __name__ == '__main__':
    fire.Fire()
