from django.test import TestCase
from maths.models import Result
from maths.forms import ResultForm


class ResultFormTest(TestCase):

    def DataBaseObjectsNumber(self):
        self.assertEqual(len(Result.objects.all()), 0)

    def DataBaseObjectsId(self, x):
        self.assertEqual(x.id, 1)

    def test_result_save_correct_data_value(self):
        data = {'value': 200}
        self.DataBaseObjectsNumber()
        form = ResultForm(data=data)
        self.assertTrue(form.is_valid())
        r = form.save()
        self.assertIsInstance(r, Result)
        self.assertEqual(r.value, 200)
        self.DataBaseObjectsId(r)
        self.assertEqual(r.error, None)

    def test_result_save_correct_data_error(self):
        data = {'error': 'Test'}
        self.DataBaseObjectsNumber()
        form = ResultForm(data=data)
        self.assertTrue(form.is_valid())
        r = form.save()
        self.assertIsInstance(r, Result)
        self.assertEqual(r.error, 'Test')
        self.DataBaseObjectsId(r)
        self.assertEqual(r.value, None)

    def test_result_save_correct_data_error_value(self):
        data = {'value': 200, 'error': 'Test'}
        self.DataBaseObjectsNumber()
        form = ResultForm(data=data)
        self.assertFalse(form.is_valid())