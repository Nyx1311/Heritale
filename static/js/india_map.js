// India Map - Using Leaflet.js with OpenStreetMap (Real Map!)
// No API key required - completely free
// Dynamically loads all states and monuments from the database
// Enhanced with 3D depth, parallax, and engaging interactions

// State coordinates for map markers (approximate center of each state/UT)
const stateCoordinates = {
    'Delhi': { coords: [28.6139, 77.2090], zoom: 11 },
    'Uttar Pradesh': { coords: [27.1767, 78.0081], zoom: 7 },
    'Rajasthan': { coords: [26.9124, 75.7873], zoom: 7 },
    'Maharashtra': { coords: [19.0760, 72.8777], zoom: 7 },
    'West Bengal': { coords: [22.5726, 88.3639], zoom: 8 },
    'Telangana': { coords: [17.3850, 78.4867], zoom: 9 },
    'Karnataka': { coords: [15.3350, 76.4600], zoom: 8 },
    'Tamil Nadu': { coords: [10.7867, 79.1378], zoom: 8 },
    'Andhra Pradesh': { coords: [15.9129, 79.7400], zoom: 8 },
    'Kerala': { coords: [10.8505, 76.2711], zoom: 8 },
    'Goa': { coords: [15.2993, 74.1240], zoom: 10 },
    'Gujarat': { coords: [22.2587, 71.1924], zoom: 7 },
    'Madhya Pradesh': { coords: [23.4734, 77.9479], zoom: 7 },
    'Odisha': { coords: [20.2961, 85.8245], zoom: 8 },
    'Punjab': { coords: [31.1471, 75.3412], zoom: 8 },
    'Haryana': { coords: [29.0588, 76.0856], zoom: 9 },
    'Bihar': { coords: [25.0961, 85.3131], zoom: 8 },
    'Jharkhand': { coords: [23.6102, 85.2799], zoom: 8 },
    'Chhattisgarh': { coords: [21.2787, 81.8661], zoom: 8 },
    'Assam': { coords: [26.2006, 92.9376], zoom: 8 },
    'Sikkim': { coords: [27.5330, 88.5122], zoom: 10 },
    'Himachal Pradesh': { coords: [31.1048, 77.1734], zoom: 8 },
    'Uttarakhand': { coords: [30.0668, 79.0193], zoom: 8 },
    'Jammu and Kashmir': { coords: [33.7782, 76.5762], zoom: 8 },
    'Ladakh': { coords: [34.1526, 77.5771], zoom: 8 },
    'Arunachal Pradesh': { coords: [28.2180, 94.7278], zoom: 8 },
    'Nagaland': { coords: [26.1584, 94.5624], zoom: 9 },
    'Manipur': { coords: [24.6637, 93.9063], zoom: 9 },
    'Mizoram': { coords: [23.1645, 92.9376], zoom: 9 },
    'Tripura': { coords: [23.9408, 91.9882], zoom: 9 },
    'Meghalaya': { coords: [25.4670, 91.3662], zoom: 9 },
    'Andaman and Nicobar Islands': { coords: [11.7401, 92.6586], zoom: 9 },
    'Lakshadweep': { coords: [10.5667, 72.6417], zoom: 11 },
    'Puducherry': { coords: [11.9416, 79.8083], zoom: 11 },
    'Chandigarh': { coords: [30.7333, 76.7794], zoom: 12 },
    'Dadra and Nagar Haveli and Daman and Diu': { coords: [20.1809, 73.0169], zoom: 10 }
};

// Monument data will be loaded dynamically from API
let monumentData = {};

// Custom marker icons - Enhanced with animated effects
const createMonumentIcon = (count) => {
    return L.divIcon({
        className: 'monument-marker',
        html: `<div class="marker-pin">
                    <span class="marker-count">${count}</span>
                    <span class="marker-icon">🏛️</span>
               </div>`,
        iconSize: [52, 62],
        iconAnchor: [26, 62],
        popupAnchor: [0, -62]
    });
};

