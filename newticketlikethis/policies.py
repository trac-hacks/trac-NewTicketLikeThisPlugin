from trac.config import ListOption
from trac.core import Component, implements
from trac.util.translation import _

from newticketlikethis.interfaces import ITicketCloner

class SimpleTicketCloner(Component):
    """
    A simple ITicketCloner with no configurability.  It clones
    all fields from the original ticket with their precise values,
    except for the summary and description, which are modified
    slightly to indicate what ticket they were cloned from.

    This mimics the behavior of the core tracopt.ticket.clone module.
    """
    implements(ITicketCloner)
    
    def build_clone_form(self, req, ticket, data):
        fields = {}
        for f in data.get('fields', []):
            name = f['name']
            if name == 'summary':
                fields['summary'] = _("%(summary)s (cloned)",
                                      summary=ticket['summary'])
            elif name == 'description':
                fields['description'] = \
                    _("Cloned from #%(id)s:\n----\n%(description)s",
                      id=ticket.id, description=ticket['description'])
            else:
                fields[name] = ticket[name]
        return fields

class ExcludedFieldsTicketCloner(Component):
    """
    An ITicketCloner implementation that will exclude certain fields
    from the original ticket when building a clone.  

    The list of fields to exclude can be configured with in trac.ini
    with the ``[newticketlikethis] excluded_fields`` option.

    By default, no fields are excluded.
    """

    implements(ITicketCloner)
    
    excluded_fields = ListOption('newticketlikethis', 'excluded_fields')

    def build_clone_form(self, req, ticket, data):
        fields_to_exclude = self.excluded_fields or []

        fields = {}
        for f in data.get('fields', []):
            name = f['name']
            if name not in fields_to_exclude:
                fields[name] = ticket[name]
        return fields
