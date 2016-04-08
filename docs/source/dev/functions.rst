Functions
=========

This document provides detailed information on how to add new functions to
pywincffi.  It's not overly difficult however it's good to be consistent about
it.

Naming Conventions
------------------

Martin Fowler once said, "There are only two hard things in Computer
Science: cache invalidation and naming things.".  This section covers how
the project expects to handle naming conventions with regards to functions.

Function Definition
~~~~~~~~~~~~~~~~~~~

The function definition should match the MSDN documentation.
So for example if you're implementing a function called `WaitForSingleObject`
then it should be defined as:

.. code-block:: python

   def WaitForSingleObject():
       pass

If you're implementing a utility function or something that's not supposed to
directly map to a specific Windows function then use
`PEP8 conventions <https://www.python.org/dev/peps/pep-0008/#function-names>`_
instead:

.. code-block:: python

   def convert_input():
       pass


Arguments and Keywords
~~~~~~~~~~~~~~~~~~~~~~

If an argument or keyword is intended to be an analog for an argument to
a Windows API call then it should follow the same naming convention as
the documented function does. The `WaitForSingleObject` function for example
takes two arguments according to the MSDN documentation which when translated
to Python would look like this:

.. code-block:: python

   def WaitForSingleObject(hHandle, dwMilliseconds):
       pass

Any argument or keyword which is not directly related to an input to a Windows
API should instead use the standard PEP8 naming conventions:

.. code-block:: python

   def WaitForSingleObject(hHandle, dwMilliseconds, other_keyword=None):
       pass


Internal Variables
~~~~~~~~~~~~~~~~~~

Like arguments or keywords variables should be named either using `camelCase`
if they're intended to map to a value passed in or used by a Windows API
call or using the `name_with_underscores` convention like PEP8 says.  Here's
an example of the two (see the inline comments below):

.. code-block:: python

   def UnlockFileEx(...):

        # internal variables
        ffi, library = dist.load()

        # lpOverlapped is a Windows structure
        if lpOverlapped is None:
            lpOverlapped = ffi.new("OVERLAPPED[]", [{"hEvent": hFile}])


Documentation
-------------

This section covers the basics of documenting functions in pywincffi.  The
below mostly applies to how we document Windows functions but it can generally
apply elsewhere in the project too.

Basic Layout
~~~~~~~~~~~~

The layout of the documentation string for each function should be consistent
throughout the project.  This generally makes it easier to understand but also
harder to miss more critical information.  Below is an annotated example
of a Windows function

.. code-block:: python

   def AWindowsFunction(...):
       """
       First few sentences should tell someone what AWindowsFunction
       does.  This can usually be pulled from the MSDN documentation but
       is usually shorter and more concise.

       .. seealso::

          <url pointing to the msdn reference for AWindowsFunction>
          <url pointing to a use case or other usefull information>

       :param <python type> variable_name:
           Some information about what variable_name is.  Again, can be pulled
           from the msdn documentation but should be concise as someone can
           always go read the msdn documentation.

       <additional keyword or argument documentation>

       :raises SomeException:
           Information about under what condition(s) SomeException may be
           raised.  SomeException should be something that's raised directly
           by AWindowsFunction.

       :returns:
           Some information about the return value.  This part of the
           documentation should be excluded if the function does not
           return anything.
       """




Arguments and Keywords
~~~~~~~~~~~~~~~~~~~~~~

Position arguments should be documented using ``:param <type> argument:``
while keywords should be documented using ``:keyword <type> keyword:``.  The
``<type>`` is referring to the Python type rather than the Windows type which
the argument may be an analog for.  Here's a simplified example:

.. code-block:: python

   def CreateFile(lpFileName, dwDesiredAccess, dwShareMode=None ...):
       """
       :param str lpFileName:

       :param int dwDesiredAccess:

       :keyword int dwShareMode:
       """

It's possible to allow an input argument to support multiple types as well:

.. code-block:: python

   def foobar(arg1):
       """
       :type arg1: int or str
       :param arg1:
       """

