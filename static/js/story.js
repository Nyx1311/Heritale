// Story Page JavaScript - Immersive Monument Experience

let currentMonumentId = null;
let currentMonumentName = '';

// Get URL parameters
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Load page on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
    currentMonumentId = getUrlParameter('monument_id');
    const language = getUrlParameter('language') || 'en';

    if (currentMonumentId) {
        document.getElementById('language').value = language;
        loadMonument(currentMonumentId);
        loadStory();
        loadUserStories(currentMonumentId);
    } else {
        alert('No monument selected');
        window.location.href = '/';
    }

    // Setup form submission
    document.getElementById('story-form').addEventListener('submit', submitStory);

    // Setup voice recording (Phase 5)
    setupVoiceRecording();

    // Setup parallax scroll for hero banner
    setupHeroParallax();
});

// Load monument details
async function loadMonument(monumentId) {
    try {
        const response = await fetch(`/api/monument/${monumentId}`);
        const data = await response.json();

        if (data.success) {
            const monument = data.monument;
            currentMonumentName = monument.name;
            document.getElementById('monument-name').textContent = monument.name;
            document.getElementById('monument-location').textContent =
                `${monument.location || ''} • ${monument.state} • ${monument.year_built || ''}`;

            // Update page title
            document.title = `${monument.name} - AI Heritage Storyteller`;

            // Load monument gallery and set immersive background
            loadMonumentGallery(monumentId);
        }
    } catch (error) {
        console.error('Error loading monument:', error);
    }
}

// Load monument image gallery and set immersive visuals
let galleryImages = [];
let currentImageIndex = 0;

async function loadMonumentGallery(monumentId) {
    try {
        const response = await fetch(`/api/monument/${monumentId}/gallery`);
        const data = await response.json();

        if (data.success && data.images && data.images.length > 0) {
            galleryImages = data.images;

            // Set the hero banner image (main immersive visual)
            const bannerImg = document.getElementById('hero-banner-img');
            const imageCount = document.getElementById('image-count');
            const galleryBadge = document.getElementById('hero-gallery-badge');

            bannerImg.src = galleryImages[0];
            bannerImg.alt = currentMonumentName;
            imageCount.textContent = galleryImages.length;
            galleryBadge.style.display = 'inline-flex';

            // Set immersive blurred background from the same image
            setImmersiveBackground(galleryImages[0]);

            // Extract dominant color and apply adaptive theme
            bannerImg.crossOrigin = 'anonymous';
            bannerImg.onload = function () {
                extractAndApplyTheme(bannerImg);
            };
        } else {
            // No images: use fallback gradient, hide gallery badge
            document.getElementById('monument-hero-banner').classList.add('no-image');
        }
    } catch (error) {
        console.error('Error loading monument gallery:', error);
        document.getElementById('monument-hero-banner').classList.add('no-image');
    }
}

// Set the full-page blurred background from monument image
function setImmersiveBackground(imageUrl) {
    const bg = document.getElementById('immersive-bg');
    if (bg) {
        bg.style.backgroundImage = `url('${imageUrl}')`;
        bg.classList.add('loaded');
    }
}

// Extract a dominant color from the hero image and apply it as page accent
function extractAndApplyTheme(imgElement) {
    try {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 50;
        canvas.height = 50;
        ctx.drawImage(imgElement, 0, 0, 50, 50);

        const imageData = ctx.getImageData(0, 0, 50, 50).data;

        // Sample pixels at strategic positions to get representative colors
        let rTotal = 0, gTotal = 0, bTotal = 0, samples = 0;

        // Sample from regions that are likely to be the monument (center, lower third)
        for (let y = 15; y < 45; y += 2) {
            for (let x = 10; x < 40; x += 2) {
                const i = (y * 50 + x) * 4;
                const r = imageData[i];
                const g = imageData[i + 1];
                const b = imageData[i + 2];

                // Skip very dark (shadows) and very bright (sky) pixels
                const brightness = (r + g + b) / 3;
                if (brightness > 30 && brightness < 220) {
                    rTotal += r;
                    gTotal += g;
                    bTotal += b;
                    samples++;
                }
            }
        }

        if (samples > 0) {
            const r = Math.round(rTotal / samples);
            const g = Math.round(gTotal / samples);
            const b = Math.round(bTotal / samples);

            // Set CSS custom properties for adaptive theming
            const root = document.documentElement;
            root.style.setProperty('--monument-color', `rgb(${r}, ${g}, ${b})`);
            root.style.setProperty('--monument-color-light', `rgba(${r}, ${g}, ${b}, 0.15)`);
            root.style.setProperty('--monument-color-medium', `rgba(${r}, ${g}, ${b}, 0.4)`);
            root.style.setProperty('--monument-color-dark', darkenColor(r, g, b, 0.5));
            root.style.setProperty('--monument-color-glow', `rgba(${r}, ${g}, ${b}, 0.3)`);

            // Mark body as themed
            document.body.classList.add('monument-themed');
        }
    } catch (e) {
        // Cross-origin or canvas errors - silently fall back to defaults
        console.log('Color extraction unavailable (cross-origin image), using default theme.');
    }
}

