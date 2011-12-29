= Create new tickets based on existing tickets =

== Description ==

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

* ``ExcludedFieldsTicketCloner`` clones all fields from the original ticket
  with no modifications.  It can also ignore certain fields entirely,
  based on a configuration setting, which will force the new ticket to be
  generated with the system's default values (or no values) for the fields
  that were excluded.

More complex policies might implement custom logic for deriving new ticket
values based on the values of the existing ticket's fields, or use
alternate cloning policies based on the ticket's type.

== Configuration ==

To use the plugin, install it in your Trac environment and enable its 
components in ``trac.ini``:

{{{ 
[components]
newticketlikethis.* = enabled
}}}

By default this will add the "Clone" button to the ticket view, and 
will use the ``SimpleTicketCloner`` component to clone your tickets.
The ``TICKET_ADMIN`` permission will be required for cloning tickets.

=== Choosing a policy ===

To use a different ticket-cloning policy, make sure to enable any
necessary components and then set the ``newticketlikethis.ticket_cloner``
option in ``trac.ini`` to reference the component's name like so:

{{{
[newticketlikethis]
ticket_cloner = ExcludedFieldsTicketCloner
}}}

=== Configuring permissions ===

By default the "Clone" button only appears if the user has the 
``TICKET_ADMIN`` permission.  You can change the required permission
using the ``newticketlikethis.ticket_clone_permission`` option:

{{{
[newticketlikethis]
ticket_clone_permission = TICKET_CREATE
}}}


=== ExcludedFieldsTicketCloner ===

If enabled, the ``ExcludedFieldsTicketCloner`` will look for an additional
configuration option ``newticketlikethis.excluded_fields`` to determine
which fields to exclude.  This should be a comma-separated list of ticket
fields.  By default, no fields are excluded. For example, you might use
a ``trac.ini`` configuration like:

{{{
[newticketlikethis]
ticket_cloner = ExcludedFieldsTicketCloner
excluded_fields = description, summary, reporter
}}}

== Customization ==

It is easy to implement your own custom policies as well.  Look at 
the code in ``newticketlikethis.policies`` for inspiration.

If you implement a custom policy that you would like to share, 
feel free to submit it as a patch, so that the ``NewTicketLikeThisPlugin``
can ship with a strong library of reusable cloning policies.
