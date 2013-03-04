# Python Wrapper for Checkvist API

This is a wrapper for the [Checkvist: Open API](https://checkvist.com/auth/api). It includes all calls found in the official documentation. Please see the source code to clarify arguments and see some basic examples.

This wrapper is intended to be used conventionally and with [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8) on iOS. The optional debugger uses print statements, because they seem to perform better on iOS.

## Installation ##

Currently, the wrapper is only available on GitHub. After using it for a few more weeks, I'll submit it to pypi. For now, you can place checkvist.py in any directory in your path and import as usual. To use the wrapper with an application like Keyboard Maestro, use a shell script action with something like the following:

    #!/usr/bin/env python
    
    import imp
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    
    username = '' 		# Enter email address
    remote_key = '' 	# Enter remote key
    
    # Import workaround for Keyboard Maestro
    checkvist = imp.load_source('checkvist', '/Volumes/MacintoshHD/skorzdorfer/unix/bin/checkvist.py')
    
    # Create instance
    cl = checkvist.user_account(username, remote_key, bugger=1)
    
    # To Turn off the Debugger
    # cl = checkvist.user_account(username, remote_key) 
     
    # Send authentication
    cl.send_auth()
    
    # get all all lists
    my_lists = cl.get_lists()
    
## Pythonista Installation

Create a new empty file and paste in checkvist.py. Name the file checkvist.
Create a new file for your script and enter something like the following: 

    #!/usr/bin/env python
    import checkvist
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    
    username = ''
    remote_key = ''
    
    # Create instance
    cl = checkvist.user_account(username, remote_key, bugger=1)
    
    # To Turn off the Debugger
    # cl = checkvist.user_account(username, remote_key)
    
    # Send authentication
    cl.send_auth()
    
    # get all all lists
    my_lists = cl.get_lists()