If the argument or keyword you are documenting requires some additional setup,
such initializing a struct, it can be helpful to include a real example:

.. code-block:: python

   def CreatePipe(lpPipeAttribute=None):
       """
       ...

       :keyword struct lpPipeAttributes:
           The security attributes to apply to the handle. By default
           ``NULL`` will be passed in meaning then handle we create
           cannot be inherited.  Example struct:

           >>> from pywincffi.core import dist
           >>> ffi, library = dist.load()
           >>> lpPipeAttributes = ffi.new(
           ...     "SECURITY_ATTRIBUTES[1]", [{
           ...     "nLength": ffi.sizeof("SECURITY_ATTRIBUTES"),
           ...     "bInheritHandle": True,
           ...     "lpSecurityDescriptor": ffi.NULL
           ...     }]
           ... )
       """


External References
~~~~~~~~~~~~~~~~~~~

External references, such as those referencing the msdn documentation, are
usually included within a ``.. seealso::`` block.  For msdn documentation,
it's preferable to use one the following url structure:

.. code-block:: rst

   .. seealso::

      https://msdn.microsoft.com/library/<article_number>
      https://msdn.microsoft.com/en-us/library/<article_number>


Handling Input
--------------

One of the main goals of pywincffi is to provide are more Python like interface
for calling Windows APIs.  To do this the pywincffi functions implement type
checking, conversion and argument handling so less work is necessary on the
consumer's part.

Type Checking
~~~~~~~~~~~~~

In order to provide better error messages and more consistent expectations of
input arguments each function should perform type checking on each
argument.  Most type checks are run using the
:func:`pywincffi.core.checks.input_check` function:

.. code-block:: python

   from six import integer_types
   from pywincffi.core.checks import input_check

   def Foobar(arg1, arg2):
       input_check("arg1", arg1, integer_types)
       input_check("arg1", arg2, allowed_values=(1, 2, 3))

If :func:`pywincffi.core.checks.input_check` does not do what you need or
you have to perform multiple steps to validate an input argument you raise
the :class:`pywincffi.exceptions.InputError` exception yourself.  Note, there
also some enums to help with special cases too.  See the code in the
:mod:`pywincffi.core.checks` module for more detailed information.


Type Conversion
~~~~~~~~~~~~~~~

The underlying library that pywincffi uses, cffi, can do most type conversions
for you.  While normally this will function as you'd expect it's better to be
explicit and handle the conversion yourself so there are fewer surprises.

Here's an example of how an 'automatic' conversion would look:

.. code-block:: python

   library.LockFileEx(hFile, 0, 0, 0, 0, lpOverlapped)

In the above example the integers being passed into the function call would
have been provided by as arguments to a function wrapping library.LockFileEx.
The problem with this is if the calls to :func:`input_check` are wrong or we
miss something then the user can end up with exceptions when the underlying
LockFileEx function is executed.  By doing the type conversion before calling
the function any last second problems are easier to diagnose because they'll
happen higher up in the stack:

.. code-block:: python

   library.LockFileEx(
      hFile,
      ffi.cast("DWORD", 0),
      ffi.cast("DWORD", 0),
      ffi.cast("DWORD", 0),
      ffi.cast("DWORD", 0),
      lpOverlapped
   )


Keywords
~~~~~~~~
**TODO**: When to use something=None (like for ffi.NULL)


Keywords with Defaults
~~~~~~~~~~~~~~~~~~~~~~




Handling Output
---------------

Windows API Error Checking
~~~~~~~~~~~~~~~~~~~~~~~~~~

Function Return Values
~~~~~~~~~~~~~~~~~~~~~~

**TODO**: namedtuples (especially for structs [optional?]) otherwise the user has to do it

Windows Constants
-----------------

Adding New Constants
~~~~~~~~~~~~~~~~~~~~
**TODO**: when to add new constants

Using Existing Constants
~~~~~~~~~~~~~~~~~~~~~~~~
