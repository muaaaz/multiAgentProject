#!/bin/sh
java -Xms1024m -Xmx20480m -cp frodo2.16/frodo2.jar frodo2.controller.Controller -local | tee output.log
