#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.
"""
Contains functions that are useful for determining the state of the
current user.
"""
import getpass
import hashlib
import os
from datetime import datetime
import sys
from typing import Optional

import pandas as pd
from mitosheet._version import __version__, package_name
from mitosheet.user.db import get_user_field
from mitosheet.user.schemas import (UJ_MITOSHEET_ENTERPRISE, UJ_MITOSHEET_LAST_UPGRADED_DATE,
                                    UJ_MITOSHEET_PRO)

try:
    import mitosheet_helper_pro
    MITOSHEET_HELPER_PRO = True
except ImportError:
    MITOSHEET_HELPER_PRO = False
try:
    import mitosheet_helper_enterprise
    MITOSHEET_HELPER_ENTERPRISE = True
except ImportError:
    MITOSHEET_HELPER_ENTERPRISE = False


def is_running_test() -> bool:
    """
    A helper function that quickly returns if the current code is running 
    inside of a test, which is useful for making sure we don't generate 
    tons of logs.
    """
    # Pytest injects PYTEST_CURRENT_TEST into the current environment when running
    running_pytests = "PYTEST_CURRENT_TEST" in os.environ
    # Github injects CI into the environment when running
    running_ci = 'CI' in os.environ and os.environ['CI'] is not None

    return running_pytests or running_ci

def is_on_kuberentes_mito() -> bool:
    """
    Returns True if the user is on Kuberentes Mito, on staging or on app
    """
    user = getpass.getuser()
    return user == 'jovyan'

def is_enterprise() -> bool:
    """
    Helper function for returning if this is a Mito Enterprise
    users
    """
    is_enterprise = get_user_field(UJ_MITOSHEET_ENTERPRISE)

    # This package overides the user.json
    if MITOSHEET_HELPER_ENTERPRISE:
        return MITOSHEET_HELPER_ENTERPRISE

    return is_enterprise if is_enterprise is not None else False

def is_pro() -> bool:
    """
    Helper function for returning if this is a
    pro deployment of mito
    """

    # This package overides the user.json
    if MITOSHEET_HELPER_PRO:
        return MITOSHEET_HELPER_PRO

    # If the current package is mitosheet-private, we activate Pro
    if package_name == 'mitosheet-private':
        return True

    # If you're on Mito Enterprise, then you get all Mito Pro features
    if is_enterprise():
        return True

    pro = get_user_field(UJ_MITOSHEET_PRO)

    return pro if pro is not None else False



def is_local_deployment() -> bool:
    """
    Helper function for figuring out if this a local deployment or a
    Mito server deployment
    """
    return not is_on_kuberentes_mito()  


def should_upgrade_mitosheet() -> bool:
    """
    A helper function that calculates if a user should upgrade, which does so by 
    checking if the user has upgraded in the past 21 days (3 weeks), since this is
    about how often we release big features.

    Always returns false if:
    - it is not a local installation, for obvious reasons.
    - if it has an admin package installed, as this is managed by an admin

    NOTE: if the user clicks the upgrade button in the app, then we change the upgraded 
    date to this date, so that the user doesn't get a bunch of annoying popups. This just
    pushes back when they are annoyed to upgrade!
    """
    if not is_local_deployment():
        return False
    
    from mitosheet.telemetry.telemetry_utils import MITOSHEET_HELPER_PRIVATE
    if MITOSHEET_HELPER_PRO or MITOSHEET_HELPER_PRIVATE:
        return False

    # If it's mitosheet-private, then we don't give them the upgrade prompts
    if package_name == 'mitosheet-private':
        return False
    
    last_upgraded_date_stored = get_user_field(UJ_MITOSHEET_LAST_UPGRADED_DATE)
    if last_upgraded_date_stored is None:
        return False

    mitosheet_last_upgraded_date = datetime.strptime(last_upgraded_date_stored, '%Y-%m-%d')
    return (datetime.now() - mitosheet_last_upgraded_date).days > 21

def get_pandas_version() -> str:
    """
    Returns the pandas version
    """
    return pd.__version__


def get_python_version() -> int:
    """
    Returns the Python version
    """
    return sys.version_info.minor


def check_pro_acccess_code(access_code: Optional[str]) -> bool:
    """Checks if the passed access code is correct, by hashing it and comparing to the hashed value"""
    return access_code is not None and hashlib.sha256(access_code.encode()).hexdigest() == '761a24dea594a8eafe698acfebb77de90bf0826c9400a2543500ee98929ea132'