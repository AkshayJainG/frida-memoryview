# frida-memoryview

A vim-like frida-based process memory viewer.  

The original software is available at  
https://github.com/walterdejong/hexview.    
This project is a partial enhancement of the above great software.  

<img width="481" alt="image" src="https://user-images.githubusercontent.com/56913432/106864280-fd304680-670c-11eb-8ff7-a55be8911ac0.png">

# Features 
The process memory of the target process can be monitored in real time.  
You can also edit the memory value.  
It also has a function to automatically move to the specified address and intercept when hooking in frida.  

# Setup
・install flask + requests
```sh
pip3 install -r requirements.txt
```
・windows: install windows-curses
```sh
pip install windows-curses
```

# Usage
You need to start both the flask server and hexview.   
If necessary, please run frida-server on the target device.

・flaskserver_side
```sh
python3 main.py processname
```
・hexviewer_side
```sh
python3 hexview.py
```

Some of the features of the original software have been modified.  
The usage is ```:?``` command to find out how to use it.

# Intercept
There are times when you want to monitor the value of a specific address when hooking in frida.  
With ```intercept(address)```, the process will stop until you press ```F``` on hexview.  
This allows you to monitor and edit the memory just like intercepting with a proxy tool.  

- - -
_Copyright 2016 by Walter de Jong <walter@heiho.net>_