from SCons.Script import *

def setupCommandLineArgs ():
    AddOption ('--compiler',
               dest='compiler',
               type='string',
               nargs=1,
               action='store',
               help='compiler',
               default='gcc')

    AddOption ('--mamainstall',
               dest='mamainstall',
               type='string',
               nargs=1,
               action='store',
               metavar='DIR',
               help='MAMA Binary installation location',
               default='/home/damian/workspace/openmama/OpenMAMA-codereview/openmama_install_2.3.1/')

    AddOption ('--mamaroot',
               dest='mamaroot',
               type='string',
               nargs=1,
               action='store',
               metavar='DIR',
               help='MAMA installation root directory',
               default='/home/damian/workspace/openmama/OpenMAMA-codereview/')

    AddOption ('--address-sanitizer',
               dest='address_sanitizer',
               action='store_true',
               default=False,
               help='Use address sanitizer')

    AddOption ('--memory-sanitizer',
               dest='memory_sanitizer',
               action='store_true',
               default=False,
               help='Use memory sanitizer')

    AddOption ('--thread-sanitizer',
               dest='thread_sanitizer',
               action='store_true',
               default=False,
               help='Use thread sanitizer')

    AddOption ('--no-debug',
               dest='no_debug',
               action='store_false',
               default=True,
               help='Disable debug build options')

    AddOption ('--no-error',
               dest='no_error',
               action='store_false',
               default=True,
               help='Disable -Werror compiler option.')

    AddOption ('--print-aliases',
               dest='aliases',
               action='store_true',
               default=False,
               help='Print the available aliases')

    AddOption ('--cflags',
               dest='cflags',
               nargs=1,
               type='string',
               action='store',
               help='CFLAGS to set for build')

    AddOption ('--ccflags',
               dest='ccflags',
               nargs=1,
               type='string',
               action='store',
               help='CCFLAGS to set for build')

    AddOption ('--cxxflags',
               dest='cxxflags',
               nargs=1,
               type='string',
               action='store',
               help='CXXFLAGS to set for build')


def setupTools (env):
    env.Tool ('nasm')

    compiler = GetOption('compiler')

    if compiler != 'default':
        if compiler == 'clang':
            env.Tool ('clang')
            env.Tool ('clang++')

        if compiler == 'clang-analyzer':
            if 'scan-build' not in os.environ['_'] and not GetOption('clean'):
                print 'If you wish to run with the static analyzer, please ensure ' \
                        'you execute scons within the scan-build tool.'
                print '\tscan-build <scan-build-arguments> scons <scons-arguments>'
                exit (1)

            env.Tool ('scan-build')

    if os.environ.has_key ('CC'):
        env.Replace( CC = os.environ['CC'] )

    if os.environ.has_key ('CXX'):
        env.Replace( CXX = os.environ['CXX'] )


def setupCompileFlags (env):
    env.Append (
                    LIBPATH = [
                                  '/usr/local/lib'
                              ],
                    ASFLAGS = ['-felf64', '-g'],
               )

    if GetOption ('no_error'):
        env.Append (
                        CCFLAGS = [
                                      '-Werror'
                                  ]
                   )

    if GetOption ('no_debug'):
        env.Append (
                        CCFLAGS =   [
                                        '-g',
                                        '-O0',
                                    ]
                    )
    else:
        env.Append (
                        CCFLAGS = [
                                    '-O2'
                                  ]
                   )

    if GetOption ('address_sanitizer'):
        env.Append  (
                        CCFLAGS   = [
                                        '-g', '-O0',
                                        '-fsanitize=address'
                                    ],
                        LINKFLAGS = [
                                        '-fsanitize=address'
                                    ]
                    )

    if GetOption ('memory_sanitizer'):
        env.Append (
                        CCFLAGS =   [
                                        '-g', '-O0',
                                        '-fsanitize=memory',
                                        '-fsanitize-memory-track-origins',
                                        '-fno-omit-frame-pointer'
                                    ],
                        LINKFLAGS = [
                                        '-g', '-O0',
                                        '-fsanitize=memory',
                                        '-fsanitize-memory-track-origins',
                                        '-fno-omit-frame-pointer'
                                    ]
                   )

    if GetOption ('thread_sanitizer'):
        env.Append (
                        CCFLAGS =   [
                                        '-g', '-O0',
                                        '-fsanitize=thread'
                                    ],
                        LINKFLAGS = [
                                        '-fsanitize=thread'
                                    ]
                   )

    if GetOption ('cflags'):
        env.Append (
                        CFLAGS = GetOption ('cflags')
                   )

    if GetOption ('ccflags'):
        env.Append (
                        CCFLAGS = GetOption ('ccflags')
                   )

    if GetOption ('cxxflags'):
        env.Append (
                        CXXFLAGS = GetOption ('cxxflags')
                   )

