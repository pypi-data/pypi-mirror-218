def compile_gvec_to_python():
    
    import subprocess
    import os
    import gvec_to_python
    import pyccel

    libpath = gvec_to_python.__path__[0]
    
    # pyccel flags
    flags = ''
    
    _li = pyccel.__version__.split('.')
    _num = int(_li[0])*100 + int(_li[1])*10 + int(_li[2])
    if _num >= 180:
        flags += '--conda-warnings off'
    
    print('\nCompiling gvec-to-python kernels ...')
    subprocess.run(['make', 
                    '-f', 
                    os.path.join(libpath, 'Makefile'),
                    'flags=' + flags,
                    'install_path=' + libpath,
                    ], check=True, cwd=libpath)
    print('Done.')

