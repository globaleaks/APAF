=========
JSON APIs
=========


 GET /services
    #    returns the list of running services

 GET /services/<servicename>
    #   returns informations about the service <servicename>
    #   404 if <servicename> was not found

 GET /services/<servicename>/start  ,  GET /services/<servicename>/stop
    #   Start/stop a service. Returns a json object {'result': state} where state
    #   is a boolean


 GET /config
    # return a key:value dictionary for each item in the config file.

 PUT /config  ## XXX must be post. ###
    # given a dictionary {key:value}, substitute each item with name `key` in
    # the dictionary with `value`.
    # In case of error, return a json object {'error':message}


 GET /tor/<spkey>
    # Wraps the command GETINFO <spkey> to the controlport.
    # return 404 in case the command is not valid, a json object {'error':message}
    # otherwise

 POST /auth/login
    # oAuth login - not implemented.

 GET /auth/logout
    # logout
