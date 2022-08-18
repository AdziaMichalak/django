from django.test import TestCase
from maths.models import Math, Result


class MathModelTest(TestCase):
    def setUp(self):
        Math.objects.create(operation='add', a=1, b=2)
        Math.objects.create(operation="sub", a=3, b=4)
        Math.objects.create(operation="mul", a=5, b=6)
        Math.objects.create(operation="div", a=7, b=8)

    def test_math_str(self):
        m1 = Math.objects.get(operation='add')
        m2 = Math.objects.get(operation='sub')
        m3 = Math.objects.get(operation='mul')
        m4 = Math.objects.get(operation='div')

        self.assertEqual(str(m1), 'id:1, a=1, b=2, op=add')
        self.assertEqual(str(m2), 'id:2, a=3, b=4, op=sub')
        self.assertEqual(str(m3), 'id:3, a=5, b=6, op=mul')
        self.assertEqual(str(m4), 'id:4, a=7, b=8, op=div')


class ResultModelTest(TestCase):
    def setUp(self):
        Result.objects.create(value=10)
        Result.objects.create(error='0 division error!')

    def test_result_str(self):
        r1 = Result.objects.get(value=10)
        r2 = Result.objects.get(error='0 division error!')

        self.assertEqual(str(r1), 'value: 10.0 | error: None')
        self.assertEqual(str(r2), 'value: None | error: 0 division error!')