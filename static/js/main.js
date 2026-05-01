// Main JavaScript for Index Page

// Load states on page load
document.addEventListener('DOMContentLoaded', function () {
    initializeLanguageSelector();
    initializeIndiaMap('india-map-container');
});

// Initialize language selector
function initializeLanguageSelector() {
    const languageSelect = document.getElementById('language');

    // Load saved language preference
    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    languageSelect.value = savedLanguage;

    // Handle language change
    languageSelect.addEventListener('change', function () {
        const selectedLang = this.value;
        const selectedText = this.options[this.selectedIndex].text;

        // Save to localStorage
        localStorage.setItem('selectedLanguage', selectedLang);

        // Show notification
        showNotification(`Language changed to ${selectedText}`);
    });
}

// Show notification message - Enhanced Heritage Style
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        background: linear-gradient(135deg, #654321, #8B4513);
        color: white;
        padding: 16px 24px;
        border-radius: 14px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3), 0 0 20px rgba(212,175,55,0.2);
        z-index: 10000;
        font-weight: 500;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        letter-spacing: 0.3px;
        border: 2px solid rgba(212,175,55,0.4);
        animation: notifSlideIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
        max-width: 380px;
    `;
    notification.textContent = message;

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes notifSlideIn {
            from { transform: translateX(420px) scale(0.8); opacity: 0; }
            to { transform: translateX(0) scale(1); opacity: 1; }
        }
        @keyframes notifSlideOut {
            from { transform: translateX(0) scale(1); opacity: 1; }
            to { transform: translateX(420px) scale(0.8); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'notifSlideOut 0.4s cubic-bezier(0.6,-0.28,0.735,0.045) forwards';
        setTimeout(() => notification.remove(), 400);
    }, 3000);
}

// Load all states
async function loadStates() {
    try {
        const response = await fetch('/api/states');
        const data = await response.json();

        const statesContainer = document.getElementById('states-container');

        if (data.success && data.states.length > 0) {
            statesContainer.innerHTML = '';

            data.states.forEach(state => {
                const stateCard = document.createElement('div');
                stateCard.className = 'state-card';
                stateCard.textContent = state;
                stateCard.onclick = () => loadMonuments(state);
                statesContainer.appendChild(stateCard);
            });
        } else {
            statesContainer.innerHTML = '<p>No states found. Please add monuments to the database.</p>';
        }
    } catch (error) {
        console.error('Error loading states:', error);
        document.getElementById('states-container').innerHTML =
            '<p style="color: red;">Error loading states. Please try again.</p>';
    }
}

// Load monuments for a selected state
async function loadMonuments(state) {
    try {
        const response = await fetch(`/api/monuments/${state}`);
        const data = await response.json();

        const monumentsSection = document.getElementById('monuments-section');
        const selectedState = document.getElementById('selected-state');
        const monumentsContainer = document.getElementById('monuments-container');

        selectedState.textContent = state;
        monumentsSection.style.display = 'block';

        if (data.success && data.monuments.length > 0) {
            monumentsContainer.innerHTML = '';

            data.monuments.forEach(async (monument, index) => {
                const monumentCard = document.createElement('div');
                monumentCard.className = 'monument-card';
                monumentCard.style.opacity = '0';
                monumentCard.style.transform = 'translateY(30px)';
                monumentCard.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
                monumentCard.innerHTML = `
                    <div class="monument-image-container">
                        <img src="/static/images/loading.svg" alt="Loading..." class="monument-image">
                    </div>
                    <div class="monument-content">
                        <h3>${monument.name}</h3>
                        <p><strong>Location:</strong> ${monument.location || 'N/A'}</p>
                        <p><strong>Year Built:</strong> ${monument.year_built || 'N/A'}</p>
                        <p>${monument.official_description.substring(0, 150)}...</p>
                    </div>
                `;
                monumentCard.onclick = () => viewStory(monument.id);
                monumentsContainer.appendChild(monumentCard);

                // Trigger staggered fade-in animation
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        monumentCard.style.opacity = '1';
                        monumentCard.style.transform = 'translateY(0)';
                    });
                });

                // Fetch and load image
                try {
                    const imageResponse = await fetch(`/api/monument/${monument.id}/image`);
                    const imageData = await imageResponse.json();

                    const imgElement = monumentCard.querySelector('.monument-image');
                    if (imageData.success && imageData.image_url) {
                        imgElement.src = imageData.image_url;
                        imgElement.alt = monument.name;
                    } else {
                        imgElement.src = '/static/images/default-monument.svg';
                        imgElement.alt = 'Monument placeholder';
                    }
                } catch (error) {
                    console.error('Error loading image:', error);
                    const imgElement = monumentCard.querySelector('.monument-image');
                    imgElement.src = '/static/images/default-monument.svg';
                    imgElement.alt = 'Monument placeholder';
                }
            });
        } else {
            monumentsContainer.innerHTML = `<p>No monuments found in ${state}</p>`;
        }

        // Scroll to monuments section
        monumentsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error loading monuments:', error);
    }
}

// View story for a monument
function viewStory(monumentId) {
    const language = localStorage.getItem('selectedLanguage') || 'en';
    window.location.href = `/story?monument_id=${monumentId}&language=${language}`;
}
