"""
OptiBar
-------
Easy, Fast, Customizable
\n
cmd_support
-----------
cmd_support is boolean to active
Coloring system in your progress bar\n
Better to use it every time !

ProgressBar
-----------
Thanks for using this class, This class is very simple to use
so let's get started,\n
- Starting with arguments to define a progress bar\n
`ProgressBar.value` it means value of the progressbar (float)\n
`ProgressBar.max_value` it means limit of the progressbar.value (float)\n
`ProgressBar.details` it showing what's the progress will do (str)\n
`ProgressBar.passed_msg` it means when the progress is finished with no errors
show a text\n
`ProgressBar.error_msg` it means if `ProgressBar.e` equals the True
show a text\n
`ProgressBar.e` when you want raise a error with progressbar make it
True with this trick `ProgressBar.e = True`\n
`ProgressBar.value_name` it means the progressbar values name
just like this `MB -> 1MB / 1024MB\n
`ProgressBar.color` so if you want the progressbar color change to cyan
don't change string, Note : if you want to change color use `colorama` (library)\n

Defining A ProgressBar
----------------------
>>> import optibar as ob
>>> i = ob.ProgressBar ()

Changing Character Of ProgressBar
---------------------------------
So we have change it every time !
the progressbar copying characters from self.vc and self.vcc
if you want change the progressbar character type this
>>> ProgressBar.vc  = "@"
>>> ProgressBar.vcc = "#"
>>> ProgressBar.print ()
Now :
@@@@@@@@@@@@@@@@@@@@@@#@@@@@@@@@@@@@@@@@
Default :
━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━
    
Printing ProgressBar
--------------------
>>> i.print ()
    
Colorama
--------
- If you have only one version of Python installed:
`pip install colorama`\n\n

- If you have Python 3 (and, possibly, other versions) installed:
`pip3 install colorama`\n\n

- If you don't have PIP or it doesn't work
`python -m pip install colorama`
`python3 -m pip install colorama`\n\n

- If you have Linux and you need to fix permissions (any one):
`sudo pip3 install colorama`
`pip3 install colorama --user`\n\n

- If you have Linux with apt
`sudo apt install colorama`\n\n

- If you have Windows and you have set up the py alias
`py -m pip install colorama`\n\n

- If you have Anaconda
`conda install -c anaconda colorama`\n\n

- If you have Jupyter Notebook
`!pip install colorama`
`!pip3 install colorama`
"""

import colorama as clm

import os

def cmd_support (bool_:bool) :
    """
    cmd_support
    -----------
    cmd_support is boolean to active
    Coloring system in your progress bar\n
    Better to use it every time !"""
    clm.init (bool_)