function darkenColor(r, g, b, factor) {
    return `rgb(${Math.round(r * factor)}, ${Math.round(g * factor)}, ${Math.round(b * factor)})`;
}

// Parallax scroll effect for the hero banner
function setupHeroParallax() {
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrollY = window.scrollY;
                const banner = document.getElementById('monument-hero-banner');
                const bannerImg = document.getElementById('hero-banner-img');
                const bannerContent = document.querySelector('.hero-banner-content');
                const immBg = document.getElementById('immersive-bg');

                if (banner && scrollY < 800) {
                    // Parallax on hero image: moves slower than scroll
                    if (bannerImg) {
                        bannerImg.style.transform = `scale(1.15) translateY(${scrollY * 0.3}px)`;
                    }
                    // Content fades and moves up
                    if (bannerContent) {
                        const opacity = Math.max(0, 1 - scrollY / 500);
                        bannerContent.style.opacity = opacity;
                        bannerContent.style.transform = `translateY(${scrollY * 0.15}px)`;
                    }
                }

                // Background parallax
                if (immBg) {
                    immBg.style.transform = `translateY(${scrollY * 0.08}px) scale(1.1)`;
                }

                ticking = false;
            });
            ticking = true;
        }
    });
}

// Lightbox functionality
function openLightbox(index) {
    currentImageIndex = index;
    showImageInLightbox();
    document.getElementById('image-lightbox').style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeLightbox() {
    document.getElementById('image-lightbox').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function showImageInLightbox() {
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxCounter = document.getElementById('lightbox-counter');

    lightboxImage.src = galleryImages[currentImageIndex];
    lightboxCounter.textContent = `${currentImageIndex + 1} / ${galleryImages.length}`;
}

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
    showImageInLightbox();
}

function prevImage() {
    currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
    showImageInLightbox();
}

// Setup lightbox event listeners
document.addEventListener('DOMContentLoaded', function () {
    // Close button
    const closeBtn = document.querySelector('.lightbox-close');
    if (closeBtn) {
        closeBtn.onclick = closeLightbox;
    }

    // Next/Prev buttons
    const nextBtn = document.querySelector('.lightbox-next');
    const prevBtn = document.querySelector('.lightbox-prev');

    if (nextBtn) nextBtn.onclick = nextImage;
    if (prevBtn) prevBtn.onclick = prevImage;

    // Close on background click
    const lightbox = document.getElementById('image-lightbox');
    if (lightbox) {
        lightbox.onclick = function (e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        };
    }

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        const lightbox = document.getElementById('image-lightbox');
        if (lightbox.style.display === 'flex') {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowRight') nextImage();
            if (e.key === 'ArrowLeft') prevImage();
        }
    });
});

