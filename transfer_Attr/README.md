
# HOW TO USE
1. clone the repository or copy the required script module to maya script folder
eg. "Documents\maya\2020\scripts"
2. Type the following code into the maya script editors python tab and run to access the tool
    ```python
    import maya.cmds as cmds
    ver = cmds.about(version = True)
    if '2014' in ver:
        import transfer_Attr.core_2014 as core
    else:
        import transfer_Attr.core as core

    reload(core)
    core.UI()
    ```
    for repeated use you could add the above snippet as a shelf icon
    
3. A simple tool demo can be found here

    [![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/i5xlmWOz4wg/0.jpg)](http://www.youtube.com/watch?v=i5xlmWOz4wg)
    
4. If all goes correctly you should get the tool a screen shot is given below


    ![alt text](transfer_Attr/ui/transfer_ui.JPG)
