from cubicweb_web.devtools.testlib import AutomaticWebTest
from logilab.common.testlib import unittest_main


class AutomaticWebTest(AutomaticWebTest):
    no_auto_populate = ("Keyword", "CodeKeyword")
    ignored_relations = {"descendant_of"}

    def to_test_etypes(self):
        # only test the cube related entities
        return {"Classification", "Keyword", "CodeKeyword"}

    def list_startup_views(self):
        return ()


if __name__ == "__main__":
    unittest_main()