// Load and display story
async function loadStory() {
    const language = document.getElementById('language').value;
    const storyText = document.getElementById('story-text');
    const loading = document.getElementById('loading');

    storyText.style.display = 'none';
    loading.style.display = 'block';

    // Update loading message
    loading.innerHTML = '<p>✨ Generating your story...</p><p style="font-size: 0.9rem;">This may take 20-40 seconds for first generation</p>';

    try {
        const response = await fetch(`/api/story/${currentMonumentId}?language=${language}`);
        const data = await response.json();

        loading.style.display = 'none';
        storyText.style.display = 'block';

        if (data.success) {
            storyText.innerHTML = `<p>${data.story.story_text}</p>`;

            // Handle audio playback (Phase 3 & 4)
            const audioPath = data.story.audio_path;

            if (audioPath && audioPath !== null && audioPath !== '') {
                const audioPlayer = document.getElementById('audio-player');
                const audioElement = document.getElementById('story-audio');
                const audioPlaceholder = document.getElementById('audio-placeholder');

                audioElement.src = `/static/audio/${audioPath}`;
                audioPlayer.style.display = 'block';
                audioPlaceholder.style.display = 'none';

                // Auto-play audio (if browser allows)
                audioElement.play().catch(err => {
                    console.log('Auto-play prevented by browser. User must click play.', err);
                });

                // Show audio success message
                storyText.innerHTML += '<p style="color: #2E7D32; font-style: italic; margin-top: 1rem;">🎵 Audio narration playing!</p>';
            } else {
                // Audio not available
                const audioPlaceholder = document.getElementById('audio-placeholder');
                audioPlaceholder.innerHTML = '<p>⚠️ Audio generation failed or is unavailable. Showing text version.</p>';
                audioPlaceholder.style.display = 'block';
                document.getElementById('audio-player').style.display = 'none';
            }

            // Show note if it's cached
            if (data.cached) {
                storyText.innerHTML += '<p style="color: #CC5500; font-style: italic; margin-top: 1rem;">✓ Previously generated story</p>';
            }

            if (data.note) {
                storyText.innerHTML += `<p style="color: #D2691E; font-style: italic; margin-top: 1rem;">📝 ${data.note}</p>`;
            }

            // Show generation stats
            if (data.user_stories_included > 0) {
                storyText.innerHTML += `<p style="color: #1976D2; font-size: 0.9rem; margin-top: 1rem;">👥 Includes ${data.user_stories_included} community ${data.user_stories_included === 1 ? 'story' : 'stories'}</p>`;
            }
        } else {
            storyText.innerHTML = `<p style="color: red;">Error loading story: ${data.error}</p>`;
        }
    } catch (error) {
        loading.style.display = 'none';
        storyText.style.display = 'block';
        storyText.innerHTML = '<p style="color: red;">Error loading story. Please try again.</p>';
        console.error('Error:', error);
    }
}

// Submit user story
async function submitStory(event) {
    event.preventDefault();

    const userStory = document.getElementById('user-story').value.trim();
    const resultDiv = document.getElementById('submission-result');
    const currentLanguage = document.getElementById('language').value;

    if (!userStory) {
        resultDiv.className = 'error';
        resultDiv.textContent = 'Please enter your story first.';
        return;
    }

    try {
        const response = await fetch('/api/upload/text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                monument_id: currentMonumentId,
                user_text: userStory,
                language: currentLanguage
            })
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.className = 'success';
            resultDiv.textContent = '✓ Thank you! Your story has been submitted successfully!';
            document.getElementById('user-story').value = '';

            // Reload user stories to show the new one
            setTimeout(() => {
                loadUserStories(currentMonumentId);
                // Scroll to stories section
                document.querySelector('.user-stories-section').scrollIntoView({
                    behavior: 'smooth',
                    block: 'nearest'
                });
            }, 500);
        } else {
            resultDiv.className = 'error';
            resultDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        resultDiv.className = 'error';
        resultDiv.textContent = 'Error submitting story. Please try again.';
        console.error('Error:', error);
    }
}

// Load user stories/comments
async function loadUserStories(monumentId) {
    const container = document.getElementById('user-stories-container');
    const noStoriesDiv = document.getElementById('no-stories');

    try {
        const response = await fetch(`/api/user-stories/${monumentId}`);
        const data = await response.json();

        if (data.success && data.stories.length > 0) {
            container.innerHTML = ''; // Clear loading message
            noStoriesDiv.style.display = 'none';

            // Update section header with count
            const header = document.querySelector('.user-stories-section h3');
            header.innerHTML = `💬 Community Stories <span class="story-count">${data.count}</span>`;

            // Display each story
            data.stories.forEach(story => {
                const storyCard = createStoryCard(story);
                container.appendChild(storyCard);
            });
        } else {
            container.innerHTML = '';
            noStoriesDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading user stories:', error);
        container.innerHTML = '<p class="error">Failed to load community stories.</p>';
    }
}

// Create story card element
function createStoryCard(story) {
    const card = document.createElement('div');
    card.className = 'story-card';

    // Format date
    const date = new Date(story.created_at);
    const formattedDate = date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });

    // Language names
    const languageNames = {
        'en': 'English',
        'hi': 'Hindi',
        'te': 'Telugu',
        'ta': 'Tamil',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'gu': 'Gujarati'
    };

    const languageName = languageNames[story.detected_language] || story.detected_language;

    // Approval status indicator
    const statusBadge = story.is_approved === 0
        ? '<span style="background: #FF9800; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-left: 0.5rem;">Pending Review</span>'
        : '';

    card.innerHTML = `
        <div class="story-header">
            <div class="story-meta">
                <span class="story-author">🙋 Anonymous Visitor</span>
                <span class="story-date">📅 ${formattedDate}</span>
            </div>
            <div>
                <span class="story-language">🌐 ${languageName}</span>
                ${statusBadge}
            </div>
        </div>
        <div class="story-content">
            <p>${escapeHtml(story.user_text)}</p>
        </div>
    `;

    return card;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Voice Recording Functionality (Phase 5)
