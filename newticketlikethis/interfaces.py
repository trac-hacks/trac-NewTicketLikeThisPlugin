from trac.core import Interface

class ITicketCloner(Interface):
    """ 
    Extension point interface for components that determine
    how to create a new "cloned" ticket from an existing ticket.
    """

    def build_clone_form(req, ticket, data):
        """
        Given a ticket to clone, return a dictionary of fields
        and their values that should be present in the new ticket.
        """

    def get_clone_form_action(req, ticket, data):
        """
        Given a ticket to clone, return a URL to submit the form to.
        """
