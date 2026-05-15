let previewMiniMap;
let previewMiniMarker;


let map;
let marker;

document.addEventListener("DOMContentLoaded", function(){

    // =========================
    // 1. MAP INITIALISATION
    // =========================
    map = L.map('trip-create-map').setView([51.505, -0.09], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
        .addTo(map);

    map.on('click', function(e){

    if(marker){
        map.removeLayer(marker);
    }

    marker = L.marker(e.latlng).addTo(map);

    // Always keep trip-level coords in sync
    const tripLat = document.getElementById("trip-latitude");
    const tripLng = document.getElementById("trip-longitude");
    if(tripLat) tripLat.value = e.latlng.lat;
    if(tripLng) tripLng.value = e.latlng.lng;

    // Write coords to ALL stop-zero cards (one per tab)
    document.querySelectorAll(".stop-0").forEach(card => {
        const latInput = card.querySelector('[name$="latitude"]');
        const lngInput = card.querySelector('[name$="longitude"]');
        if(latInput) latInput.value = e.latlng.lat;
        if(lngInput) lngInput.value = e.latlng.lng;
    });

    // Also write to active card if there is one
    const activeCard = document.querySelector(".stop-card.active");
    if(activeCard){
        const latInput = activeCard.querySelector('[name$="latitude"]');
        const lngInput = activeCard.querySelector('[name$="longitude"]');
        if(latInput) latInput.value = e.latlng.lat;
        if(lngInput) lngInput.value = e.latlng.lng;
    }

    updatePreviewMiniMap(e.latlng.lat, e.latlng.lng);
});


   // =========================
// 2. MAP SEARCH
// =========================
const locationInput = document.getElementById("location-input");

if(locationInput){
    locationInput.addEventListener("change", function(){

        const query = this.value;

        fetch(`https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q=${query}`)
        .then(res => res.json())
        .then(data => {

            if(!data.length) return;

            const place = data[0];

            const lat = parseFloat(place.lat);
            const lon = parseFloat(place.lon);

            map.setView([lat, lon], 10);

            if(marker){
                map.removeLayer(marker);
            }

            marker = L.marker([lat, lon]).addTo(map);

            // Write trip-level coords safely
            const tripLat = document.getElementById("trip-latitude");
            const tripLng = document.getElementById("trip-longitude");
            if(tripLat) tripLat.value = lat;
            if(tripLng) tripLng.value = lon;

            // Write search coords to all stop-zero cards
            document.querySelectorAll(".stop-0").forEach(card => {
                const latInput = card.querySelector('[name$="latitude"]');
                const lngInput = card.querySelector('[name$="longitude"]');
                if(latInput) latInput.value = lat;
                if(lngInput) lngInput.value = lon;
            });

            // Update the live preview mini map
            updatePreviewMiniMap(lat, lon);

            // FULL DESTINATION
            const destinationInput = document.querySelector('[name="destination"]');
            if(destinationInput){
                destinationInput.value = place.display_name;
            }

            // CITY NAME ONLY
            const titleInput = document.querySelector('[name="title"]');
            if(titleInput){

                const addr = place.address;

                const cityName =
                    addr.city ||
                    addr.town ||
                    addr.village ||
                    addr.municipality ||
                    addr.county ||
                    addr.state ||
                    place.display_name.split(",")[0];

                titleInput.value = cityName;
                titleInput.dispatchEvent(new Event("input"));

                // LOCK FIELD
                titleInput.readOnly = true;
            }

            // Save country code for flag display
            const countryCode = place.address.country_code || "";
            const countryCodeInput = document.querySelector('[name="country_code"]');
            if (countryCodeInput) countryCodeInput.value = countryCode.toUpperCase();

        })
        .catch(err => console.error("Search error:", err));

    });
}

// =========================
// MINI PREVIEW MAP
// =========================

function updatePreviewMiniMap(lat, lng){

    const mapEl = document.getElementById("preview-mini-map");
    if(!mapEl) return;

    if(!previewMiniMap){
        previewMiniMap = L.map(mapEl, {
            zoomControl:false,
            attributionControl:false
        }).setView([lat, lng], 13);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
            .addTo(previewMiniMap);
    } else {
        previewMiniMap.setView([lat, lng], 13);
    }

    if(previewMiniMarker){
        previewMiniMap.removeLayer(previewMiniMarker);
    }

    previewMiniMarker = L.marker([lat, lng])
        .addTo(previewMiniMap);
}
// =========================
// 3. LIVE PREVIEW (TRIP LEVEL)
// =========================
const titleInput = document.querySelector('[name="title"]');
const destinationInput = document.querySelector('[name="destination"]');
const startDateInput = document.querySelector('[name="start_date"]');
const endDateInput = document.querySelector('[name="end_date"]');
const descriptionInput =
    document.querySelector('[name="context_title"]') ||
    document.querySelector('[name="description"]');
const tripStoryTitleInput = document.querySelector('[name="story_title"]');
const tripStoryDescInput = document.querySelector('[name="story_description"]');

const previewTitle = document.getElementById("context-title");
const previewDates = document.getElementById("preview-dates");
const previewDescription = document.getElementById("preview-description");

function updatePreview(){

    if(titleInput){
        previewTitle.textContent = titleInput.value || "Your Trip Title";
    }

    if(startDateInput && endDateInput){
        const start = startDateInput.value;
        const end = endDateInput.value;

        previewDates.textContent = (start || end)
            ? `${start || "Start"} → ${end || "End"}`
            : "";
    }

    if(descriptionInput){
        previewDescription.textContent =
            descriptionInput.value || "Stop Name";
    }

    // ✅ FIX — ensure story updates when typing at trip level
    updateStoryPreview();
}

[
    titleInput,
    destinationInput,
    startDateInput,
    endDateInput,
    descriptionInput,
    tripStoryTitleInput,
    tripStoryDescInput
]
.forEach(input => {
    if(input){
        input.addEventListener("input", updatePreview);
    }
});

updatePreview();
updateStoryPreview();


// =========================
// STORY PREVIEW SYSTEM
// =========================
const storyTitleMain = document.querySelector('[name="story_title"]');
const storyDescMain = document.querySelector('[name="story_description"]');

let activeStops = {};

function setActiveStop(card){

    document.querySelectorAll(".stop-card")
        .forEach(c => c.classList.remove("active"));

    card.classList.add("active");

    const category = card.dataset.category;
    activeStops[category] = card;

    updateStoryPreview();
    updateContextCubes();
    updateDayNumber(card);

    const lat = card.querySelector('[name$="latitude"]')?.value;
    const lng = card.querySelector('[name$="longitude"]')?.value;

    if(lat && lng){
        updatePreviewMiniMap(lat, lng);
    }
}

function updateStoryPreview(){

    const active = document.querySelector(".stop-card.active");

    const previewContextTitle = document.getElementById("context-title");
    const previewStoryTitle = document.getElementById("story-title");
    const previewStory = document.getElementById("story-description");
    const previewDescription = document.getElementById("preview-description");

    // =========================
    // NO ACTIVE STOP → TRIP LEVEL
    // =========================
    if(!active){

        if(previewContextTitle){
            previewContextTitle.textContent =
                document.querySelector('[name="title"]')?.value || "Your Context Title";
        }

        if(previewStoryTitle){
            previewStoryTitle.textContent =
                document.querySelector('[name="story_title"]')?.value || "Your trip title will appear here...";
        }

        if(previewStory){
            previewStory.textContent =
                document.querySelector('[name="story_description"]')?.value || "Your trip story will appear here...";
        }

        if(previewDescription){
            previewDescription.textContent =
                document.querySelector('[name="description"]')?.value || "Stop name";
        }

        return;
    }

    // =========================
    // ACTIVE STOP → USE STOP FIELDS
    // =========================
    const storyTitle = active.querySelector('[name$="story_title"]');
    const story = active.querySelector('[name$="story_description"]');
    const description = active.querySelector('[name$="description"]');

    if(previewContextTitle){
        previewContextTitle.textContent =
            document.querySelector('[name="title"]')?.value || "Your Context Title";
    }

    if(previewStoryTitle){
        previewStoryTitle.textContent =
            storyTitle?.value || "Your story title";
    }

    if(previewStory){
        previewStory.textContent =
            story?.value || "Your story";
    }

    if(previewDescription){
        previewDescription.textContent =
            description?.value || "Stop name";
    }
}

// =========================
// DATE + WEATHER CUBES
// =========================
function updateContextCubes(dateInputOverride, weatherInputOverride, dayNightOverride){

    let dateInput = dateInputOverride;
    let weatherInput = weatherInputOverride;
    let dayNightInput = dayNightOverride;

    // If no overrides passed → fallback to ACTIVE STOP ONLY
    if(!dateInput || !weatherInput || !dayNightInput){

        const activeStop = document.querySelector(".stop-card.active");

        if(activeStop){
            dateInput = activeStop.querySelector('[name$="travel_date"]');
            weatherInput = activeStop.querySelector('[name$="weather"]');
            dayNightInput = activeStop.querySelector('[name$="day_night"]');
        } else {
            dateInput = document.querySelector('[name="start_date"]');
            weatherInput = document.querySelector('[name="weather"]');
            dayNightInput = document.querySelector('[name="day_night"]');
        }
    }

    const weatherCube = document.getElementById("preview-weather-cube");
    const weatherIcon = document.getElementById("preview-weather-icon");
    const weatherLabel = document.getElementById("preview-weather-label");
    const dayNightLabel = document.getElementById("preview-daynight");

    const monthEl = document.getElementById("preview-month");
    const dayEl = document.getElementById("preview-day");
    const yearEl = document.getElementById("preview-year");

    const tripInfoMonthEl = document.getElementById("tripinfo-month");
    const tripInfoDayEl = document.getElementById("tripinfo-day");
    const tripInfoYearEl = document.getElementById("tripinfo-year");

    const weatherMap = {
        sun: { icon: "☀", label: "Sunny" },
        cloud: { icon: "☁", label: "Cloudy" },
        rain: { icon: "🌧", label: "Rainy" },
        snow: { icon: "❄", label: "Snowy" },
        wind: { icon: "💨", label: "Windy" },
        storm: { icon: "⛈", label: "Stormy" }
    };

    // WEATHER
    if(weatherInput && weatherCube){
        if(weatherInput.value){
            weatherCube.className = "weather-cube weather-" + weatherInput.value;

            if(weatherMap[weatherInput.value]){
                weatherIcon.textContent = weatherMap[weatherInput.value].icon;
                weatherLabel.textContent = weatherMap[weatherInput.value].label;
            }
        } else {
            weatherCube.className = "weather-cube";
            weatherIcon.textContent = "";
            weatherLabel.textContent = "";
        }
    }

    // DAY/NIGHT
    if(dayNightInput && dayNightLabel){
        dayNightLabel.textContent = dayNightInput.value
            ? dayNightInput.value.toUpperCase()
            : "";
    }

    // DATE (STRICT: ONLY the provided dateInput — no global fallback)
    if(dateInput && dateInput.value){

        const d = new Date(dateInput.value);

        const month = d.toLocaleString('default', { month: 'short' }).toUpperCase();
        const day = d.getDate();
        const year = d.getFullYear();

        if(monthEl) monthEl.textContent = month;
        if(dayEl) dayEl.textContent = day;
        if(yearEl) yearEl.textContent = year;

        // Only update Trip Info cube if we are NOT inside a stop
const activeStop = document.querySelector(".stop-card.active");

if(!activeStop){
    if(tripInfoMonthEl) tripInfoMonthEl.textContent = month;
    if(tripInfoDayEl) tripInfoDayEl.textContent = day;
    if(tripInfoYearEl) tripInfoYearEl.textContent = year;
}

    } else {
        if(monthEl) monthEl.textContent = "";
        if(dayEl) dayEl.textContent = "";
        if(yearEl) yearEl.textContent = "";
    }
}


// =========================
// HARD LOCK title
// =========================
document.addEventListener("input", function(e){

    const card = e.target.closest(".stop-card");

    if(card){

        // ALWAYS make this stop active when typing
        setActiveStop(card);

        // FORCE preview update immediately
        updateStoryPreview();
    }

    // Trip-level typing
    if(
        e.target.matches('[name="story_title"]') ||
        e.target.matches('[name="story_description"]') ||
        e.target.matches('[name="description"]') ||
        e.target.matches('[name="title"]')
    ){
        updateStoryPreview();
    }
});


// =========================
// DAY NUMBER
// =========================
function updateDayNumber(card){

const el = document.getElementById("preview-dates");
if(!card || !el) return;

const start = card.querySelector('[name$="travel_date"]')?.value;

// ONLY START DATE
if(start){
    el.textContent = start;
    return;
}

// ONLY visible tab stops
const activePanel =
document.querySelector(".tab-panel[style*='display: block']");

const allStops =
activePanel.querySelectorAll(".stop-card");

let index = Array.from(allStops).indexOf(card) + 1;

el.textContent = "Day " + index;

}

// =========================
// TYPING UPDATES PREVIEW
// =========================



// =========================
// STOP DATE / WEATHER CHANGE
// =========================
document.addEventListener("change", function(e){

    if(
        e.target.matches('[name$="travel_date"]') ||
        e.target.matches('[name$="weather"]') ||
        e.target.matches('[name$="day_night"]')
    ){
        const card = e.target.closest(".stop-card");

        if(card){
            setActiveStop(card);

            // Only update cubes for THIS stop
            const dateInput = card.querySelector('[name$="travel_date"]');
            const weatherInput = card.querySelector('[name$="weather"]');
            const dayNightInput = card.querySelector('[name$="day_night"]');

            updateContextCubes(
    card.querySelector('[name$="travel_date"]'),
    card.querySelector('[name$="weather"]'),
    card.querySelector('[name$="day_night"]')
);
        }
    }

});


// =========================
// TRIP LEVEL DATE / WEATHER
// =========================
document.addEventListener("change", function(e){

    if(
        e.target.matches('[name="start_date"]') ||
        e.target.matches('[name="weather"]') ||
        e.target.matches('[name="day_night"]')
    ){
        updateContextCubes();
    }

});


// =========================
// CLICKING A STOP SELECTS IT
// =========================
document.addEventListener("click", function(e){
    const card = e.target.closest(".stop-card");
    if(card){
        const category = card.dataset.category;
        activeStops[category] = card;
        setActiveStop(card);
        updateContextCubes();
        updateDayNumber(card);
    }
});

    // =========================
    // CATEGORY LABEL SWITCH
    // =========================
    const labelTitle = document.getElementById("label-title");
    const labelDestination = document.getElementById("label-destination");
    const labelDescription = document.getElementById("label-description");

    const contentMap = {
        sights: {
            title: "Where did you go?",
            destination: "Where was the trip to?",
            description: "What did you see?",
            storyTitle: "Give this trip a title?",
            storyDesc: "Tell us all about your trip & the sights?"
        },
        flavours: {
            title: "Where did you go?",
            destination: "Where was the trip to?",
            description: "Where did you eat / drink?",
            storyTitle: "Give this trip a title?",
            storyDesc: "Tell us all about your trip & the flavours?"
        },
        experiences: {
            title: "Where did you go?",
            destination: "Where was the trip to?",
            description: "What did you experience?",
            storyTitle: "Give this trip a title?",
            storyDesc: "Tell us all about your trip & the experiences?"
        },
        vibes: {
            title: "Where did you go?",
            destination: "Where was the trip to?",
            description: "What was the overall vibe?",
            storyTitle: "Give this trip a title?",
            storyDesc: "Tell us all about your trip & the vibes?"
        },
        seasons: {
            title: "Where did you go?",
            destination: "Where was the trip to?",
            description: "Which season did you travel?",
            storyTitle: "Give this trip a title?",
            storyDesc: "Tell us all about your trip & the seasons?"
        }
    };

    function updateFormContext(category){
        const content = contentMap[category];
        if(!content) return;

        labelTitle.textContent = content.title;
        labelDestination.textContent = content.destination;
        labelDescription.textContent = content.description;

        if(descriptionInput){
            descriptionInput.placeholder = content.description;
        }

        document.querySelectorAll(".story-title").forEach(input => {
            input.placeholder = content.storyTitle;
        });

        document.querySelectorAll(".story-description").forEach(input => {
            input.placeholder = content.storyDesc;
        });
    }

// =========================
// TABS + STOPS
// =========================

function updateTabs(){

    const active = document.querySelector(".trip-tab.active").dataset.category;

    document.querySelectorAll(".tab-panel").forEach(panel => {
        panel.style.display = (panel.dataset.category === active)
            ? "block"
            : "none";
    });

    const activeStopCard = activeStops[active];

    if(activeStopCard){
        setActiveStop(activeStopCard);
    } else {
        const firstStop = document.querySelector(
    `.tab-panel[data-category="${active}"] .stop-card`
);

if(firstStop){
    setActiveStop(firstStop);
} else {
    // No stops yet → show trip preview instead
    document.querySelectorAll(".stop-card")
        .forEach(c => c.classList.remove("active"));
    updateStoryPreview();
}
    }

    updateFormContext(active);
}


// =========================
// STOP NUMBERING
// =========================
function updateStopNumbers(){

const activePanel =
document.querySelector(".tab-panel[style*='display: block']");

const allStops =
activePanel.querySelectorAll(".stop-card");
    const tripTitle = document.querySelector('[name="title"]')?.value || "";

    allStops.forEach((card, index) => {

        const header = card.querySelector(".stop-header h4");
        if(header){
            header.textContent = "Stop " + (index + 1);
        }

        // ✅ display_order
        const orderInput = card.querySelector('.display-order');
        if(orderInput){
            orderInput.value = index + 1;
        }

        // ✅ title (comes from main trip title)
        const titleInput = card.querySelector('.stop-title');
        if(titleInput){
            titleInput.value = tripTitle;
        }

    });
}


// =========================
// ADD STOP
// =========================
document.querySelectorAll(".add-stop-btn").forEach(button => {

button.addEventListener("click", function(){

const totalForms =
document.querySelector("#id_items-TOTAL_FORMS");

const index = document.querySelectorAll(".stop-card").length;

const template =
document.getElementById("empty-form-template")
.innerHTML
.replace(/__prefix__/g, index)
.replace(/__number__/g, index + 1);

const panel = this.closest(".tab-panel");
const container = panel.querySelector(".stops-container");

const categoryId =
document.querySelector(".trip-tab.active")
.dataset.categoryId;

const newStop =
document.createElement("div");

newStop.innerHTML = template;

const stopCard =
newStop.firstElementChild;

stopCard.querySelector(".category-field").value = categoryId;

container.appendChild(stopCard);

totalForms.value = index + 1;

updateStopNumbers();

});
});


// =========================
// REMOVE STOP
// =========================
document.addEventListener("click", function(e){

    if(e.target.classList.contains("remove-stop-btn")){
        const card = e.target.closest(".stop-card");
        if(!card) return;

        const wasActive = card.classList.contains("active");

        card.remove();
        updateStopNumbers();

        // If we deleted the active card, clear active state
        if(wasActive){
            document.querySelectorAll(".stop-card")
                .forEach(c => c.classList.remove("active"));

            updateStoryPreview();
        }
    }

});


// =========================
// TAB CLICK
// =========================
document.querySelectorAll(".trip-tab").forEach(tab => {
    tab.addEventListener("click", function(){

        document.querySelectorAll(".trip-tab")
            .forEach(t => t.classList.remove("active"));

        this.classList.add("active");
        updateTabs();
    });
});


// =========================
// ADD STOP BUTTON CLICK
// =========================
document.querySelectorAll(".add-stop-btn").forEach(button => {

    button.addEventListener("click", function(){
        const panel = this.closest(".tab-panel");
        addStop(panel);
    });

});


// =========================
// INITIAL STOPS
// =========================

updateTabs();

// Auto-activate first stop so map clicks register immediately
const firstStop = document.querySelector(".tab-panel.active .stop-card, .tab-panel[style*='display: block'] .stop-card");
if (firstStop) setActiveStop(firstStop);


// TRIP IMAGE PREVIEW
const tripImageInput = document.querySelector('input[name="trip_image"]');

if(tripImageInput){

    tripImageInput.addEventListener("change", function(){

        const previewImage = document.getElementById("preview-image");
        const imagePlaceholder = document.getElementById("image-placeholder");

        const file = this.files[0];
        if(!file) return;

        const reader = new FileReader();

        reader.onload = function(e){
            if(previewImage){
                previewImage.src = e.target.result;
                previewImage.classList.remove("d-none");
            }

            if(imagePlaceholder){
                imagePlaceholder.style.display = "none";
            }
        };

        reader.readAsDataURL(file);
    });
}


// STOP IMAGE PREVIEW
document.addEventListener("change", function(e){

    if(e.target.matches('.stop-card input[type="file"]')){

        const file = e.target.files[0];
        if(!file) return;

        const previewImage = document.getElementById("preview-image");
        const imagePlaceholder = document.getElementById("image-placeholder");

        const reader = new FileReader();

        reader.onload = function(ev){
            if(previewImage){
                previewImage.src = ev.target.result;
                previewImage.classList.remove("d-none");
            }

            if(imagePlaceholder){
                imagePlaceholder.style.display = "none";
            }
        };

        reader.readAsDataURL(file);
    }

});

});
document.addEventListener("DOMContentLoaded", function(){

const form = document.querySelector("form");

if(form){

form.addEventListener("submit", function(){

    const tripTitle = document.querySelector('[name="title"]')?.value || "";

    document.querySelectorAll(".stop-card").forEach((card, index) => {

        const titleInput = card.querySelector('.stop-title');
        const orderInput = card.querySelector('.display-order');

        if(titleInput){
            titleInput.value = tripTitle;
        }

        if(orderInput){
            orderInput.value = index + 1;
        }

    });

});

}

});




document.addEventListener("change", function(e){

    if (e.target.type === "file") {

        const file = e.target.files[0]

        if (!file) return

        const reader = new FileReader()

        reader.onload = function(event){

            const preview = document.getElementById("preview-image")
            const placeholder = document.getElementById("image-placeholder")

            preview.src = event.target.result
            preview.classList.remove("d-none")

            if (placeholder){
                placeholder.style.display = "none"
            }

        }

        reader.readAsDataURL(file)

    }

})





document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function () {

        form.querySelectorAll('input[type="text"], textarea')
            .forEach(field => {

                // Skip hidden/system fields just in case
                if (
                    field.closest("#empty-form-template") ||
                    field.name?.includes("latitude") ||
                    field.name?.includes("longitude")
                ) {
                    return;
                }

                if (field.value.trim()) {

                    field.value = field.value
                        .toLowerCase()
                        .replace(/\b\w/g, char => char.toUpperCase());

                }

            });

    });

});
