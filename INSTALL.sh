#!/bin/sh 
########################################################################
# <INSTALL.sh, Install script for mmmserice project
# Copyright (C) 2014  Manuel Moscoso Dominguez manuel.moscoso.d@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
########################################################################
SCRIPT_USER=root
SCRIPT_NAME="INSTALL.sh"
SCRIPT_LOCATION=/usr/local/bin/

## DEFINITION OF SCRIPTS
SOFTWARE_NAME=mm-monitor

## INIT SCRIPT
INITSCRIPT_NAME=mmmservice
INITSCRIPT_PATH=/etc/init.d/$INITSCRIPT_NAME

## SCRIPT LOCATION
SCRIPT_SERVICE=$SCRIPT_LOCATION$SOFTWARE_NAME

## CONFIGURATION
CONFIG_DIR=/etc/$SOFTWARE_NAME
CONFIG_NAME=mmmservice.cfg
CONFIG_PATH=$CONFIG_DIR/$CONFIG_NAME

### COLORS  FOR MESSAGES ###############################################
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # End COLOR
########################################################################

check_user () {
	if [ $SCRIPT_USER != $USER ]
	then
		echo "This script must be run as root"
		exit 1
	fi
}

case "$1" in
	remove)
		echo "${RED}Removing $SCRIPT_SERVICE ${NC}"
		rm -rf $SCRIPT_SERVICE
		echo "${RED}Removing $CONFIG_PATH ${NC}"
		rm -rf $CONFIG_DIR
        echo "${RED}Removing $INITSCRIPT_PATH ${NC}"
		rm -rf $INITSCRIPT_PATH
		echo "${GREEN}Files removed ${NC}"
	;;

	depends)
		check_user 
		echo "For Debian and derived distributions"
		echo "apt-get install python"
	;;
	install)
		check_user
		echo "${GREEN}Installing $SOFTWARE_NAME in $SCRIPT_SERVICE ${NC}"
		cp $SOFTWARE_NAME $SCRIPT_SERVICE
		chmod 700 $SCRIPT_SERVICE
		chown root:root $SCRIPT_SERVICE
		
		echo "${GREEN}Installing $INITSCRIPT_NAME in $INITSCRIPT_PATH ${NC}"
		cp $INITSCRIPT_NAME $INITSCRIPT_PATH
		chmod 700 $INITSCRIPT_PATH
		chown root:root $INITSCRIPT_PATH
		/lib/systemd/systemd-sysv-install enable $INITSCRIPT_NAME
        
		echo "${GREEN}Installing $CONFIG_NAME in $CONFIG_PATH ${NC}"
		if [ ! -d "$CONFIG_DIR" ]; then
			# Control will enter here if $DIRECTORY doesn't exist.
			echo "${GREEN}Creating $CONFIG_DIR  ${NC}"
			mkdir $CONFIG_DIR
            cp $CONFIG_NAME $CONFIG_PATH
		else
			echo "${YELLOW}Directory $CONFIG_DIR already exists ${NC}"
            cp $CONFIG_NAME $CONFIG_PATH
		fi
		
		
		echo "Installation completed"
	;;
	check)
		check_user
		#FILE EXISTS
		echo "${YELLOW}Checking${NC}"
		## mm-monitor
		if [ ! -f $SCRIPT_SERVICE ]; then
			echo "${RED}$SCRIPT_SERVICE does not exists${NC}"
		else
			echo "${GREEN}$SCRIPT_SERVICE exists${NC}"
		fi
		## mmmservice.cfg
		if [ ! -f $CONFIG_PATH ]; then
			echo "${RED}$CONFIG_PATH does not exists${NC}"
		else
			echo "${GREEN}$CONFIG_PATH exists${NC}"
		fi
        ## mmmservice
		if [ ! -f $INITSCRIPT_PATH ]; then
			echo "${RED}$INITSCRIPT_PATH does not exists${NC}"
		else
			echo "${GREEN}$INITSCRIPT_PATH exists${NC}"
		fi
		
	;;
	*)
		check_user
		echo "${YELLOW}Instructions"
		echo "Usage: sh $SCRIPT_NAME {check|install|depends|remove}"
		echo "check: For check the correct user"
		echo "install: For installations of scripts"
		echo "depends: For view depends of scripts"
		echo "remove: For detele all files"
		echo "${NC}"
		exit 1
	;;
esac
exit 0 
Status 
