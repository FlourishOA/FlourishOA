import django.test.testcases as testcases


class TestSearchView(testcases.TestCase):

    def test_call_search_view_loads(self):
        response = self.client.get("/search")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main_site/search.html")