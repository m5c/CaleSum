from unittest import TestCase

from calendar_intel.event_parser import extract_time_zone_if_present, \
    scheduled_to_start_stop_strings, strip_time_zone


class Test(TestCase):

    # "Scheduled: Oct 9, 2023 at 2:00 AM to Oct 10, 2023 at 2:15 AM, EDT"

    def test_same_day_with_timezone(self):
        test_string: str = "Scheduled: Aug 28, 2023 at 7:15 AM to 7:45 AM, EDT"

        # test time zone extraction
        self.assertEqual(extract_time_zone_if_present(test_string), "EDT")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), "EDT"),
                          "Aug 28, 2023 at 7:15 AM to 7:45 AM")

    def test_same_day_without_timezone(self):
        test_string: str = "Scheduled: Nov 6, 2023 to Nov 7, 2023"
        self.assertEqual(extract_time_zone_if_present(test_string), "")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), ""),
                          "Nov 6, 2023 to Nov 7, 2023")

    def test_other_day_with_timezone(self):
        test_string: str = "Scheduled: Nov 5, 2023 at 12:00 PM to Nov 7, 2023 at 1:00 PM, EST"
        self.assertEqual(extract_time_zone_if_present(test_string), "EST")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), "EST"),
                          "Nov 5, 2023 at 12:00 PM to Nov 7, 2023 at 1:00 PM")

    def test_same_day_with_plusminus_timezone(self):
        test_string: str = "Scheduled: Oct 12, 2023 at 10:15 AM to 11:15 AM, GMT-4"
        self.assertEqual(extract_time_zone_if_present(test_string), "GMT-4")

        # test range construction
        self.assertEqual(strip_time_zone(test_string.replace('Scheduled: ', ''), "GMT-4"),
                          "Oct 12, 2023 at 10:15 AM to 11:15 AM")
