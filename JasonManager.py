#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json


def Ler_Users():
    Users = {}

    if os.path.exists('UsersData.json'):
        with open('UsersData.json', 'r', encoding='utf-8') as f:
            Users= json.load(f)
    return Users

def Guardar_Users(Users):
    with open('UsersData.json', 'w', encoding='utf-8') as f:
        json.dump(Users, f, indent= 2,  ensure_ascii= False)

def Ler_Empregos():
    Empregos = {}

    if os.path.exists('EmpregosData.json'):
        with open('EmpregosData.json', 'r', encoding='utf-8') as f:
            Empregos= json.load(f)
    return Empregos

def Guardar_Empregos(Empregos):
    with open('EmpregosData.json', 'w', encoding='utf-8') as f:
        json.dump(Empregos, f, indent= 2,  ensure_ascii= False)

