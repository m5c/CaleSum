"""
Consumes a list of events and analyzes the contained information,, e.g. to create textual
breakdown or statistics.
"""
from calendar_intel.event import Event
from calendar_intel.title_stats import TitleStats, format_human_readable_time


def event_filter(events: [Event], include_all_day: bool, include_multi_day: bool):
    """
    Depending on which checkboxes are selected in the gui we want to kick out some of the ecents
    pasted into the text box. i.e. events that spend over multiple days or are all day events. (
    both have no accurate notion of time).
    """
    # nothing to do if no filtering requested
    if include_multi_day and include_multi_day:
        return events

    # filter is only active if things are excluded.
    filtered_events: [Event] = []
    for event in events:
        if not include_all_day and event.all_day:
            continue
        if not include_multi_day and event.multi_day:
            continue
        # no filter criteria met, lets add this event to result set
        filtered_events.append(event)
    return filtered_events


def extract_all_titles(events: [Event], case_sensitive: bool) -> dict:
    """
    Consumes a list of events an returns a dictionary with only the titles.
    """
    titles: dict = {}
    for event in events:
        if case_sensitive:
            titles[event.title] = []
        else:
            titles[event.title.lower()] = []
    return titles


def create_stats(events: [Event], case_sensitive: bool) -> str:
    """
    Creates stats for a provided list of events. The stats are a printable string where the first
    line is the total mount of time for everything that has been pasted, followed by an accurate
    breakdown.
    """
    print("Mining " + str(len(events)) + " events.")

    # this is a map from titles to title stats objects.
    title_stats_by_title: dict = {}

    # iterate over all events and add to dictionary
    for event in events:
        # figure out title to use
        title: str = event.title.lower() if case_sensitive else event.title

        # if map has already an entry, extend it Otherwise, create new list with that entry
        if title_stats_by_title.get(title):
            title_stats_by_title[title].add_event(event)
        else:
            title_stats_by_title[title] = TitleStats(event)

    # sort dictionary by total times
    # python is messy, it's not actually a list that comes back, but a list of tuples
    sorted_title_stats: list = sorted(title_stats_by_title.items(),
                                      key=lambda item: item[1].total_time_seconds, reverse=True)

    # then print stats for each entry in map (for now unsorted)
    stats_text: str = ""
    total_time: int = 0
    for stats in sorted_title_stats:
        stats_text += f'{stats[0][:40]:44s}  {str(stats[1]):32s}\n'
        total_time += stats[1].total_time_seconds

    return "Total time: " + format_human_readable_time(total_time) + "\n----------\n" + stats_text
