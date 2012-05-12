============
Threat Model
============

*21:15 < rransom> What security properties should APAF provide? What attacks (or
classes of attacks) should APAF prevent or resist?*
This section describes the classes of attacks the APAF should prevent/resist.

The Application
---------------
*present briefly the application and describe how the user shall interact with
it*
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
*who is going to use the application?*

The application may be used from:
  - a generic anonymous user intending not to share its identity;
  - an anonymous activist;
  - a non-profit organization with a low budget;
  - an anonymous user interested in sharing documents but unable to host a server

Vulnerabilities
---------------
*a list of the vulnerable corners of the application.*
 - gain access to the configuration page on the login may lead to serving system dirrectories;
 - possible xss;
 - executable infection;
 - data leakage outside tor;
 - *read twisted documentation, which kind of authentication does twisted support?*

Attacks
--------
*the attack a malicious user may perform*

 - bruteforce over the login form;
 - the .exe/.app contains, compressed, all the python standard library in pyc
   format. Replaacing one of these bitcode libraries may lead to the control of
   the applciation.
 - denial of service


Security Controls
-----------------
*Precautions for attacks*
As far as I know, -onion hostnames, by thir own, provide  a secutipry mechanisms
to avoid poisoning or man in the middle attacks.

The user shall be advised with very clear messages in the configuration page
about the consequences of editing a certain box.

