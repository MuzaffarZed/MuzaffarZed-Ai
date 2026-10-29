import win32evtlog
import win32evtlogutil
import win32con

server = 'localhost'
logtype = 'Application'
hand = win32evtlog.OpenEventLog(server, logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

print("Reading Application Event Log:")
count = 0
events = win32evtlog.ReadEventLog(hand, flags, 0)
while events and count < 10:
    for ev in events:
        source = ev.SourceName
        event_id = ev.EventID & 0xFFFF
        if ev.EventType in (win32con.EVENTLOG_ERROR_TYPE, win32con.EVENTLOG_WARNING_TYPE) or "FL" in source:
            time_gen = ev.TimeGenerated.Format()
            strings = ev.StringInserts or []
            msg = " | ".join(str(s) for s in strings)
            if any(k in msg.lower() or k in source.lower() for k in ["fl64", "fl studio", "image-line", "fault"]):
                print(f"[{time_gen}] Source: {source} (ID: {event_id}) -> {msg[:300]}")
                count += 1
                if count >= 10: break
    events = win32evtlog.ReadEventLog(hand, flags, 0)
win32evtlog.CloseEventLog(hand)

if count == 0:
    print("No FL Studio or Application crash events found in recent logs.")