const createSingleMonumentIcon = () => {
    return L.divIcon({
        className: 'single-monument-marker',
        html: `<div class="single-marker-pin">📍</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
};

// India Map class using Leaflet - Enhanced with 3D depth and engaging interactions
class IndiaMap {
    constructor(containerId) {
        this.containerId = containerId;
        this.map = null;
        this.markers = [];
        this.monumentMarkers = [];
        this.selectedState = null;
        this.states = [];
        this.totalMonuments = 0;
        this.init();
    }

    async init() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error('Map container not found');
            return;
        }

        // Set container height for map
        container.style.height = '650px';
        container.style.overflow = 'hidden';

        console.log('Initializing Leaflet map...');
        this.createMap();

        // Load states dynamically from API
        await this.loadStatesFromAPI();

        this.addStateMarkers();
        this.addLegend();
        this.updateMapStats();
        this.setupMapControls();
        this.setupParallax();
        console.log(`Map initialized with ${this.states.length} states!`);
    }

    async loadStatesFromAPI() {
        try {
            console.log('Loading states from API...');
            const response = await fetch('/api/states');
            const data = await response.json();

            if (data.states && Array.isArray(data.states)) {
                this.states = data.states;
                console.log(`Loaded ${this.states.length} states:`, this.states);
            } else {
                console.error('Invalid states data received');
            }
        } catch (error) {
            console.error('Error loading states:', error);
        }
    }

    createMap() {
        // Initialize map centered on India with smooth animations
        this.map = L.map(this.containerId, {
            center: [22.5, 82.5], // Center of India
            zoom: 5,
            minZoom: 4,
            maxZoom: 18,
            scrollWheelZoom: true,
            zoomAnimation: true,
            fadeAnimation: true,
            markerZoomAnimation: true,
            zoomSnap: 0.25,
            zoomDelta: 0.5
        });

        // Use Stamen Watercolor-inspired tiles for heritage feel, fallback to OSM
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | AI Heritage Storyteller',
            maxZoom: 19
        }).addTo(this.map);

        // Add event listeners for map interactions
        this.map.on('zoomend', () => this.onZoomChange());
        this.map.on('movestart', () => this.onMoveStart());
        this.map.on('moveend', () => this.onMoveEnd());
    }

    onZoomChange() {
        // Adjust marker visibility or size based on zoom
        const zoom = this.map.getZoom();
        const wrapper = document.getElementById('map-wrapper');
        if (wrapper) {
            // Subtle perspective shift based on zoom
            const depth = Math.max(0, (zoom - 5) * 2);
            wrapper.style.boxShadow = `0 ${20 + depth}px ${60 + depth * 2}px rgba(0,0,0,${0.2 + depth * 0.01})`;
        }
    }

    onMoveStart() {
        const container = document.getElementById(this.containerId);
        if (container) container.style.cursor = 'grabbing';
    }

    onMoveEnd() {
        const container = document.getElementById(this.containerId);
        if (container) container.style.cursor = 'grab';
    }

    addStateMarkers() {
        console.log('Adding markers for states...');

        this.states.forEach((stateData, index) => {
            const stateName = stateData.state;
            const monumentCount = stateData.count;
            this.totalMonuments += monumentCount;

            // Get coordinates for this state
            const stateInfo = stateCoordinates[stateName];
            if (!stateInfo) {
                console.warn(`No coordinates found for state: ${stateName}`);
                return;
            }

            // Create marker for state with staggered animation
            const marker = L.marker(stateInfo.coords, {
                icon: createMonumentIcon(monumentCount),
                riseOnHover: true,
                riseOffset: 30
            }).addTo(this.map);

            // Create enhanced popup content with heritage header
            const popupContent = `
                <div class="map-popup">
                    <div class="map-popup-header">
                        <h3>📍 ${stateName}</h3>
                    </div>
                    <div class="map-popup-body">
                        <p><strong>${monumentCount}</strong> Heritage Monument${monumentCount > 1 ? 's' : ''}</p>
                        <button onclick="indiaMap.selectState('${stateName}')" class="popup-btn">
                            ✨ Explore Monuments
                        </button>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent, {
                maxWidth: 320,
                minWidth: 220,
                className: 'heritage-popup',
                autoPanPaddingTopLeft: [50, 50],
                autoPanPaddingBottomRight: [50, 50]
            });

            // Add hover tooltip for quick info
            marker.bindTooltip(
                `<strong>${stateName}</strong><br>${monumentCount} monument${monumentCount > 1 ? 's' : ''}`,
                {
                    direction: 'top',
                    offset: [0, -65],
                    className: 'heritage-tooltip'
                }
            );

            // Store marker reference
            this.markers.push({ stateName, marker, count: monumentCount });
        });

        console.log(`Added ${this.markers.length} state markers`);
    }

    async selectState(stateName) {
        console.log('Selected state:', stateName);
        this.selectedState = stateName;

        // Get state coordinates
        const stateInfo = stateCoordinates[stateName];
        if (!stateInfo) {
            console.error(`No coordinates for state: ${stateName}`);
            return;
        }

        // Close any open popup
        this.map.closePopup();

        // Zoom to state with smooth fly animation
        this.map.flyTo(stateInfo.coords, stateInfo.zoom, {
            duration: 1.8,
            easeLinearity: 0.25
        });

        // Clear previous monument markers
        this.monumentMarkers.forEach(m => this.map.removeLayer(m));
        this.monumentMarkers = [];

        // Load monuments from API
        try {
            const response = await fetch(`/api/monuments/${encodeURIComponent(stateName)}`);
            const data = await response.json();

            if (data.monuments && Array.isArray(data.monuments)) {
                console.log(`Loaded ${data.monuments.length} monuments for ${stateName}`);

                // Add a brief highlight effect on the map wrapper
                const wrapper = document.getElementById('map-wrapper');
                if (wrapper) {
                    wrapper.style.transition = 'box-shadow 0.5s ease';
                    wrapper.style.boxShadow = '0 20px 60px rgba(0,0,0,0.2), 0 0 50px rgba(212,175,55,0.3)';
                    setTimeout(() => {
                        wrapper.style.boxShadow = '';
                    }, 1000);
                }
            }
        } catch (error) {
            console.error('Error loading monuments:', error);
        }

        // Trigger monument loading in main.js
        if (typeof loadMonuments === 'function') {
            loadMonuments(stateName);
        }
    }

    addLegend() {
        const legend = L.control({ position: 'bottomright' });

        legend.onAdd = function (map) {
            const div = L.DomUtil.create('div', 'map-legend-leaflet');
            div.innerHTML = `
                <h4>🗺️ India Heritage Map</h4>
                <div class="legend-item">
                    <span class="legend-marker">🏛️</span>
                    <span>Heritage Sites (with count)</span>
                </div>
                <div class="legend-item">
                    <span class="legend-marker">📍</span>
                    <span>Individual Monuments</span>
                </div>
                <p class="legend-tip">Click markers to explore! Scroll to zoom.</p>
            `;
            return div;
        };

        legend.addTo(this.map);
    }

    // Update the stats bar with animated counting
    updateMapStats() {
        const statesEl = document.getElementById('stat-states');
        const monumentsEl = document.getElementById('stat-monuments');
        const storiesEl = document.getElementById('stat-stories');

        if (statesEl) this.animateCounter(statesEl, this.states.length, 1200);
        if (monumentsEl) this.animateCounter(monumentsEl, this.totalMonuments, 1500);
        if (storiesEl) this.animateCounter(storiesEl, this.totalMonuments, 1800);
    }

    animateCounter(element, target, duration) {
        let start = 0;
        const increment = target / (duration / 16);
        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.ceil(start);
            }
        }, 16);
    }

    // Setup map control buttons
    setupMapControls() {
        const resetBtn = document.getElementById('btn-reset-map');
        const randomBtn = document.getElementById('btn-random-monument');

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetView();
                // Hide monuments section
                const monumentsSection = document.getElementById('monuments-section');
                if (monumentsSection) monumentsSection.style.display = 'none';
            });
        }

        if (randomBtn) {
            randomBtn.addEventListener('click', () => this.surpriseMe());
        }
    }

    // Navigate to a random state/monument
    async surpriseMe() {
        if (this.states.length === 0) return;

        // Pick a random state
        const randomIndex = Math.floor(Math.random() * this.states.length);
        const randomState = this.states[randomIndex];
        const stateName = randomState.state;

        // Add a fun visual feedback
        const randomBtn = document.getElementById('btn-random-monument');
        if (randomBtn) {
            randomBtn.textContent = '🎲 Finding...';
            randomBtn.classList.add('active');
        }

        // Briefly zoom out first for dramatic effect, then fly in
        this.map.flyTo([22.5, 82.5], 4, { duration: 0.8 });
        await new Promise(resolve => setTimeout(resolve, 900));

        // Now select the random state
        this.selectState(stateName);

        // Open the marker popup
        setTimeout(() => {
            const markerData = this.markers.find(m => m.stateName === stateName);
            if (markerData) {
                markerData.marker.openPopup();
            }
            if (randomBtn) {
                randomBtn.textContent = '🎲 Surprise Me';
                randomBtn.classList.remove('active');
            }
        }, 2000);
    }

    // Parallax effect for the map wrapper on scroll
    setupParallax() {
        const wrapper = document.getElementById('map-wrapper');
        if (!wrapper) return;

        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    const rect = wrapper.getBoundingClientRect();
                    const windowHeight = window.innerHeight;
                    const visible = rect.top < windowHeight && rect.bottom > 0;

                    if (visible) {
                        // Calculate parallax offset based on position in viewport
                        const progress = (windowHeight - rect.top) / (windowHeight + rect.height);
                        const parallaxY = (progress - 0.5) * 15;
                        const rotateX = (progress - 0.5) * 1.5;

                        wrapper.style.transform = `perspective(1200px) translateY(${parallaxY}px) rotateX(${rotateX}deg)`;

                        // Dynamic shadow depth based on scroll position
                        const shadowDepth = 20 + Math.abs(parallaxY);
                        wrapper.style.boxShadow = `0 ${shadowDepth}px ${shadowDepth * 2.5}px rgba(0,0,0,${0.15 + Math.abs(parallaxY) * 0.003})`;
                    }

                    ticking = false;
                });
                ticking = true;
            }
        });
    }

    resetView() {
        // Clear monument markers
        this.monumentMarkers.forEach(m => this.map.removeLayer(m));
        this.monumentMarkers = [];
        this.selectedState = null;

        // Reset map wrapper parallax transform
        const wrapper = document.getElementById('map-wrapper');
        if (wrapper) {
            wrapper.style.transition = 'transform 0.5s ease, box-shadow 0.5s ease';
            wrapper.style.transform = 'perspective(1200px) translateY(0) rotateX(0)';
            setTimeout(() => { wrapper.style.transition = ''; }, 600);
        }

        // Reset to India view with smooth animation
        this.map.flyTo([22.5, 82.5], 5, {
            duration: 1.8,
            easeLinearity: 0.25
        });
    }
}

// Global map instance
let indiaMap = null;

async function initializeIndiaMap(containerId = 'india-map-container') {
    console.log('Initializing India map with Leaflet...');
    indiaMap = new IndiaMap(containerId);
    return indiaMap;
}
