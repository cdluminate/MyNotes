python package manager, anaconda
================================

Anaconda ships many packages by default but many of them may not be
needed. One can install Miniconda (Lite version of Anaconda) and
packages in need by himself.

download https://mirrors.tuna.tsinghua.edu.cn/anaconda/

doc https://docs.continuum.io/anaconda/

quick start https://conda.io/docs/test-drive.html

conda command quick reference
-----------------------------

::

    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
    conda config --set show_channel_urls yes

::

    anaconda-navigator

::

    conda --version
    conda update conda

    conda create --name snowflakes biopython
    conda create --name bunnies python=3.5 astroid babel
    conda info --envs
    conda remove --name flowers --all

    conda search --full-name python
    python --version

    conda list
    conda search beautifulsoup4
    conda install --name bunnies beautifulsoup4
    conda install iopro
    conda remove --name bunnies iopro
    conda remove --name snakes --all

    rm -rf ~/miniconda OR  rm -rf ~/anaconda
