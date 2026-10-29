
import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from io import BytesIO
from datetime import date

st.set_page_config(
    page_title="NMIET INFO",
    page_icon="🎓",
    layout="wide"
)

# ---------- APP DESIGN ----------
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
[data-testid="stSidebar"] {
    background-color: #10213b;
}
[data-testid="stSidebar"] * {
    color: white;
}
h1, h2, h3 {
    color: #17365d;
}
.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SAMPLE DATA ----------
if "events" not in st.session_state:
    st.session_state.events = [
        {
            "Event": "Tech Fest",
            "Date": date(2026, 11, 15),
            "Club": "Technical Club",
            "Type": "Event",
            "Description": "Technical competitions and workshops",
            "Link": "https://example.com"
        },
        {
            "Event": "Cultural Day",
            "Date": date(2026, 11, 20),
            "Club": "Cultural Club",
            "Type": "Event",
            "Description": "Music, dance and cultural activities",
            "Link": "https://example.com"
        },
        {
            "Event": "Sample College Holiday",
            "Date": date(2026, 11, 25),
            "Club": "College",
            "Type": "Holiday",
            "Description": "Replace with verified holiday information",
            "Link": ""
        }
    ]

if "clubs" not in st.session_state:
    st.session_state.clubs = [
        {
            "Name": "Technical Club",
            "Description": "Coding, robotics and technical events",
            "Link": "https://example.com"
        },
        {
            "Name": "Cultural Club",
            "Description": "Music, dance and cultural activities",
            "Link": "https://example.com"
        },
        {
            "Name": "Sports Club",
            "Description": "Sports competitions and activities",
            "Link": "https://example.com"
        }
    ]

if "announcements" not in st.session_state:
    st.session_state.announcements = [
        "Welcome to NMIET INFO!",
        "Check the Events section for upcoming activities."
    ]

# ---------- SIDEBAR ----------
st.sidebar.title("🎓 NMIET INFO")
st.sidebar.caption("Unofficial Student Information Portal")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "College Calendar",
        "Events",
        "Clubs",
        "QR Scanner",
        "Quick Links",
        "Announcements",
        "Admin Panel"
    ]
)

