from distutils.core import setup

setup(
    name = 'fastminhash',
    packages = ['minhash'],
    version = '0.1.1',
    license = 'MIT',
    description = 'N-gram MinHash implementation in C',
    author = 'starcatmeow',
    author_email = 'dongruixuan@hotmail.com',
    url = 'https://github.com/starcatmeow/fastminhash',
    setup_requires = ['cffi>=1.0.0'],
    cffi_modules = ['minhash/minhash_build.py:ffibuilder'],
    install_requires = ['cffi>=1.0.0']
)
