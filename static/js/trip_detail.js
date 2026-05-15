document.addEventListener("DOMContentLoaded", function () {

    const flagSpan = document.querySelector(".flag");

    function updateFlag(countryCode) {
        const country = (countryCode || "").trim();
        if (flagSpan && country && country !== "None") {
            flagSpan.innerHTML = `<img src="https://flagcdn.com/w40/${country.toLowerCase()}.png" style="width:36px;border-radius:4px;">`;
        }
    }

    // Works for both itinerary-tabs and trip-tabs radio inputs
    const tabs = document.querySelectorAll('input[name="tabs"]');

    tabs.forEach(tab => {
        tab.addEventListener("change", function () {
            updateFlag(this.dataset.country);
        });
    });

    // Show flag for the initially checked tab
    const first = document.querySelector('input[name="tabs"]:checked');
    if (first) updateFlag(first.dataset.country);

});




document.addEventListener("DOMContentLoaded", function () {

    const maps = new Map();

    function initMap(el) {

        if (maps.has(el)) return;

        const lat = parseFloat(el.dataset.lat);
        const lng = parseFloat(el.dataset.lng);

        if (isNaN(lat) || isNaN(lng)) return;

        setTimeout(() => {

            const map = L.map(el, {
                zoomControl: false,
                attributionControl: true
            });

            L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            L.marker([lat, lng]).addTo(map);

            el._leaflet_map = map;
            maps.set(el, map);

            setTimeout(() => {
                map.invalidateSize();
                map.setView([lat, lng], 13);
            }, 200);

        }, 100);
    }

    function scan() {
        document.querySelectorAll(".mini-map").forEach(initMap);
    }

    // INITIAL LOAD
    setTimeout(scan, 1200);

    // TAB CHANGE
    document.querySelectorAll('input[name="tabs"]').forEach(tab => {
        tab.addEventListener("change", () => {
            setTimeout(scan, 400);
        });
    });

    // CAROUSEL BUTTONS
    document.querySelectorAll(".carousel-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            setTimeout(scan, 400);
        });
    });

    // RESIZE
    window.addEventListener("resize", () => {
        setTimeout(scan, 300);
    });

});



document.addEventListener("DOMContentLoaded", function () {

    function resizeAllMaps() {

        document.querySelectorAll(".mini-map").forEach(el => {

            const map = el._leaflet_map;

            if (!map) return;

            requestAnimationFrame(() => {
                setTimeout(() => {
                    map.invalidateSize();
                }, 250);
            });

        });

    }

    document.querySelectorAll('input[name="tabs"]').forEach(tab => {
        tab.addEventListener("change", function () {
            setTimeout(resizeAllMaps, 500);
        });
    });

    setTimeout(resizeAllMaps, 1000);

});




document.addEventListener("DOMContentLoaded", function(){

document.querySelectorAll(".carousel").forEach(function(carousel){

const track = carousel.querySelector(".carousel-track");
const slides = carousel.querySelectorAll(".carousel-slide");
const nextBtn = carousel.querySelector(".next");
const prevBtn = carousel.querySelector(".prev");
const dots = carousel.querySelectorAll(".dot");

let index = 0;

function updateCarousel(){

// ✅ EXISTING (unchanged)
track.style.transform =
`translateX(-${index * 100}%)`;

dots.forEach(dot => dot.classList.remove("active"));

if(dots[index]){
dots[index].classList.add("active");
}

// 🔥 ADDED: ensure maps render correctly on slide change
setTimeout(() => {

document.querySelectorAll(".mini-map").forEach(el => {

const map = el._leaflet_map;

if (!map) {
    // Trigger your existing scan/init system
    window.dispatchEvent(new Event("resize"));
} else {
    map.invalidateSize();
}

});

}, 300);

}

// ✅ EXISTING (unchanged)
nextBtn.addEventListener("click", function(){

index++;

if(index >= slides.length){
index = 0;
}

updateCarousel();

});

prevBtn.addEventListener("click", function(){

index--;

if(index < 0){
index = slides.length - 1;
}

updateCarousel();

});

dots.forEach((dot, i)=>{

dot.addEventListener("click", function(){

index = i;

updateCarousel();

});

});

});

});





document.addEventListener("DOMContentLoaded", function () {

    const initialisedMaps = new Map();

    function initMiniMap(el) {
        if (initialisedMaps.has(el)) {
            setTimeout(() => {
                initialisedMaps.get(el).invalidateSize();
            }, 100);
            return;
        }

        let lat = parseFloat(el.dataset.lat);
        let lng = parseFloat(el.dataset.lng);

        if (isNaN(lat) || isNaN(lng) || lat === 0 || lng === 0) {
            lat = 51.505;
            lng = -0.09;
        }

        setTimeout(() => {
            const m = L.map(el, {
                zoomControl: false,
                attributionControl: true
            }).setView([lat, lng], 12);

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(m);

            L.marker([lat, lng]).addTo(m);

            initialisedMaps.set(el, m);

            setTimeout(() => {
                m.invalidateSize();
                m.setView([lat, lng], 12);
            }, 200);

        }, 100);
    }

    function scanAndInit() {
        document.querySelectorAll(".mini-map").forEach(initMiniMap);
    }

    setTimeout(scanAndInit, 500);

    document.querySelectorAll('input[name="tabs"]').forEach(tab => {
        tab.addEventListener("change", () => {
            setTimeout(scanAndInit, 400);
        });
    });

    window.addEventListener("resize", () => {
        setTimeout(scanAndInit, 300);
    });

});