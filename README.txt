Create new tickets based on existing tickets
============================================

Description
-----------

The NewTicketLikeThisPlugin adds a "Clone" button to existing tickets,
which lets you create a new ticket whose fields derive from the original
ticket if you have the appropriate permission.

It is based on the tracopt.ticket.clone.ticketclonebutton extension that
ships with Trac core.  Unlike that extension, the NewTicketLikeThisPlugin
defines and consumes a pluggable interface for implementing custom policies
to determine the way in which a new ticket is derived from the original.
This allows flexible, customized business logic to be provided based on
the needs and workflows of your team.  Also, the NewTicketLikeThisPlugin
allows you to configure the permission required to clone a ticket, whereas
the core ``ticketclonebutton`` hard-codes the TICKET_ADMIN permission.

Two policies are provided by default, in the ``newticketlikethis.policies`` 
module:

* ``SimpleTicketCloner`` mimics the behavior of the 
  ``core tracopt.ticket.clone.ticketclonebutton`` extension: all fields
  from the original ticket are cloned, and the "summary" and "description"
  fields are modified to denote the ticket that they were cloned from.

* ``DerivedFieldsTicketCloner`` can ignore certain fields entirely
  based on a configuration setting; can derive new field values from
  the old ticket using Genshi templates, also through configuration;
  and clones all remaining fields from the original ticket verbatim.

More complex policies might implement custom logic for deriving new ticket
values based on the values of the existing ticket's fields, or use
alternate cloning policies based on the ticket's type.

Configuration
-------------

To use the plugin, install it in your Trac environment and enable its 
components in ``trac.ini``::

  [components]
  newticketlikethis.* = enabled

By default this will add the "Clone" button to the ticket view, and 
will use the ``SimpleTicketCloner`` component to clone your tickets.
The ``TICKET_ADMIN`` permission will be required for cloning tickets.

Choosing a policy
~~~~~~~~~~~~~~~~~

To use a different ticket-cloning policy, make sure to enable any
necessary components and then set the ``newticketlikethis.ticket_cloner``
option in ``trac.ini`` to reference the component's name like so::

  [newticketlikethis]
  ticket_cloner = ExcludedFieldsTicketCloner


Using an alternate form handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default the "Clone" button will submit a POST request to the current
Trac environment's /newticket handler.  You can specify an alternate form
submission (such as a different Trac instance's /newticket handler) with::

  [newticketlikethis]
  ticket_clone_form_action = http://trac.example.com/main/newticket
  ticket_clone_form_method = GET

Either or both of these options may be omitted.


Configuring permissions
~~~~~~~~~~~~~~~~~~~~~~~

By default the "Clone" button only appears if the user has the 
``TICKET_ADMIN`` permission.  You can change the required permission
using the ``newticketlikethis.ticket_clone_permission`` option::

  [newticketlikethis]
  ticket_clone_permission = TICKET_CREATE



DerivedFieldsTicketCloner
~~~~~~~~~~~~~~~~~~~~~~~~~~

If enabled, the ``DerivedFieldsTicketCloner`` will look for an additional
configuration option ``newticketlikethis.excluded_fields`` to determine
which fields to exclude.  This should be a comma-separated list of ticket
fields.  By default, no fields are excluded. 

It will also look for an option ``newticketlikethis.derived_fields`` to 
determine how to derive new field values from the existing ticket.  This
should be a comma-separated list of Genshi templates mapped to new field
values.

For example, you might use a ``trac.ini`` configuration like::

  [newticketlikethis]
  ticket_cloner = DerivedFieldsTicketCloner
  excluded_fields = description, summary, reporter
  derived_fields = $ticket.reporter->cc, milestone:$ticket.milestone component:$ticket.component->keywords

This would allow you to create cloned tickets with the old ticket's reporter CCed; 
the old ticket's milestone and component namespaced and set as keywords on the new
ticket; the new ticket's description, summary and reporter left blank; and all other
fields from the old ticket transferred verbatim to the new ticket.


Customization
-------------

It is easy to implement your own custom policies as well.  Look at 
the code in ``newticketlikethis.policies`` for inspiration.

If you implement a custom policy that you would like to share, 
feel free to submit it as a patch, so that the ``NewTicketLikeThisPlugin``
can ship with a strong library of reusable cloning policies.
