#!/bin/bash
# shellcheck shell=bash

#############################
# PARSE CONFIGURATIONS
#############################
stage_port=$(awk -F "=" '/stage-port/ {print $2}' local.ini)
master_port=$(awk -F "=" '/master-port/ {print $2}' local.ini)

ssh_host=$(awk -F "=" '/ssh-host/ {print $2}' local.ini)
stage_host=$(awk -F "=" '/stage-mysql-host/ {print $2}' local.ini)
master_host=$(awk -F "=" '/master-mysql-host/ {print $2}' local.ini)

ssh_user=$(awk -F "=" '/ssh-user/ {print $2}' local.ini)

#############################
# FREE THE PORTS
#############################
function killproc (){
    lsof -i tcp:"$1" -t | xargs kill -9
    lsof -i tcp:"$1" -t 2>/dev/null >/dev/null || printf "killed processes on port %s\n" "$1"
}

killproc $stage_port
killproc $master_port

#############################
# ESTABLISH SSH CONNECTION
#############################
function establishconn() {
    ssh -fN -L localhost:"$1":"$2":3306 "$3"@"$4"
}

echo "Setting up stage on port " $stage_port
establishconn $stage_port $stage_host $ssh_user $ssh_host

echo "Setting up master on port " $master_port
establishconn $master_port $master_host $ssh_user $ssh_host
