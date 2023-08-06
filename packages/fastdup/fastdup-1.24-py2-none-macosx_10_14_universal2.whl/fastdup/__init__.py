#!/bin/python3.8
#FastDup Software, (C) copyright 2022 Dr. Amir Alush and Dr. Danny Bickson.
#This software is free for non-commercial and academic usage under the Creative Common Attribution-NonCommercial-NoDerivatives
#4.0 International license. Please reach out to info@databasevisual.com for licensing options.

#__init__.py file wraps the main calls to our c++ engine.


__version__="1.24"
CONTACT_EMAIL="info@visual-layer.com"

import sentry_sdk
from sentry_sdk import capture_exception

import time
import os
import sys
import traceback
import platform
import uuid
import hashlib
from functools import wraps
import subprocess

#get a random token based on the machine uuid
token = hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()
unit_test = None
def find_certifi_path():
    try:
        import certifi
        return os.path.join(os.path.dirname(certifi.__file__), 'cacert.pem')
    except Exception as ex:
        print('Failed to find certifi', ex)
    return None


def traces_sampler(sampling_context):
    # Examine provided context data (including parent decision, if any)
    # along with anything in the global namespace to compute the sample rate
    # or sampling decision for this transaction

    print(sampling_context)
    return 1

def init_sentry():
    global unit_test

    if 'SENTRY_OPT_OUT' not in os.environ:

        if platform.system() == 'Darwin':
            # fix CA certficate issue on latest MAC models
            path = find_certifi_path()
            if path is not None:
                if 'SSL_CERT_FILE' not in os.environ:
                    os.environ["SSL_CERT_FILE"] = path
                if 'REQUESTS_CA_BUNDLE' not in os.environ:
                    os.environ["REQUESTS_CA_BUNDLE"] = path

        sentry_sdk.init(
            dsn="https://b526f209751f4bcea856a1d90e7cf891@o4504135122944000.ingest.sentry.io/4504168616427520",
            debug='SENTRY_DEBUG' in os.environ,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1,
            release=__version__,
            default_integrations=False
        )
        unit_test = 'UNIT_TEST' in os.environ
        try:
            filename = os.path.join(os.environ.get('HOME', '/tmp'),".token")
            if platform.system() == "Windows":
                filename = os.path.join(os.environ.get('USERPROFILE',"c:\\"),".token")
            with open(filename, "w") as f:
                f.write(token)
                #if platform.system() == "Windows":
                #    f.write("\n")
                #    LOCAL_DIR=os.path.dirname(os.path.abspath(__file__))
                #    f.write(LOCAL_DIR)
        except:
            pass

def fastdup_capture_exception(section, e, warn_only=False, extra=""):
    if not warn_only:
        traceback.print_exc()
    if 'SENTRY_OPT_OUT' not in os.environ:
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("section", section)
            scope.set_tag("unit_test", unit_test)
            scope.set_tag("token", token)
            scope.set_tag("platform", platform.platform())
            scope.set_tag("platform.version", platform.version())
            scope.set_tag("python", sys.version.strip().replace("\n", " "))
            scope.set_tag("production", "FASTDUP_PRODUCTION" in os.environ)
            if extra != "":
                scope.set_tag("extra", extra)
            capture_exception(e, scope=scope)


def fastdup_performance_capture(section, start_time):
    if 'SENTRY_OPT_OUT' not in os.environ:
        try:
            # avoid reporting unit tests back to sentry
            if token == '41840345eec72833b7b9928a56260d557ba2a1e06f86d61d5dfe755fa05ade85':
                import random
                if random.random() < 0.995:
                    return
            sentry_sdk.set_tag("runtime", str(time.time()-start_time))

            with sentry_sdk.push_scope() as scope:
                scope.set_tag("section", section)
                scope.set_tag("unit_test", unit_test)
                scope.set_tag("token", token)
                scope.set_tag("runtime-sec", time.time()-start_time)
                scope.set_tag("platform", platform.platform())
                scope.set_tag("platform.version", platform.version())
                scope.set_tag("python", sys.version.strip().replace("\n", " "))
                scope.set_tag("production", "FASTDUP_PRODUCTION" in os.environ)
                sentry_sdk.capture_message("Performance", scope=scope)
        finally:
            sentry_sdk.flush(timeout=5)


