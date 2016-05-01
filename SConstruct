import os
from site_utils import *

setupCommandLineArgs ()

VariantDir ('build', 'src')

env = Environment (
                      HOMELOCATION   = os.getcwd(),
                      LOCALINCLUDE   = '$HOMELOCATION/build/include',
                      BININSTALL     = '$HOMELOCATION/install/bin',
                      LIBINSTALL     = '$HOMELOCATION/install/lib',
                      INCLUDEINSTALL = '$HOMELOCATION/install/include',
                      MAMAINSTALL    = GetOption('mamainstall'),
                      MAMACORE       = GetOption('mamaroot')
                  )

setupTools (env)
setupCompileFlags (env)

# Main MamaC++ libraries
SConscript ('build/lib/mamac++/SConscript', 'env')

# Library Public Headers
SConscript ('build/include/SConscript', 'env')

# Sample applications
SConscript ('build/bin/SConscript', 'env')

if GetOption('aliases'):
    print 'Available Build Aliases:'
    print '-----'
    aliases = SCons.Node.Alias.default_ans.keys()
    aliases.sort()
    for x in aliases:
        print x

    exit (0)
