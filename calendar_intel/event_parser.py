"""
Helper module for the actual event parsing.
Date is interpreted using this library:
https://stackoverflow.com/questions/13258554/convert-unknown-format-strings-to-datetime-objects
"""

import re

from calendar_intel.event import Event


def parse_calendar_paste(pasted_raw_event_string: str) -> None:
    print("Making sense of pasted String...")

    # Split long string into individual event strings
    events_as_strings: [str] = separate_string_by_event(pasted_raw_event_string)
    print(events_as_strings)

    # Create event objects out of strings
    if len(events_as_strings) > 0:
        parse_single_event_string(events_as_strings[0])

    # Use this library... https://stackoverflow.com/questions/13258554/convert-unknown-format
    # -strings-to-datetime-objects


def parse_single_event_string(event_string: str) -> Event:
    """
    Converts a single textual event string to a corresponding event object
    :param event_string: as multiple lines of text describing a single string. First line must be
    title, second must start with 'Scheduled' keyword and list a time range.
    :return: Event object representing the parsed textual information.
    """
    title: str = event_string.splitlines()[0]
    # Remove prefix from time range description
    range: [str] = scheduled_to_start_stop_strings(event_string.splitlines()[1])
    # start = parser.parse(range[0])
    # end = parser.parse(range[1])


def extract_time_zone_if_present(range) -> str:
    """
    :param range: consumes a time range and extracts time zone info if existing. If there is not
    time
    zone info it returns an empty string.
    Algorithm:
    Figure out if there is a time zone, by checking if there is at least one comma.
    If yes split at last comma, inspect remainder.
    If it contains three subsequent upper case letters, this is a time zone info.
    Return that info or an empty string.
    :return: time zone string without leading ', ' or empty string if not time zone was detected.
    """
    # Do not process if there is no at least one comma.
    if ',' not in range:
        return ""

    # Find last comma in string (with rfind), it indicates transition to potential time zone info
    last_comma_pos: int = range.rfind(',')
    potential_time_zone: str = range[last_comma_pos + 2:]

    # Not all date strings have time zone. We can find out by searching for three subsequent
    # upper case characters: https://stackoverflow.com/a/20538792/13805480
    pattern = re.compile("^(.*[A-Z]){3}.*$")
    is_time_zone: bool = pattern.match(potential_time_zone)

    if is_time_zone:
        return potential_time_zone
    return ""


def strip_time_zone(range, time_zone):
    """
    Reduces time zone information from range string, if time_zone is not empty
    :param range: as range string (without 'Scheduled prefix', but possibly with timezone info)
    :param time_zone: as previously extracted time zone info for range.
    :return: range without time zone info
    """
    # Create start and end strings without timezone, if not empty
    # the "-2" is because of the omitted timezone ", " prefix
    if time_zone:
        range = range[:len(range) - len(time_zone) - 2]
    return range


def range_without_timezone_to_start_stop_strings(range: str) -> dict:
    """
    Consumes a range string without time zone information. Is guaranteed of format `* to *` (
    contains keyword 'to'). First and or second half may contain 'at' keyword. Not all
    combinations are legal. Semantic of second substring (after 'to') changes dependeing on
    whether 'at' string is present in first half.
    'at' in both: both substrings are date and time.
    'at' only in first: first substring is date and time, second is date of first one at other time.
    'at' only in last: not legal. (all day events must be all day in both)
    'at' in none: both substrings are pure date (all day) information without time.
    :param range: as string without 'Scheduled' and without time zone information.
    :return: coherent start and end string as start and stop entries in dictionary. multi-day
    flag to indicate the range coveres multiple daysa nd a all-day falg to indicate no time
    information is contained in range string. If no time information provided (all day event)
    midnight (first moment of day) is used as time info. (day begins at midnight, so we use 12
    AM, equivalent to 00:00)
    """
    # Reject in case string does not contain the 'to' keyword
    if "to" not in range:
        raise Exception("The provided string is not a time range.")
    start: str = range.split("to")[0].strip()
    stop: str = range.split("to")[1].strip()

    at_in_first: bool = "at" in start
    at_in_second: bool = "at" in stop

    # Case 1: "at" in both. => Both are already day + time
    if at_in_first and at_in_second:
        # String is already good as is
        pass

    # Case 2: "at" only in first => Use day of first for second
    elif at_in_first and not at_in_second:
        # Use day info of start for stop
        stop = start.split("at")[0] + "at " + stop

    # Case 3: no "at" in either
    elif not at_in_first and not at_in_second:
        # These are all day events, use first second after midnight for start, one second before
        # midnight for second
        start = start + " at 0:01 AM"
        stop = stop + " at 11:59 PM"

    # Note: "at" only in second is not legal. Cannot be all day in first and not in second.
    else:
        raise Exception(
            "Provided string cannot be interpreted. Start has not time but end has. All day "
            "events cannot be unilateral.")

    result: dict = {}
    result['start'] = start
    result['stop'] = stop
    return result


