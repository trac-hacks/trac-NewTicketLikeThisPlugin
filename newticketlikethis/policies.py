from genshi.template.text import NewTextTemplate
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

class DerivedFieldsTicketCloner(Component):
    """
    An ITicketCloner implementation that allows you to exclude certain 
    fields from the original ticket when building a clone, and derive
    other fields from the original ticket using Genshi templates.

    The list of fields to exclude and to derive can be configured with::

    [newticketlikethis]
    excluded_fields = description, component, reporter, owner
    derived_fields = hardcoded string->summary, $ticket.id->original_ticket_id, $ticket.component $ticket.reporter->keywords, $ticket.reporter $ticket.owner->cc

    By default, no fields are excluded, and no fields are derived; 
    all fields are copied verbatim.

    If a field is specified in both excluded_fields and derived_fields,
    the excluded_fields configuration takes precedence.
    """

    implements(ITicketCloner)
    
    excluded_fields = ListOption('newticketlikethis', 'excluded_fields')
    derived_fields = ListOption('newticketlikethis', 'derived_fields')

    def build_clone_form(self, req, ticket, data):
        fields = {}
        for derivation in self.derived_fields:
            template, new_field = derivation.split('->')
            if new_field in self.excluded_fields:
                continue
            template = NewTextTemplate(template.replace("\\n", "\n").encode('utf8'))
            fields[new_field] = template.generate(ticket=ticket).render('text', encoding=None).strip()

        for f in data.get('fields', []):
            name = f['name']
            if name in fields:
                continue
            if name not in self.excluded_fields:
                fields[name] = ticket[name]
        return fields

