from unittest import TestCase
from django.urls import resolve
from django.urls.exceptions import Resolver404
from maths.views import add, sub, mul, div, math, maths_list, math_details, results_list


class TestUrls(TestCase):
    def test_resolution_for_add(self):
        resolver = resolve('/maths/add/1/2')
        self.assertEqual(resolver.func, add)

    def test_resolution_for_sub(self):
        resolver = resolve('/maths/sub/1/2')
        self.assertEqual(resolver.func, sub)

    def test_resolution_for_mul(self):
        resolver = resolve('/maths/mul/1/2')
        self.assertEqual(resolver.func, mul)

    def test_resolution_for_div(self):
        resolver = resolve('/maths/div/1/2')
        self.assertEqual(resolver.func, div)

    def test_resolution_for_math(self):
        resolver = resolve('/maths/')
        self.assertEqual(resolver.func, math)

    def test_resolution_for_list(self):
        resolver = resolve('/maths/histories/')
        self.assertEqual(resolver.func, maths_list)

    def test_resolution_for_details(self):
        resolver = resolve('/maths/histories/1')
        self.assertEqual(resolver.func, math_details)

    def test_resolution_for_results(self):
        resolver = resolve('/maths/results/')
        self.assertEqual(resolver.func, results_list)

    def test_arguments_should_be_integers_or_404(self):
        with self.assertRaises(Resolver404):
            resolve('maths/sub/a/b')