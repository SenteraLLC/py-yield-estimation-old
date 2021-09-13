import arrow


def hello_world(tz):
    """Hello world from a location."""
    now = arrow.now(tz)
    current_time = now.format("h:mm a")
    location = tz.split("/")[-1].replace("_", " ")
    return f"Hello, {location}! The time is {current_time}."
