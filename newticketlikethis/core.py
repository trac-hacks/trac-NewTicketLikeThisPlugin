"""
NewTicketLikeThisPlugin:
a plugin for Trac
http://trac.edgewall.org
"""

from genshi.builder import tag
from genshi.filters import Transformer

from trac.config import ExtensionOption
from trac.core import Component, Interface, implements
from trac.web.api import ITemplateStreamFilter
from trac.util.translation import _

from newticketlikethis.interfaces import ITicketCloner

class NewTicketLikeThisPlugin(Component):

    implements(ITemplateStreamFilter)

    ticket_cloner = ExtensionOption('newticketlikethis', 'ticket_cloner',
                                    ITicketCloner,
                                    'SimpleTicketCloner',
                                    """Name of the component implementing `ITicketCloner`, which provides the logic for building a new ticket from an existing one.""")
    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if filename == 'ticket.html':
            ticket = data.get('ticket')
            if ticket and ticket.exists and \
                    'TICKET_ADMIN' in req.perm(ticket.resource):
                filter = Transformer('//h3[@id="comment:description"]')
                stream |= filter.after(self._clone_form(req, ticket, data))
        return stream

    def _clone_form(self, req, ticket, data):
        fields = self.ticket_cloner.build_clone_form(req, ticket, data)

        return tag.form(
            tag.div(
                tag.input(type="submit", name="clone", value=_("Clone"),
                          title=_("Create a copy of this ticket")),
                [tag.input(type="hidden", name='field_' + n, value=v)
                 for n, v in fields.iteritems()],
                tag.input(type="hidden", name='preview', value=''),
                class_="inlinebuttons"),
            method="post", action=req.href.newticket())
