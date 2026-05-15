


document.addEventListener("DOMContentLoaded", function(){

const tabs = document.querySelectorAll('.itinerary-tabs input[name="tabs"]');
const flagSpan = document.querySelector(".flag");

function updateFlag(tab){
const country = (tab.dataset.country || "").trim();

if(flagSpan && country && country !== "None"){
flagSpan.innerHTML =
`<img src="https://flagcdn.com/w40/${country.toLowerCase()}.png"
style="width:36px;border-radius:4px;">`;
}
}

tabs.forEach(tab=>{
tab.addEventListener("change", function(){
updateFlag(this);
});
});

const first = document.querySelector('.itinerary-tabs input[name="tabs"]:checked');

if(first){
updateFlag(first);
}

});




document.addEventListener("DOMContentLoaded", function () {

    const initialisedMaps = new Map();

    function initMiniMap(el) {
        if (initialisedMaps.has(el)) {
            // Already initialised — just invalidate size
            setTimeout(() => {
                initialisedMaps.get(el).invalidateSize();
            }, 100);
            return;
        }

        const lat = parseFloat(el.dataset.lat);
        const lng = parseFloat(el.dataset.lng);
        if (isNaN(lat) || isNaN(lng)) return;

        setTimeout(() => {
            const m = L.map(el, {
                zoomControl: false,
                attributionControl: true
            }).setView([lat, lng], 13);

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(m);

            L.marker([lat, lng]).addTo(m);

            initialisedMaps.set(el, m);

            setTimeout(() => {
                m.invalidateSize();
                m.setView([lat, lng], 13);
            }, 200);

        }, 100);
    }

    function scanAndInit() {
        document.querySelectorAll(".mini-map").forEach(initMiniMap);
    }

    // Initial load
    setTimeout(scanAndInit, 500);

    // On every tab change — reinitialise visible maps
    document.querySelectorAll('input[name="tabs"]').forEach(tab => {
        tab.addEventListener("change", () => {
            setTimeout(scanAndInit, 400);
        });
    });

    // On window resize
    window.addEventListener("resize", () => {
        setTimeout(scanAndInit, 300);
    });

});
