from django.test import TestCase
from testlibrary.models import *
from django.utils import timezone

class TestRunTestCase(TestCase):
	def setUp(self):
		Case.objects.create(title='UT_Case')

	def test_test_run_created(self):
		testrun = TestRun()
		testrun.start_date = timezone.now()
		testrun.end_date = timezone.now()
		testrun.save()
		testrun.test_cases.add(Case.objects.first())
		testrun.save()
		testrun.CreateResults()
		print(TestResult.objects.filter(test_run=testrun.pk))