"""
Object representation of parsed calendar event.
Author: Maximilian Schiedermeier
"""


class Event:

    def __init__(self, title: str, start: int, end: int, all_day: bool, multi_day: bool,
                 time_zone: str):
        """
        Event that allocates a range of system time to a descriptive activity.
        :param title:
        :param start:
        :param end:
        """
        self.title: str = title
        self.start: int = start
        self.end: int = end
        self.duration: int = 0
        self.all_day: bool = all_day
        self.multi_day: bool = multi_day
        self.time_zone: str = time_zone

    def __str__(self):
        """
        Creates human-readable representation of event, intended for printing to console.
        :return: string representation of this calendar event
        """
        result: str = "+--------------------+\n"
        result = result + "| Title:       " + self.title + "\n"
        result = result + "| Start:       " + str(self.start) + "\n"
        result = result + "| End:         " + str(self.end) + "\n"
        result = result + "| Duration     " + str(self.duration) + "\n"
        result = result + "| All Day:     " + str(self.all_day) + "\n"
        result = result + "| Multi Day:   " + str(self.multi_day) + "\n"
        result = result + "| Time Zone:   " + self.time_zone + "\n"
        result = result + "+--------------------+\n\n"
        return result