# ---------- HOME ----------
if page == "Home":
    st.title("🎓 NMIET INFO")
    st.write("Your college. Your events. All in one place.")
    st.info(
        "Unofficial student portal. "
        "Verify dates and announcements with official college sources."
    )

    today = date.today()
    events = st.session_state.events
    upcoming = sorted(
        [e for e in events if e["Date"] >= today],
        key=lambda e: e["Date"]
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", len(events))
    col2.metric("Clubs", len(st.session_state.clubs))
    col3.metric("Upcoming", len(upcoming))

    st.subheader("📅 Upcoming Events")

    if upcoming:
        for event in upcoming[:5]:
            with st.container(border=True):
                st.markdown(f"### {event['Event']}")
                st.write(f"📅 {event['Date'].strftime('%d %B %Y')}")
                st.write(f"🏷️ {event['Club']}")
                st.write(event["Description"])
                if event["Link"]:
                    st.link_button("Open Event Link", event["Link"])
    else:
        st.write("No upcoming events added yet.")

    st.subheader("📢 Latest Announcements")
    for announcement in st.session_state.announcements:
        st.info(announcement)

# ---------- COLLEGE CALENDAR ----------
elif page == "College Calendar":
    st.title("📅 College Calendar")

    month = st.date_input("Choose a date", value=date.today())
    selected_month = month.month
    selected_year = month.year

    month_events = [
        e for e in st.session_state.events
        if e["Date"].month == selected_month
        and e["Date"].year == selected_year
    ]

    if month_events:
        for event in sorted(month_events, key=lambda e: e["Date"]):
            with st.container(border=True):
                st.write(
                    f"**{event['Date'].strftime('%d %B %Y')}**"
                )
                st.subheader(event["Event"])
                st.write(f"Category: {event['Type']}")
                st.write(event["Description"])
    else:
        st.info("No events or holidays added for this month.")

    st.caption("Calendar dates are sample data until verified.")

# ---------- EVENTS ----------
elif page == "Events":
    st.title("🎉 College Events")

    search = st.text_input("Search events")
    category = st.selectbox(
        "Filter by type",
        ["All", "Event", "Holiday"]
    )

    for event in sorted(
        st.session_state.events,
        key=lambda e: e["Date"]
    ):
        if search.lower() not in event["Event"].lower():
            continue
        if category != "All" and event["Type"] != category:
            continue

        with st.container(border=True):
            st.subheader(event["Event"])
            st.write(f"📅 {event['Date']}")
            st.write(f"Club: {event['Club']}")
            st.write(event["Description"])
            if event["Link"]:
                st.link_button("Registration / Details", event["Link"])

# ---------- CLUBS ----------
elif page == "Clubs":
    st.title("👥 College Clubs")

    for club in st.session_state.clubs:
        with st.container(border=True):
            st.subheader(club["Name"])
            st.write(club["Description"])
            if club["Link"]:
                st.link_button("Open Club Link", club["Link"])

# ---------- QR SCANNER ----------
elif page == "QR Scanner":
    st.title("📷 QR Code Scanner")
    st.write("Upload a QR code image to read its contents.")

    uploaded = st.file_uploader(
        "Upload QR image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:
        try:
            from pyzbar.pyzbar import decode

            image = Image.open(uploaded).convert("RGB")
            st.image(image, width=300)
            results = decode(image)

            if results:
                for result in results:
                    value = result.data.decode("utf-8")
                    st.success(f"QR content: {value}")

                    if value.startswith(("https://", "http://")):
                        st.link_button("Open QR Link", value)
            else:
                st.warning("QR code not detected. Try a clearer image.")

        except Exception:
            st.error(
                "QR scanner dependency unavailable. "
                "Install the required system library and pyzbar."
            )

# ---------- QUICK LINKS ----------
elif page == "Quick Links":
    st.title("🔗 Quick Links")

    links = {
        "Official College Website": "https://www.nmiet.edu.in/",
        "Google Forms": "https://forms.google.com",
        "Google Drive": "https://drive.google.com",
        "Google Calendar": "https://calendar.google.com"
    }

    for name, url in links.items():
        st.link_button(name, url)

    st.caption("Replace or verify links before publishing.")

# ---------- ANNOUNCEMENTS ----------
elif page == "Announcements":
    st.title("📢 Announcements")

    for announcement in st.session_state.announcements:
        st.info(announcement)

# ---------- ADMIN PANEL ----------
elif page == "Admin Panel":
    st.title("🔐 Admin Panel")
    st.warning(
        "Prototype only: this panel has no secure authentication. "
        "Do not deploy it publicly as-is."
    )

    with st.form("add_event"):
        st.subheader("Add Event or Holiday")
        event_name = st.text_input("Event name")
        event_date = st.date_input("Date", value=date.today())
        event_club = st.text_input("Club / Department")
        event_type = st.selectbox("Type", ["Event", "Holiday"])
        event_desc = st.text_area("Description")
        event_link = st.text_input("Registration or information URL")

        submitted = st.form_submit_button("Add to Calendar")

        if submitted:
            if not event_name.strip():
                st.error("Please enter an event name.")
            elif event_link and not event_link.startswith(
                ("https://", "http://")
            ):
                st.error("Please enter a valid HTTP or HTTPS URL.")
            else:
                st.session_state.events.append({
                    "Event": event_name.strip(),
                    "Date": event_date,
                    "Club": event_club.strip(),
                    "Type": event_type,
                    "Description": event_desc.strip(),
                    "Link": event_link.strip()
                })
                st.success("Event added for this session.")
                st.rerun()

    with st.form("add_club"):
        st.subheader("Add a Club")
        club_name = st.text_input("Club name")
        club_desc = st.text_area("Club description")
        club_link = st.text_input("Club URL")
        add_club = st.form_submit_button("Add Club")

        if add_club:
            if not club_name.strip():
                st.error("Please enter a club name.")
            elif club_link and not club_link.startswith(
                ("https://", "http://")
            ):
                st.error("Please enter a valid URL.")
            else:
                st.session_state.clubs.append({
                    "Name": club_name.strip(),
                    "Description": club_desc.strip(),
                    "Link": club_link.strip()
                })
                st.success("Club added for this session.")
                st.rerun()

    with st.form("add_announcement"):
        st.subheader("Publish Announcement")
        announcement = st.text_area("Announcement text")
        publish = st.form_submit_button("Publish")

        if publish:
            if announcement.strip():
                st.session_state.announcements.insert(
                    0, announcement.strip()
                )
                st.success("Announcement added for this session.")
                st.rerun()
            else:
                st.error("Please enter announcement text.")

    st.subheader("Export Events")
    df = pd.DataFrame(st.session_state.events)
    st.download_button(
        "Download Events CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="nmiet_events.csv",
        mime="text/csv"
    )

# ---------- FOOTER ----------
st.sidebar.divider()
st.sidebar.caption("NMIET INFO • Unofficial app")
