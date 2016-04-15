#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
from random import randrange
from ale_python_interface import ALEInterface
import gflags


FLAGS = gflags.FLAGS

gflags.DEFINE_string('rom', None, 'the rom to run', short_name='r')
gflags.MarkFlagAsRequired('rom')
gflags.DEFINE_boolean('display', False, 'display the emulator screen', short_name='d')
gflags.DEFINE_boolean('sound', False, 'play sounds')
gflags.DEFINE_integer('seed', 123, 'random seed')


def main(argv):

    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print 'Error:', e
        print 'Usage: ',FLAGS
        sys.exit(1)


    ale = ALEInterface()

    # Get & Set the desired settings
    ale.setInt(b'random_seed', FLAGS.seed)

    # Set USE_SDL to true to display the screen. ALE must be compilied
    # with SDL enabled for this to work. On OSX, pygame init is used to
    # proxy-call SDL_main.
    USE_SDL = FLAGS.display
    if USE_SDL:
      if sys.platform == 'darwin':
        import pygame
        pygame.init()
        ale.setBool('sound', False) # Sound doesn't work on OSX
      elif sys.platform.startswith('linux'):
        ale.setBool('sound', FLAGS.sound)
      ale.setBool('display_screen', FLAGS.display)

    # Load the ROM file
    rom_file = str.encode(FLAGS.rom)
    ale.loadROM(rom_file)

    # Get the list of legal actions
    legal_actions = ale.getLegalActionSet()
    minimal_actions = ale.getMinimalActionSet()
    print "Legal Actions:", legal_actions
    print "Minimal Actions:", minimal_actions
    print "Screen size:", ale.getScreenDims()

    # Play 10 episodes
    for episode in range(10):
      total_reward = 0
      while not ale.game_over():
        a = legal_actions[randrange(len(legal_actions))]
        # Apply an action and get the resulting reward
        reward = ale.act(a);
        total_reward += reward
        #print ale.getFrameNumber(), ale.getEpisodeFrameNumber(), reward, total_reward
      print('Episode %d ended with score: %d' % (episode, total_reward))
      ale.reset_game()


if __name__ == '__main__':
    main(sys.argv)
