from django.test import TestCase
from maths.models import Result
from maths.forms import ResultForm


class ResultFormTest(TestCase):

    def test_result_save_correct_data(self):
        data = {"value": 200}
        form = ResultForm(data=data)
        self.assertTrue(form.is_valid())
        r = form.save()
        self.assertIsInstance(r, Result)
        self.assertEqual(r.value, 200)