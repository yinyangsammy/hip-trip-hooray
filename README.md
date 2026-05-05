#  HipTripHooray

<h3 align="center" text-align="center"><img src="assets/readme/mockup-placeholder.jpg"></h3>

HipTripHooray is a **map-driven travel storytelling platform** designed to transform how users create, structure, and experience itineraries.

Rather than simple lists of places, HipTripHooray enables users to build **rich, narrative journeys**, combining locations, experiences, and contextual data into a seamless, interactive flow.

---

# Table of Contents

## Contents

* [User Stories](#user-stories)

  * [Visitor Goals](#visitor-goals)
* [Design](#design)

  * [Colour Scheme](#colour-scheme)
  * [Typography](#typography)
  * [Imagery](#imagery)
  * [Icons](#icons)
* [Structure](#structure)
* [Irregular Structure](#irregular-structure)
* [Features](#features)

  * [Current Features](#current-features)
  * [Future Features](#future-features)
* [Wireframes](#wireframes)
* [ERDs](#erds)
* [Technologies](#technologies)

  * [Languages](#languages)
  * [Frameworks Libraries Programs](#frameworks-libraries-programs)
* [Testing](#testing)
* [Testing User Stories](#testing-user-stories)

  * [Testing Visitor Goals](#testing-visitor-goals)
* [Deployment](#deployment)
* [Credits](#credits)

---

# User Stories

## Visitor Goals

"***As a user of HipTripHooray, I would like*** _____________"

:white_check_mark: *successfully implemented*
:x: *not yet implemented*

* :white_check_mark: *an intuitive interface for building travel itineraries without needing instructions*

* :white_check_mark: *to create structured trips with multiple categories of experiences*

* :white_check_mark: *to add detailed contextual information to each stop (story, time, weather, imagery)*

* :white_check_mark: *to visually interact with locations using maps*

* :white_check_mark: *to preview my itinerary in real-time as I build it*

* :white_check_mark: *to organise stops into meaningful categories (Sights, Flavours, Experiences, etc.)*

* :white_check_mark: *to see each stop represented clearly with structured data*

* :white_check_mark: *a smooth and responsive user experience across devices*

* :x: *to share itineraries publicly*

* :x: *to collaborate with other users*

* :x: *to book experiences or accommodation directly*

---

# Design

## Colour Scheme

* A modern, travel-inspired palette combining dark overlays, soft highlights, and vibrant accents.
* Designed to support a **glassmorphism UI** and immersive visual hierarchy.

<h3 align="center"><img src="assets/readme/colour-palette-placeholder.png"></h3>

---

## Typography

* Clean, readable fonts for content clarity
* Stylised headings for branding and storytelling emphasis

<h3 align="center"><img src="assets/readme/typography-placeholder.png"></h3>

---

## Imagery

* Map-first interface using OpenStreetMap
* Visual previews of itinerary stops
* Carousel-based layout for immersive storytelling

<h3 align="center"><img src="assets/readme/images-placeholder.png"></h3>

---

## Icons

### Map & Interaction Icons

* 📍 Location markers for stops
* 🗺️ Map navigation indicators
* 📌 Pin system for itinerary building

### UI Icons

* Clean iconography used to enhance usability and reduce friction

---

# Structure

The application is structured around **trip creation and itinerary visualisation**.

## 1) Trip Creation Page

Users can:

* Define trip details
* Add multiple stops using formsets
* Assign categories to each stop
* Input:

  * Story title
  * Description
  * Date
  * Day/Night context
  * Weather
  * Image
  * Location (map or search)

<h3 align="center"><img src="assets/readme/trip-builder-placeholder.png"></h3>

---

## 2) Live Preview System

* Real-time updates as the user inputs data
* Immediate visual feedback
* Reduces friction and improves UX

<h3 align="center"><img src="assets/readme/live-preview-placeholder.png"></h3>

---

## 3) Itinerary View

* Tab-based category navigation
* Carousel-style layout
* Structured storytelling flow

<h3 align="center"><img src="assets/readme/itinerary-placeholder.png"></h3>

---

# Irregular Structure

## Formsets

* Django formsets used for dynamic stop creation
* Allows scalable and flexible input handling

## Mixed View Types

* Combination of CBVs and FBVs
* Chosen for flexibility and clarity where needed

---

# Features

## Current Features:

* Map-based location selection (Leaflet + OpenStreetMap)
* Multi-category trip builder
* Dynamic formsets for adding stops
* Real-time preview system
* Mini-maps per stop
* Itinerary view with tabs and carousel
* Structured stop data (story, date, weather, etc.)
* Responsive UI design
* Country-based logic using ISO codes

---

## Future Features:

* Itinerary table generated from pinned markers
* Visit duration tracking
* Calendar scheduling
* Export/share functionality
* Booking integrations (accommodation, experiences)
* Public itinerary sharing
* User authentication & saved trips

---

# Wireframes

<h3 align="center"><img src="assets/readme/wireframe-placeholder.png"></h3>

---

# Technologies

## Languages

* HTML5
* CSS3
* JavaScript
* Python

---

## Frameworks Libraries Programs

* Django
* Leaflet
* OpenStreetMap
* Nominatim
* Overpass API

---

# Testing

## Approach

* Manual testing for UX validation
* Console-based debugging
* Iterative refinement during development

---

## Key Areas Tested

* Map interactions
* Formset behaviour
* Live preview synchronisation
* Responsiveness across devices

---

# Testing User Stories

## Testing Visitor Goals

### ✅ Intuitive Interface

* Clean layout
* Logical flow
* Minimal learning curve

---

### ✅ Trip Creation

* Formsets allow multiple stops
* Categories clearly structured

---

### ✅ Map Interaction

* Click-to-add functionality
* Search-based location input

---

### ✅ Live Preview

* Immediate updates as user types
* Accurate reflection of final itinerary

---

# Deployment

(To be added)

---

# Credits

## Code

* Built using Django and Vanilla JavaScript
* Inspired by modern UX patterns and travel platforms

---

## Media

* Map data from OpenStreetMap ecosystem
* Additional media to be integrated

---

## Acknowledgements

* Development journey shaped through continuous iteration and refinement

---

# Root

HipTripHooray is being developed as a **portfolio-ready, scalable travel platform**, with future ambitions for real-world deployment and expansion.

<h4 align="center">yinyangsammy 2026</h4>
