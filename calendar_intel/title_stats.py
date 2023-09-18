from calendar_intel.event import Event


class TitleStats:
    """
    Represents stats for a specific calendar title. This is the cumulative information for all
    calendar events which matcha given title.
    """

    def __init__(self, event: Event):
        self.total_time_seconds: int = event.duration
        self.events: [Event] = [event]

    def add_event(self, event: Event):
        self.events.append(event)
        self.total_time_seconds = self.total_time_seconds + event.duration

    def total_time_seconds(self) -> int:
        return self.total_time_seconds

    @property
    def total_amount_events(self) -> int:
        return len(self.events)

    def __str__(self):
        return format_human_readable_time(self.total_time_seconds) + " (" + str(
            self.total_amount_events) + " Events)"


def format_human_readable_time(seconds: int) -> str:
    """
    Converts amount of time in seconds (int) to a human readable string of days, hours, etc...
    :param: amount in seconds as int
    :return: human-readable string
    """
    days: int = seconds // (60 * 60 * 24)
    hours: int = seconds % (60 * 60 * 24) // (60 * 60)
    minutes: int = seconds % (60 * 24) // 60
    secs: int = seconds % 60
    return str(int(days)) + "d " + str(int(hours)) + "h " + str(int(minutes)) + "m " + str(
        int(secs)) + "s"
