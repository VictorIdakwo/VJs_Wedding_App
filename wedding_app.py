import streamlit as st
import base64
import os
from PIL import Image
import streamlit.components.v1 as components

# === Page Config ===
st.set_page_config(page_title="Victor & Joy Wedding", layout="wide")

# === Sidebar Navigation ===
page = st.sidebar.selectbox("Go to", ["Wedding Card", "Wedding Program", "Wedding Navigation"])

# === Helper to Show PDF ===
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# === Helper to Check File ===
def file_exists(path, file_type="file"):
    if not os.path.exists(path):
        st.warning(f"{file_type.capitalize()} not found at `{path}`.")
        return False
    return True

# === Helper to Create Download Button ===
def download_button(file_path, label):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">📥 {label}</a>'
            st.markdown(href, unsafe_allow_html=True)

# === Wedding Card Page ===
if page == "Wedding Card":
    st.markdown("<h1 style='text-align: center;'>Victor & Joy's Wedding 💍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>You're Invited!</h3>", unsafe_allow_html=True)

    card_path = "assets/invitation_card.jpeg"
    if file_exists(card_path, "invitation card"):
        if card_path.endswith(".pdf"):
            show_pdf(card_path)
        else:
            st.image(card_path, use_container_width=True)
        download_button(card_path, "Download Invitation")

    # Scrolling Memories Section
    media_folder = "assets/media"
    if os.path.exists(media_folder):
        media_files = sorted(
            [f for f in os.listdir(media_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
            key=lambda x: os.path.getmtime(os.path.join(media_folder, x))
        )
        if media_files:
            st.markdown("---")
            st.subheader("Memories ❤️ (Swipe → or wait...)")

            images_html = ""
            for file in media_files:
                file_path = os.path.join(media_folder, file)
                try:
                    with open(file_path, "rb") as image_file:
                        encoded = base64.b64encode(image_file.read()).decode()
                        ext = os.path.splitext(file)[-1].replace(".", "")
                        images_html += f'<img src="data:image/{ext};base64,{encoded}" class="carousel-img"/>'
                except:
                    continue

            carousel_css = """
                <style>
                .carousel-container {
                    white-space: nowrap;
                    overflow: hidden;
                    width: 100%;
                    margin-top: 10px;
                    padding-bottom: 30px;
                }
                .carousel-img {
                    display: inline-block;
                    margin: 0 10px;
                    height: 160px;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                    animation: scroll-left 30s linear infinite;
                }
                @keyframes scroll-left {
                    0% { transform: translateX(100%); }
                    100% { transform: translateX(-100%); }
                }
                </style>
            """
            st.markdown(carousel_css, unsafe_allow_html=True)
            st.markdown(f'<div class="carousel-container">{images_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No images found in 'assets/media'. Upload .jpg or .png files.")
    else:
        st.warning("Media folder not found. Please create 'assets/media' and add images.")

# === Wedding Program Page ===
elif page == "Wedding Program":
    st.markdown("<h1 style='text-align: center;'>Wedding Program 📜</h1>", unsafe_allow_html=True)
    program_path = "assets/wedding_program.jpeg"
    if file_exists(program_path, "program file"):
        if program_path.endswith(".pdf"):
            show_pdf(program_path)
        else:
            st.image(program_path, use_container_width=True)
        download_button(program_path, "Download Wedding Program")

# === Wedding Navigation Page ===
elif page == "Wedding Navigation":
    st.markdown("<h1 style='text-align: center;'>Navigate to the Wedding Venues 📍</h1>", unsafe_allow_html=True)
    st.markdown("### 📌 Select a destination below to begin navigation:")

    venues = {
        "Traditional Marriage": {"coords": (9.636327, 6.513065)},
        "Church Wedding - LFC Gbaiko Minna": {"coords": (9.642587, 6.505967)},
        "Reception - PSS Hall": {"coords": (9.635238, 6.512557)},
        "SAFTEC Hotels": {"coords": (9.589305, 6.541952)},
        "WhiteHills Luxery Hotel": {"coords": (9.590192, 6.541766)},
    }

    selected_venue = st.selectbox("Choose a destination", list(venues.keys()))
    dest_lat, dest_lon = venues[selected_venue]["coords"]

    html_string = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8' />
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <link rel='stylesheet' href='https://unpkg.com/leaflet@1.2.0/dist/leaflet.css' />
        <link rel='stylesheet' href='https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.css' />
        <style>
            #map {{
                width: 100%;
                height: 600px;
            }}
            .leaflet-routing-container {{
                max-height: 150px;
                overflow-y: auto;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div id='map'></div>
        <script src='https://unpkg.com/leaflet@1.2.0/dist/leaflet.js'></script>
        <script src='https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js'></script>
        <script>
            var map = L.map('map').fitWorld();

            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; OpenStreetMap contributors'
            }}).addTo(map);

            var destLatLng = L.latLng({dest_lat}, {dest_lon});
            L.marker(destLatLng).addTo(map).bindPopup("Destination: {selected_venue}").openPopup();

            function speakDirection(text) {{
                const synth = window.speechSynthesis;
                const utter = new SpeechSynthesisUtterance(text);
                synth.speak(utter);
            }}

            function onLocationFound(e) {{
                var userLatLng = e.latlng;
                var control = L.Routing.control({{
                    waypoints: [userLatLng, destLatLng],
                    routeWhileDragging: false,
                    addWaypoints: false,
                    showAlternatives: false
                }}).addTo(map);

                control.on('routesfound', function(e) {{
                    var routes = e.routes;
                    var summary = routes[0].summary;
                    var steps = routes[0].instructions || [];
                    speakDirection(`Starting route to {selected_venue}. Total distance: ${{summary.totalDistance / 1000}} kilometers.`);
                    routes[0].instructions.forEach(instr => {{
                        speakDirection(instr.text);
                    }});
                }});
            }}

            function onLocationError(e) {{
                alert("Could not get your location. Please enable GPS or location access.");
            }}

            map.on('locationfound', onLocationFound);
            map.on('locationerror', onLocationError);
            map.locate({{setView: true, maxZoom: 16}});
        </script>
    </body>
    </html>
    """

    components.html(html_string, height=650)

# === Footer ===
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        With ❤️ from Victor & Joy | © 2025
    </div>
""", unsafe_allow_html=True)
