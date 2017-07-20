#  Copyright (C) 2017, Jaguar Land Rover
#
#  This program is licensed under the terms and conditions of the
#  Mozilla Public License, version 2.0.  The full text of the
#  Mozilla Public License is at https://www.mozilla.org/MPL/2.0/
#

import vsi_py as vsi

# an arbitrary group number (alphabet positions for 'vsm') to reduce the
# risk of conflicts with other VSI group numbers
GROUPNUM = 221913

# default domain
DOMAIN = 1

# TODO: inline these into the various docstrings
# The module public interface consists of the following functions:
#
# send    - Function to send signal.
#           It takes signal ID and value as arguments.
#
# receive - Function to receive signal.
#           It returns the received message as a [(ID, Value)].
# TODO: document set_signal_number_map

# Establish a signal group to allow listening only to the specific signals which
# concern us. Otherwise, we would monitor up to tens of thousands of signals (as
# measured in real-world scenarios).

# delete this group before creating it to reset it to an empty state
status = vsi.deleteSignalGroup(GROUPNUM)
status = vsi.createSignalGroup(GROUPNUM)

signal_to_number = {}
number_to_signal = {}

def set_signal_number_map(new_signal_to_number):
    global signal_to_number
    global number_to_signal
    signal_to_number = new_signal_to_number
    # NOTE: this assumes the signal numbers are unique (which they should be)
    number_to_signal = {v: k for k, v in signal_to_number.items()}

    for signum in signal_to_number.values():
        # TODO: look this up? Or just get it from the map passed in above
        name = ""

        status = vsi.addSignalToGroup(DOMAIN, signum, name, GROUPNUM)
        # TODO: check status value; non-zero indicates error

def send(signal_name, value):
    # TODO: handle cases where it's missing
    signal_id = signal_to_number[signal_name]

    # FIXME: decide when to parse `value` as int instead of string
    # FIXME: just pass in zero when there's a string value
    # FIXME: pass in the value as the last argument; currently passing in an
    # artificial value since VSI only allows ints
    value_int = 127
    value_str = value

    # TODO: for int values, set this to sizeof(unsigned long) -- 4?
    value_size = len(value_str)

    # VSI call to insert (send) signal.
    status = vsi.insertSignalData(DOMAIN, signal_id, signal_name, value_size,
            value_int, value_str)

def receive():
    # This function should use the new functions with group support to monitor
    # group of signals.

    # TODO: cut -- this works if all the data needed is already in place but
    # that won't always be true; should block (see below) to match the behavior
    # for ZeroMQ
    #
    # get the latest (signal, value) among our watched signals without waiting
    # if none is available
    results = vsi.getOldestInGroup(GROUPNUM, False)

    # TODO: this should be our behavior (to match ZeroMQ) but, as of this
    # writing, it deadlocks AND puts the DB in a bad state (where it will always
    # deadlock even if reading the oldest in the group WITHOUT blocking)
    """
    # get the latest (signal, value) among our watched signals
    # wait if none exist
    results = vsi.getOldestInGroup(GROUPNUM, True)
    """

    if type(results) is not list or len(results) < 1:
        return None

    # TODO: in a new "teardown" method, try to delete the signal group just to
    # clean up after ourselves

    result_tuples = []
    for result in results:
        # TODO: handle the case this key has no entry
        signal = number_to_signal[result["signal"]]
        result_tuples.append((signal, result["value"]))

    return result_tuples
