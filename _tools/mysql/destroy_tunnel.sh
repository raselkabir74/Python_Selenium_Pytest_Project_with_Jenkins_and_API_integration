#!/bin/bash
# shellcheck shell=bash

#############################
# PARSE CONFIGURATIONS
#############################
stage_port=$(awk -F "=" '/stage-port/ {print $2}' local.ini)
master_port=$(awk -F "=" '/master-port/ {print $2}' local.ini)


#############################
# FREE THE PORTS
#############################
function killproc (){
    lsof -i tcp:"$1" -t | xargs kill -9
    lsof -i tcp:"$1" -t 2>/dev/null >/dev/null || printf "killed processes on port %s\n" "$1"
}

killproc $stage_port
killproc $master_port
