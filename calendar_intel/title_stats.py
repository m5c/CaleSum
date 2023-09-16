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

    def format_seconds(self) -> str:
        days: int = self.total_time_seconds // (60*60*24)
        hours: int = self.total_time_seconds % (60*60*24) // (60*60)
        minutes: int = self.total_time_seconds % (60*24) // 60
        seconds: int = self.total_time_seconds % 60
        return str(int(days))+"d "+str(int(hours))+"h "+str(int(minutes))+"m "+str(int(seconds))+"s"

    def __str__(self):
        return self.format_seconds()+" ("+str(self.total_amount_events)+" Events)"
