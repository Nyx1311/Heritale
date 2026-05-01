#  Heritale (AI Heritage Storyteller)

An interactive, multilingual web application that transforms Indian monuments into engaging storytelling experiences using AI, featuring real maps, image galleries, and audio narration.

## 🎯 Project Status: Phase 6 Complete ✨

### ✅ Phase 1 - Core Infrastructure (Complete)
- Project structure setup
- Flask web server
- SQLite database with models
- API endpoints for monuments and stories
- Basic frontend with HTML/CSS/JS
- **104 monuments across all 36 Indian states/UTs**

### ✅ Phase 2 - AI Story Generation (Complete)
- LLaMA 3.2 integration via Ollama
- Intelligent prompt engineering for storytelling
- Context-aware narrative generation
- **"Once upon a time" narrative style**
- User story integration in AI prompts
- Story caching for performance

### ✅ Phase 3 - Audio Generation (Complete)
- gTTS (Google Text-to-Speech) integration
- Automatic audio generation from stories
- MP3 audio file generation
- Audio caching system
- Auto-play functionality in frontend

### ✅ Phase 4 - Multilingual Translation (Complete)
- Google Translate API integration
- Support for 7 languages (English + 6 Indian languages)
- Translation caching for performance
- Functional language selector with localStorage
- Audio generation in all supported languages

### ✅ Phase 5 - Voice Input (Complete)
- Browser-based speech recognition (Web Speech API)
- Microphone recording UI with visual feedback
- Real-time voice-to-text transcription
- Support for all 7 languages in voice input
- Automatic language detection
- Translation of voice submissions to English

### ✅ Phase 6 - Interactive Map & Community Features (Complete)
- **Real geographical map** using Leaflet.js + OpenStreetMap
- **Dynamic state markers** with monument counts
- **GPS coordinates** for all 36 states
- **Clickable markers** to view monuments by state
- **Community stories section** - users can view and post stories
- **Automatic image gallery** from Wikipedia/Wikimedia Commons
- **Lightbox viewer** with slideshow navigation
- **Hero image display** with full gallery access

## 📁 Project Structure

```
ai-heritage-storyteller/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── seed_data.py            # Database seeding script
├── requirements.txt        # Python dependencies
├── database/
│   ├── db.py              # Database connection
│   └── models.py          # SQLAlchemy models
├── routes/
│   ├── monument_routes.py # Monument API endpoints
│   ├── page_routes.py     # Page rendering routes  
│   ├── story_routes.py    # Story generation endpoints
│   └── user_input_routes.py # User submission endpoints
├── services/
│   ├── __init__.py        # Services package
│   └── image_service.py   # Wikipedia image fetching
├── translation/
│   ├── __init__.py        # Translation package
│   └── translate_service.py # Google Translate integration
├── static/
│   ├── css/style.css      # Styling
│   ├── js/
│   │   ├── main.js        # Home page & map logic
│   │   └── story.js       # Story page & gallery
│   ├── images/            # SVG placeholders
│   └── audio/             # Generated audio files (auto-created)
└── templates/
    ├── index.html         # Home page with map
    └── story.html         # Story page with gallery
```

## 🚀 Quick Start

> **📖 For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

### Prerequisites
- Python 3.9+
- **Ollama with llama3.2 model installed**
- Internet connection (for Wikipedia images & translation)

### 1. Install Ollama
```powershell
# Download from https://ollama.ai
# Pull llama3.2 model
ollama pull llama3.2
```

### 2. Install Python Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install requirements
pip install -r requirements.txt
```

### 3. Initialize Database

```powershell
python seed_monuments.py
```

### 4. Run Application

```powershell
# Make sure Ollama is running
ollama serve  # Run in separate terminal if needed

# Start Flask app
python app.py
```

### 5. Open Browser

Navigate to: `http://localhost:5000`

---

## 🎨 Features

### Interactive Map
- ✅ Real geographical map using Leaflet.js + OpenStreetMap
- ✅ 36 state markers with monument counts
- ✅ Click any state to view monuments
- ✅ No API key required (free OpenStreetMap tiles)

### Monument Discovery
- ✅ 104 monuments across all Indian states/UTs
- ✅ Browse monuments by state
- ✅ View detailed monument information
- ✅ Automatic Wikipedia image galleries (6 photos per monument)
- ✅ Hero image with lightbox viewer
- ✅ Slideshow navigation (arrows & keyboard)

### AI Storytelling
- ✅ LLaMA 3.2 powered narrative generation
- ✅ "Once upon a time" storytelling style
- ✅ Context-aware stories using historical facts
- ✅ Community stories integration
- ✅ Smart caching for performance

### Audio Narration
- ✅ Automatic text-to-speech with gTTS
- ✅ Audio in all 7 supported languages
- ✅ Auto-play functionality
- ✅ Audio caching

### Multilingual Support
- ✅ 7 languages: English, Hindi, Telugu, Tamil, Bengali, Marathi, Gujarati
- ✅ Translated stories and audio
- ✅ Language selector with persistence
- ✅ Google Translate API integration