def scheduled_to_start_stop_strings(scheduled_string: str) -> Event:
    """
    Converts scheduled time range to two strings indicating start and end, in same notation as
    original. This does not yet convert time string to system millis.
    Sample inputs:
    Scheduled: Aug 28, 2023 at 7:15 AM to 7:45 AM, EDT
    Scheduled: Nov 6, 2023 to Nov 7, 2023
    Scheduled: Nov 5, 2023 at 12:00 PM to Nov 7, 2023 at 1:00 PM, EST
    Scheduled: Oct 12, 2023 at 10:15 AM to 11:15 AM, GMT-4
    -> Not all inputs have time zone information
    -> Not all inputs have hour information
    -> Not all inputs have same day for start and end
    => All inputs have "to" keyword
    => Time zone information is only provided once, at end.
    => Time zone format changes, can be GMT+- or actual time zone name.


    :param scheduled_string:
    :return: two strings as list, each in same string format. First is start, second is end.
    """
    # Strip initial "Scheduled keyword"
    range: str = scheduled_string.replace('Scheduled: ', '')
    # time zone is empty if no time zone information found.
    time_zone = extract_time_zone_if_present(range)
    range_without_timezone: [str] = range_without_timezone_to_start_stop_strings(range, time_zone)

    start_with_timezone: str = range_without_timezone['start'] + ", " + time_zone
    stop_with_timezone: str = range_without_timezone['stop'] + ", " + time_zone

    return [start_with_timezone, stop_with_timezone]

    # start_without_timezone: str = range_without_timezone.split(' to')[0]
    # end_without_timezone: str = range_without_timezone.split(' to')[1]
    # # Now start is something like: "Aug 27, 2023 at 9:00 AM "
    # # And end is something like: " 11:30 AM"
    # start_without_timezone = start_without_timezone.replace(' at', ',')
    #
    # # If end is shorter than 10 characters, we assume it is an event on the same day as start,
    # # so we still need to concatenate the original day information.
    #
    # # Print to check
    # print("Time Zone: \"" + time_zone + "\"")
    # print("Range remaining \"" + start_without_timezone + "\", \"" + end_without_timezone + "\"")


def separate_string_by_event(pasted_raw_events: str) -> str:
    """
    Breaks the long string pasted into an array of strings (breaks by one or more empty lines).
    Then filters all entries that do not have 'Scheduled' keyword in second line.
    :param: a single raw string containing all events as pasted.
    :return: array of strings, where every entry represents one event as string.
    """
    # split events by searching for one or more newlines
    # See: https://stackoverflow.com/a/57097762/13805480
    blank_line_regex = r"(?:\r?\n){2,}"
    events_as_strings: [str] = re.split(blank_line_regex, pasted_raw_events.strip())

    # Filter out all entries that are not calendar events (calendar event description may have also
    # contained empty lines, in that case we're not interested in the second half of the event.)
    verified_events_as_strings: [str] = []
    for event_string in events_as_strings:
        if len(event_string.splitlines()) > 1 and event_string.splitlines()[1].startswith(
                "Scheduled"):
            verified_events_as_strings.append(event_string)
    return verified_events_as_strings
