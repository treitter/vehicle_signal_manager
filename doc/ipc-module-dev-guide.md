Introduction
=============
IPC modules redirect VSM signal I/O through another transport. This can support,
for example, logging signal emissions to a database or routing signals to other
processes for them to act upon.

Module Requirements
===================
For this prototype version of VSM, all IPC modules must either be written in
Python or provide Python bindings with the following interfaces.

Required Methods
----------------
`send(signal_name, value)`:
This method propagates a signal with the name `signal_name` and value `value`.
The type for `value` depends upon the value type of the signal itself and thus
can be a `str`, an `int`, or other type.

This method returns `None`.

`receive()`:
Returns a `[(signal_name, value)]`. That is, a `list` of
`(str, <variable type>)` tuples. As with `send()`, the type of each `value`
depends upon the signal it corresponds to.

This return type allows the IPC module to return any number of (signal, value)
pairs as needed. This is particularly important for transports such as VSI which
always have the potential to return multiple (signal, value) pairs at once.
Thus, the IPC module can avoid needing to buffer results.

Optional Methods
----------------
`set_signal_number_map(new_signal_to_number)`:
If the module depends upon signal IDs (not just signal names), this method can
be created to set the mapping between signal names and their IDs.

The argument is a `dict` of `str` to `int` and the method returns `None`.