class ProgressBar :
    """
    ProgressBar
    -----------
    Thanks for using this class, This class is very simple to use
    so let's get started,\n
    - Starting with arguments to define a progress bar\n
    `ProgressBar.value` it means value of the progressbar (float)\n
    `ProgressBar.max_value` it means limit of the progressbar.value (float)\n
    `ProgressBar.details` it showing what's the progress will do (str)\n
    `ProgressBar.passed_msg` it means when the progress is finished with no errors
    show a text\n
    `ProgressBar.error_msg` it means if `ProgressBar.e` equals the True
    show a text\n
    `ProgressBar.e` when you want raise a error with progressbar make it
    True\n
    `ProgressBar.value_name` it means the progressbar values name
    just like this `MB -> 1MB / 1024MB\n
    `ProgressBar.color` so if you want the progressbar color change to cyan
    don't change string, Note : if you want to change color use `colorama` (library)\n
    
    Defining A ProgressBar
    ----------------------
    >>> import optibar as ob
    >>> i = ob.ProgressBar ()

    Changing Character Of ProgressBar
    ---------------------------------
    So we have change it every time !
    the progressbar copying characters from self.vc and self.vcc
    if you want change the progressbar character type this
    >>> ProgressBar.vc  = "@"
    >>> ProgressBar.vcc = "#"
    >>> ProgressBar.print ()
    Now :
    @@@@@@@@@@@@@@@@@@@@@@#@@@@@@@@@@@@@@@@@
    Default :
    ━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━

    Printing ProgressBar
    --------------------
    >>> i.print ()
    
    Colorama
    --------
    - If you have only one version of Python installed:
    `pip install colorama`\n\n

    - If you have Python 3 (and, possibly, other versions) installed:
    `pip3 install colorama`\n\n

    - If you don't have PIP or it doesn't work
    `python -m pip install colorama`
    `python3 -m pip install colorama`\n\n

    - If you have Linux and you need to fix permissions (any one):
    `sudo pip3 install colorama`
    `pip3 install colorama --user`\n\n

    - If you have Linux with apt
    `sudo apt install colorama`\n\n

    - If you have Windows and you have set up the py alias
    `py -m pip install colorama`\n\n

    - If you have Anaconda
    `conda install -c anaconda colorama`\n\n

    - If you have Jupyter Notebook
    `!pip install colorama`
    `!pip3 install colorama`
    """
    def __init__(self, value:float=0, max_value:float=100,
                 details:str=None, passed_msg:str="Succesfully Completed",
                 error_msg:str="The Progess Has Finished With Errors",
                 e:bool=False, value_name:str="", color:str=clm.Fore.CYAN,
                 e_mode:str="error") :
        self.value = value
        self.max_value = max_value
        self.details = details
        self.vcc = "╺"
        self.vc = "━"
        self.emsg = error_msg
        self.pmsg = passed_msg
        self.e = e
        self.st = 0
        self.u = 0
        self.vn = value_name
        self.color = color
        self.e_mode = e_mode
    
    def print (self) :
        """
        print
        -----
        To print the ProgressBar use this function because it's
        fast, Optimized and Easy to print the ProgressBar,
        But if you want print ProgressBar don't print anything except the ProgressBar
        , But if your ProgressBar has Finished print anything you like
        """
        if not self.e == True :
            val = self.value
            vc = val
            val_ = f"{self.color}"
            x = 0
            z = 0
            for i in range (40) :
                val = val - (self.max_value / 40)
                if not val < 0 :
                    x += 1
                else : break
            val_ += f"{self.vc}" * x
            if x < 40 :
                val_ += f"{clm.Fore.RESET}{self.vcc}"
            z = x
            x + 1
            for i in range (40 - x) :
                val_ += self.vc
            if self.value == self.max_value or self.value > self.max_value :
                a = ""
                for i in str(self.value) + str(self.max_value) + "  " + (self.vn * 2) :
                    a += " "
                print ("\r  "+self.pmsg + "                                                                                " + a)
            else :
                if self.st == 0 :
                    print (f"{self.details}\n{val_}{clm.Fore.RESET} {int (z * 2.5)}% / 100% - {self.value}{self.vn} / {self.max_value}{self.vn}{clm.Fore.RESET}",end="")
                    self.st = 1
                elif self.st == 1 :
                    print (f"\r{val_}{clm.Fore.RESET} {int (z * 2.5)}% / 100% - {self.value}{self.vn} / {self.max_value}{self.vn}{clm.Fore.RESET}",end="")
        else :
            if self.u == 0 :
                self.u = 1
                if self.e_mode == "error" :
                    print (f"\n{clm.Back.RED}{clm.Fore.WHITE} "+self.emsg+f" {clm.Back.RESET}{clm.Fore.RESET}")
                elif self.e_mode == "bug" :
                    print (f"\n{clm.Back.YELLOW}{clm.Fore.WHITE} "+self.emsg+f" {clm.Back.RESET}{clm.Fore.RESET}")
                else :
                    print (f"\n{clm.Back.RED}{clm.Fore.WHITE} "+self.emsg+f" {clm.Back.RESET}{clm.Fore.RESET}")

a = ProgressBar ()
a.value = 10
a.print ()