### Community Features
- ✅ Submit text stories
- ✅ Voice recording (Web Speech API)
- ✅ Real-time voice transcription
- ✅ View community stories on monument pages
- ✅ Automatic language detection

### User Experience
- ✅ Heritage-themed responsive UI
- ✅ Image gallery with full-screen viewer
- ✅ Keyboard navigation (arrows, ESC)
- ✅ Mobile-friendly design
- ✅ Loading states & error handling

## 📚 API Endpoints

### Monuments
- `GET /api/states` - Get all states with monument counts
- `GET /api/monuments/<state>` - Get monuments by state
- `GET /api/monument/<id>` - Get single monument details
- `GET /api/monument/<id>/image` - Get main monument image from Wikipedia
- `GET /api/monument/<id>/gallery` - Get image gallery (6 photos)

### Stories
- `GET /api/story/<monument_id>?language=en` - Generate/retrieve story with audio
- `GET /api/story/<monument_id>?language=en&regenerate=true` - Force regenerate

### User Input
- `POST /api/upload/text` - Submit text story
- `POST /api/upload/audio` - Submit voice story
- `GET /api/user-stories/<monument_id>` - Get community stories

### Pages
- `GET /` - Home page with interactive map
- `GET /story?monument_id=<id>&language=<lang>` - Story page with gallery

## 🗄️ Database Schema

### Monuments Table
- `id` - Primary key
- `name` - Monument name
- `state` - Indian state/UT
- `location` - City/district
- `year_built` - Construction year
- `official_description` - Historical information
- `created_at` - Timestamp

### User Stories Table
- `id` - Primary key
- `monument_id` - Foreign key to monuments
- `user_text` - Story text
- `user_audio_path` - Voice recording path
- `detected_language` - Auto-detected language
- `translated_english_text` - English translation
- `is_approved` - Moderation status
- `created_at` - Timestamp

### Generated Stories Table
- `id` - Primary key
- `monument_id` - Foreign key to monuments
- `language` - Language code (en, hi, te, ta, bn, mr, gu)
- `story_text` - AI-generated story
- `audio_path` - TTS audio file path
- `play_count` - Usage statistics
- `generated_at` - Timestamp

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.23
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Map**: Leaflet.js 1.9.4 + OpenStreetMap
- **AI**: LLaMA 3.2 (via Ollama)
- **TTS**: gTTS 2.5.0 (Google Text-to-Speech)
- **Translation**: googletrans 4.0.0-rc1
- **Images**: Wikipedia/Wikimedia Commons API
- **Voice**: Web Speech API (Browser-based)
- **HTTP**: requests 2.31.0

### Key Libraries
```
Flask==3.0.0
SQLAlchemy==2.0.23
gTTS==2.5.0
googletrans==4.0.0-rc1
requests==2.31.0
```

## 🌐 Supported Languages

- 🇬🇧 English
- 🇮🇳 हिंदी (Hindi)
- 🇮🇳 తెలుగు (Telugu)  
- 🇮🇳 தமிழ் (Tamil)
- 🇮🇳 বাংলা (Bengali)
- 🇮🇳 मराठी (Marathi)
- 🇮🇳 ગુજરાતી (Gujarati)

## 📝 Development Notes

This project showcases:
- ✨ AI-powered cultural preservation
- 🌍 Multilingual content generation (7 languages)
- 🎵 Audio-first user experience
- 🗺️ Interactive geographical mapping
- 🖼️ Automatic image curation from Wikipedia
- 👥 Community-driven storytelling
- 📱 Responsive, mobile-friendly design

## 🎓 Educational Purpose

Built for heritage preservation and cultural education. Demonstrates:
- Natural Language Processing with LLaMA
- Text-to-Speech systems
- Translation technologies
- RESTful API design
- Modern web development
- Wikipedia API integration
- Interactive mapping with Leaflet.js

## 📊 Project Statistics

- **104 monuments** across all Indian states
- **36 states/UTs** covered
- **7 languages** supported
- **6 images per monument** (auto-fetched)
- **Free & open-source** - no API keys required for core features

## 🚀 Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for:
- Complete step-by-step setup guide
- System requirements
- Troubleshooting tips
- Production deployment options
- Mobile/network access instructions

## 🤝 Contributing

This project is complete and functional. Feel free to:
- Fork and customize for your region/monuments
- Add more monuments to the database
- Enhance UI/UX features
- Improve AI prompts
- Add more languages

## 📄 License

Open Source (MIT)

## 🙏 Acknowledgments

- Ollama team for LLaMA integration
- OpenStreetMap contributors
- Wikipedia/Wikimedia Commons
- Google Translate & gTTS
- Indian heritage preservation community

---

**Status**: All Phases Complete ✅  
**Version**: 1.0  
**Last Updated**: February 2026

**Features**: Interactive Map | AI Stories | Audio Narration | 7 Languages | Image Galleries | Community Stories

Credits:
A. NEELU
SYYEDA UZMA
ZUMAR SANIA
