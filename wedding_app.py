import streamlit as st
import base64
import os
from PIL import Image
import streamlit.components.v1 as components

# === Page Config ===
st.set_page_config(page_title="Victor & Joy Wedding", layout="wide")

# === Scrolling Notification ===
st.markdown("""
<div style="overflow:hidden; white-space:nowrap;">
    <div style="
        display:inline-block;
        padding-left:100%;
        animation: marquee 15s linear infinite;
        color: #d63384;
        font-size: 1.1em;
        font-weight: bold;
    ">
        Please explore each section of Victor & Joy's wedding using the top tabs. 💕
    </div>
</div>
<style>
@keyframes marquee {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}
</style>
""", unsafe_allow_html=True)

# === Helper Functions ===
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

def file_exists(path, file_type="file"):
    if not os.path.exists(path):
        st.warning(f"{file_type.capitalize()} not found at `{path}`.")
        return False
    return True

def download_button(file_path, label):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">📥 {label}</a>'
            st.markdown(href, unsafe_allow_html=True)

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["💌 Wedding Card", "📜 Wedding Program", "📍 Wedding Navigation", "🎥 Live Stream"])

# === Tab 1: Wedding Card ===
with tab1:
    st.markdown("<h1 style='text-align: center;'>Victor & Joy's Wedding 💍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>You're Invited!</h3>", unsafe_allow_html=True)

    card_path = "assets/invitation_card.jpeg"
    if file_exists(card_path, "invitation card"):
        if card_path.endswith(".pdf"):
            show_pdf(card_path)
        else:
            st.image(card_path, use_container_width=True, caption="Wedding Invitation - Pinch to Zoom on Mobile")
        download_button(card_path, "Download Invitation")

    # Scrolling Memories
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

# === Tab 2: Wedding Program ===
with tab2:
    st.markdown("<h1 style='text-align: center;'>Wedding Program 📜</h1>", unsafe_allow_html=True)

    img_path = "assets/wedding_program.jpeg"
    pdf_path = "assets/wedding_program.pdf"

    if file_exists(img_path, "program image"):
        st.image(img_path, use_container_width=True, caption="Wedding Program (Pinch to Zoom on Mobile)")
    else:
        st.warning("Preview image not found.")

    if file_exists(pdf_path, "program file"):
        with st.expander("📄 Tap to View Full Wedding Program PDF"):
            show_pdf(pdf_path)
        st.markdown("<br>", unsafe_allow_html=True)
        download_button(pdf_path, "Download Wedding Program")
    else:
        st.warning("Wedding program PDF not found.")

# === Tab 3: Wedding Navigation ===
with tab3:
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
                max-height: 80px;
                font-size: 12px;
            }}
            @media (max-width: 600px) {{
                .leaflet-routing-container {{
                    max-height: 70px;
                    font-size: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div id='map'></div>
        <script src='https://unpkg.com/leaflet@1.2.0/dist/leaflet.js'></script>
        <script src='https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js'></script>
        <script>
            let lastSpokenInstruction = '';
            let routeControl;
            let destLatLng = L.latLng({dest_lat}, {dest_lon});

            const map = L.map('map').fitWorld();
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; OpenStreetMap contributors'
            }}).addTo(map);

            L.marker(destLatLng).addTo(map).bindPopup("Destination: {selected_venue}");

            function speak(text) {{
                if (text && text !== lastSpokenInstruction) {{
                    const synth = window.speechSynthesis;
                    synth.cancel();
                    const utter = new SpeechSynthesisUtterance(text);
                    synth.speak(utter);
                    lastSpokenInstruction = text;
                }}
            }}

            function updateRoute(position) {{
                const userLatLng = L.latLng(position.coords.latitude, position.coords.longitude);

                if (routeControl) {{
                    routeControl.setWaypoints([userLatLng, destLatLng]);
                }} else {{
                    routeControl = L.Routing.control({{
                        waypoints: [userLatLng, destLatLng],
                        routeWhileDragging: false,
                        addWaypoints: false,
                        showAlternatives: false,
                        fitSelectedRoutes: true
                    }}).addTo(map);

                    routeControl.on('routesfound', function(e) {{
                        const routes = e.routes;
                        if (routes.length > 0) {{
                            const instructions = routes[0].instructions;
                            if (instructions.length > 0) {{
                                speak(instructions[0].text);
                            }}
                        }}
                    }});
                }}
            }}

            function onError(error) {{
                alert("Could not get your location. Please enable GPS or location access.");
            }}

            navigator.geolocation.watchPosition(updateRoute, onError, {{
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }});

            speak("Welcome to Victor and Joy's Wedding navigation. Please follow the directions.");
        </script>
    </body>
    </html>
    """
    components.html(html_string, height=650)

with tab4:
    st.markdown("<h1 style='text-align: center;'>🎥 Victor & Joy's Wedding – Live Stream</h1>", unsafe_allow_html=True)
    st.markdown("Join us live at 1:00 PM on July 11, 2025! The stream will begin shortly...")

    countdown_html = """
    <div id="countdown-container" style="text-align:center;">
        <h2 id="countdown" style="color:#d63384;"></h2>
    </div>

    <div id="livestream" style="display:none; text-align:center;">
        <iframe 
            src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2Fvictor.idakwo.5%2Fvideos%2F2637333386460126%2F&width=1280"  
            width="100%" height="720" style="border:none;overflow:hidden" scrolling="no" frameborder="0" 
            allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share">
        </iframe>
    </div>

    <script>
    const countdownElement = document.getElementById("countdown");
    const livestreamDiv = document.getElementById("livestream");
    const countdownContainer = document.getElementById("countdown-container");

    const eventDate = new Date("2025-07-11T13:00:00+01:00").getTime();

    const interval = setInterval(() => {
        const now = new Date().getTime();
        const distance = eventDate - now;

        if (distance <= 0) {
            clearInterval(interval);
            countdownContainer.style.display = "none";
            livestreamDiv.style.display = "block";
        } else {
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            countdownElement.innerHTML = `⏳ Live in ${days}d ${hours}h ${minutes}m ${seconds}s`;
        }
    }, 1000);
    </script>
    """

    components.html(countdown_html, height=750)

# === Footer ===
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        With ❤️ from Victor & Joy | © 2025
    </div>
""", unsafe_allow_html=True)