let recognition = null;
let isRecording = false;
let finalTranscript = '';

function setupVoiceRecording() {
    const startBtn = document.getElementById('start-recording');
    const stopBtn = document.getElementById('stop-recording');
    const status = document.getElementById('recording-status');
    const transcriptDiv = document.getElementById('voice-transcript');
    const transcriptText = document.getElementById('transcript-text');

    // Check if browser supports Web Speech API
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        startBtn.disabled = true;
        startBtn.textContent = '❌ Voice recording not supported in this browser';
        startBtn.style.background = '#999';
        return;
    }

    // Initialize speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();

    // Get current language from selector
    const currentLang = document.getElementById('language').value;
    const langMap = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'te': 'te-IN',
        'ta': 'ta-IN',
        'bn': 'bn-IN',
        'mr': 'mr-IN',
        'gu': 'gu-IN'
    };

    recognition.lang = langMap[currentLang] || 'en-US';
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    // Start recording
    startBtn.addEventListener('click', function () {
        if (!isRecording) {
            finalTranscript = '';
            transcriptText.textContent = '';
            transcriptDiv.style.display = 'none';

            try {
                recognition.start();
                isRecording = true;
                startBtn.style.display = 'none';
                stopBtn.style.display = 'inline-block';
                status.textContent = '🔴 Recording...';
                status.style.display = 'inline';
            } catch (error) {
                console.error('Error starting recognition:', error);
                alert('Error starting voice recording. Please try again.');
            }
        }
    });

    // Stop recording
    stopBtn.addEventListener('click', function () {
        if (isRecording) {
            recognition.stop();
            isRecording = false;
            stopBtn.style.display = 'none';
            startBtn.style.display = 'inline-block';
            status.textContent = '';
            status.style.display = 'none';
        }
    });

    // Handle speech recognition results
    recognition.onresult = function (event) {
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;

            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        // Display transcript
        transcriptDiv.style.display = 'block';
        transcriptText.textContent = finalTranscript + interimTranscript;
    };

    // Handle errors
    recognition.onerror = function (event) {
        console.error('Speech recognition error:', event.error);
        isRecording = false;
        stopBtn.style.display = 'none';
        startBtn.style.display = 'inline-block';
        status.textContent = '';
        status.style.display = 'none';

        let errorMessage = 'Voice recording error. ';
        if (event.error === 'no-speech') {
            errorMessage += 'No speech detected. Please try again.';
        } else if (event.error === 'audio-capture') {
            errorMessage += 'Microphone not available.';
        } else if (event.error === 'not-allowed') {
            errorMessage += 'Microphone permission denied.';
        } else {
            errorMessage += event.error;
        }

        alert(errorMessage);
    };

    // Handle end of recognition
    recognition.onend = function () {
        isRecording = false;
        stopBtn.style.display = 'none';
        startBtn.style.display = 'inline-block';
        status.textContent = '';
        status.style.display = 'none';

        // If we have a transcript, copy it to the text area
        if (finalTranscript.trim()) {
            document.getElementById('user-story').value = finalTranscript.trim();
            transcriptDiv.style.display = 'block';
            transcriptText.textContent = finalTranscript.trim();

            // Show success message
            const resultDiv = document.getElementById('submission-result');
            resultDiv.className = 'success';
            resultDiv.textContent = '✓ Voice transcribed! You can edit the text below before submitting.';

            // Clear message after 5 seconds
            setTimeout(() => {
                resultDiv.textContent = '';
                resultDiv.className = '';
            }, 5000);
        }
    };

    // Update language when selector changes
    document.getElementById('language').addEventListener('change', function () {
        const newLang = this.value;
        recognition.lang = langMap[newLang] || 'en-US';
    });
}
