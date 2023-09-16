from unittest import TestCase

from calendar_intel.event_parser import extract_time_zone_if_present, \
    strip_time_zone, range_without_timezone_to_start_stop_strings


class Test(TestCase):

    def test_same_day_with_timezone(self):
        test_string: str = "Scheduled: Aug 28, 2023 at 7:15 AM to 7:45 AM, EDT"

        # test time zone extraction
        self.assertEqual(extract_time_zone_if_present(test_string), "EDT")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), "EDT"),
                         "Aug 28, 2023 at 7:15 AM to 7:45 AM")

        # test extraction of start and stop datestamps
        parsed_string: dict = range_without_timezone_to_start_stop_strings(
            "Aug 28, 2023 at 7:15 AM to 7:45 AM")
        self.assertEqual(parsed_string['start'], "Aug 28, 2023 at 7:15 AM")
        self.assertEqual(parsed_string['stop'], "Aug 28, 2023 at 7:45 AM")
        self.assertEqual(parsed_string['all_day'], False)
        self.assertEqual(parsed_string['multi_day'], False)


    def test_same_day_without_timezone(self):
        test_string: str = "Scheduled: Nov 6, 2023 to Nov 7, 2023"
        self.assertEqual(extract_time_zone_if_present(test_string), "")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), ""),
                         "Nov 6, 2023 to Nov 7, 2023")

        # test extraction of start and stop datestamps
        parsed_string: dict = range_without_timezone_to_start_stop_strings(
            "Nov 6, 2023 to Nov 7, 2023")
        self.assertEqual(parsed_string['start'], "Nov 6, 2023 at 0:00 AM")
        self.assertEqual(parsed_string['stop'], "Nov 7, 2023 at 11:59 PM")
        self.assertEqual(parsed_string['all_day'], True)
        self.assertEqual(parsed_string['multi_day'], True)

    def test_other_day_with_timezone(self):
        test_string: str = "Scheduled: Nov 5, 2023 at 12:00 PM to Nov 7, 2023 at 1:00 PM, EST"
        self.assertEqual(extract_time_zone_if_present(test_string), "EST")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), "EST"),
                         "Nov 5, 2023 at 12:00 PM to Nov 7, 2023 at 1:00 PM")

        # test extraction of start and stop datestamps
        parsed_string: dict = range_without_timezone_to_start_stop_strings(
            "Nov 5, 2023 at 12:00 PM to Nov 7, 2023 at 1:00 PM")
        self.assertEqual(parsed_string['start'], "Nov 5, 2023 at 12:00 PM")
        self.assertEqual(parsed_string['stop'], "Nov 7, 2023 at 1:00 PM")
        self.assertEqual(parsed_string['all_day'], False)
        self.assertEqual(parsed_string['multi_day'], True)

    def test_same_day_with_plusminus_timezone(self):
        test_string: str = "Scheduled: Oct 12, 2023 at 10:15 AM to 11:15 AM, GMT-4"
        self.assertEqual(extract_time_zone_if_present(test_string), "GMT-4")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), "GMT-4"),
                         "Oct 12, 2023 at 10:15 AM to 11:15 AM")

        # test extraction of start and stop datestamps
        parsed_string: dict = range_without_timezone_to_start_stop_strings(
            "Oct 12, 2023 at 10:15 AM to 11:15 AM")
        self.assertEqual(parsed_string['start'], "Oct 12, 2023 at 10:15 AM")
        self.assertEqual(parsed_string['stop'], "Oct 12, 2023 at 11:15 AM")
        self.assertEqual(parsed_string['all_day'], False)
        self.assertEqual(parsed_string['multi_day'], False)

    def test_single_all_day(self):
        test_string: str = "Scheduled: Oct 12, 2023"
        self.assertEqual(extract_time_zone_if_present(test_string), "")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), ""),
                         "Oct 12, 2023")

        # test extraction of start and stop datestamps
        parsed_string: dict = range_without_timezone_to_start_stop_strings(
            "Oct 12, 2023")
        self.assertEqual(parsed_string['start'], "Oct 12, 2023 at 0:00 AM")
        self.assertEqual(parsed_string['stop'], "Oct 12, 2023 at 11:59 PM")
        self.assertEqual(parsed_string['all_day'], True)
        self.assertEqual(parsed_string['multi_day'], False)
