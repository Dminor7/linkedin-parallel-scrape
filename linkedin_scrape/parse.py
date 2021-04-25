import parslepy
import lxml.etree

class Parse:

    def recursive_extract(self, html, template):
        """For given html content and template recursively parse and returns the result

        Args:
            html 
            template

        Returns:
            data
        """
        data = None
        html_parser = lxml.etree.HTMLParser()
        doc = lxml.etree.fromstring(html, parser=html_parser)
        p = parslepy.Parselet(template)
        data = p.extract(doc)
        return data