def fastdup_capture_log_debug_state(config):
    if 'SENTRY_OPT_OUT' not in os.environ:
        breadcrumb = {'type':'debug', 'category':'setup', 'message':'snapshot', 'level':'info', 'timestamp':time.time() }
        breadcrumb['data'] = config
        #with sentry_sdk.configure_scope() as scope:
        #    scope.clear_breadcrumbs()
        sentry_sdk.add_breadcrumb(breadcrumb)




init_sentry()

LOCAL_DIR=os.path.dirname(os.path.abspath(__file__))
os.environ['FASTDUP_LOCAL_DIR'] = LOCAL_DIR
is_windows = False
is_mac = False
is_linux = False

if platform.system() == "Windows":
    is_windows = True
elif platform.system() == "Darwin":
    is_mac = True
    OSVER="mac"
    OS_SUBVER=subprocess.run(["sw_vers","-productVersion"], capture_output=True, text=True).stdout.strip()
else: #Linux
    is_linux = True
    OSVER=subprocess.run(["lsb_release","-r","-s"], capture_output=True, text=True).stdout.strip()
    if OSVER == "10":
        OSVER=subprocess.run(["cat","/etc/debian_version"], capture_output=True, text=True).stdout.strip()

sys_version = sys.version.replace('\n','')
if is_mac:
    if "3.8" not in sys_version and "3.9" not in sys_version:
        print("fastdup identified you are running on Python " + str(sys_version) + " while on MACOS only python3.8 and python3.9 are supported")
        fastdup_capture_exception("Unsupported MACOS system", RuntimeError("Found unsupported MAC OS system " + str(sys_version)))
    else:
        print(
            "fastdup identified you are running on supported Python using unsupported OS version " + str(OS_SUBVER)
            "We support 10.X to 12.X. Try to upgrade pip using `pip install -U pip` and try again.")
        fastdup_capture_exception("Unsupported MACOS version",
                                  RuntimeError("fastdup identified you are running on supported Python using unsupported OS version " + str(OS_SUBVER) + ", we support 10.X to 12.X please reach out to support"))

elif is_linux:
    if "3.8" not in sys_version and "3.9" not in sys_version and "3.10" not in sys_version and "3.7" not in sys_version:
        print("fastdup identified you are running on Python " + str(sys_version) + " while on Linux only python3.7-python3.10 are supported " + str(OSVER))
        fastdup_capture_exception("Unsupported Linux system", RuntimeError("fastdup identified you are running on Python " + str(sys_version) + " while on Linux only python3.7-python3.10 are supported " + str(OSVER)))
    elif OSVER == "10.12" or OSVER == "7.9.2009":
        print(
            "fastdup supports installation on Centos7, Redhat 4.8, Amazon Linux 2 via the release page (https://github.com/visual-layer/fastdup/releases). "
            "Look for Centos 7 releases. You system is " + str(OSVER))
        fastdup_capture_exception("Unsupported Linux system", RuntimeError(
            "fastdup supports installation on Centos7, Redhat 4.8, Amazon Linux 2 via the release page (https://github.com/visual-layer/fastdup/releases). "
            "Look for Centos 7 releases. You system is " + str(OSVER)))

    else:
        print(
            "fastdup identified you are running unsupported Linux OS version " + str(OS_SUBVER) + ", we support Ubuntu 18-22, Centos7, Redhat 4.8, Amazon Linux 2, python3.7-python3.10. "
            "The later 3 needs to be install via our gihtub release page.")
        fastdup_capture_exception("Unsupported Linux version",
                                  RuntimeError("fastdup identified you are running on supported Python using unsupported OS version " + str(OS_SUBVER) + ", we support 10.X to 12.X please reach out to support"))
