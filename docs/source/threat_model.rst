.. _threat_model :


============
Threat Model
============

This section describes attacks, classes of attacks APAF should prevent/resist.

The Application
---------------
The Anonymous Python Application Framework is built and delivered as a
standalone application, and consists in a simple static file server.

Double clicking the executable, a new browser tab will show the configuration
page, on which the user can select the destination folder and edit advanced
options.

Entry Points: Hidden Service port selected in the configuration page, telnet
login?
Flowing Data: documents selected from the user

Key Scenarios
-------------

The application may be used from:
  - a generic anonymous user intending not to share its identity;
  - an anonymous activist;
  - a non-profit organization with a low budget;
  - an anonymous user interested in sharing documents but unable to host a server


Vulnerabilities
---------------
Follows a list of the vulnerable corners of the applciation:
 - gain access to the configuration page on the login may lead to serving system directories;
 - possible xss;
 - executable infection;
 - data leakage outside tor;

Attacks
--------
Follows a list of attacks a malicious user may perform:
 - bruteforce over the login form;
 - the .exe/.app contains, compressed, all the python standard library in pyc
   format. Replacing one of these bytecode libraries may lead to the control of
   the applciation;
 - denial of service;



Security Controls
-----------------
Attacks precaution mostly concerns a possible misconfiguration of APAF, since
.onion domains avoid by their own possible traffic poisoning or man in the
middle attacks.

*todo: hence, the user should be warned with very clear, syntethic but
explicative descriptions whenever modifying a certain item of the configuration*
