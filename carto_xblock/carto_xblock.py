"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from xblock.core import XBlock
from xblock.fragment import Fragment
from xblock.fields import Scope, String
from webob.response import Response


class CartoXBlock(XBlock):
    """
    XBlock holding an iframe showing a CartoDB map
    """
    display_name = String(
        display_name="Display Name",
        default="Carto XBlock",
        scope=Scope.settings
    )

    embed_url = String(
        display_name="Embed URL",
        default="https://exteng.carto.com/u/exteng-admin/builder/4105204d-e3b2-49cf-8386-4c0a5573f2a0/embed?state=%7B%22map%22%3A%7B%22center%22%3A%5B8.952036908213827%2C-79.53629493713379%5D%2C%22zoom%22%3A17%7D%7D",
        scope=Scope.settings
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the TimelineXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/carto.html")
        frag = Fragment(html.format(
            self=self,
            embed_url=self.embed_url))
        frag.add_css_url(
            self.runtime.local_resource_url(
                self, 'public/css/carto_xblock.css'))
        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        html_str = pkg_resources.resource_string(__name__, "static/html/carto_edit.html")
        frag = Fragment(unicode(html_str).format(
            display_name=self.display_name,
            thumbnail_url=self.thumbnail_url,
            display_description=self.display_description,
            embed_url=self.embed_url
        ))
        js_str = pkg_resources.resource_string(__name__, "public/js/carto_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('StudioEdit')

        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        data = request.POST
        self.display_name = data['display_name']
        self.display_description = data['display_description']
        self.thumbnail_url = data['thumbnail']

        return Response(json_body={'result': 'success'})

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CartoXBlock",
             """<carto_xblock/>
             """)
        ]
