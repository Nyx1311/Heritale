"""
Seed script to populate the database with comprehensive monument data
Covers all states and union territories of India with major heritage sites
"""

from database.db import db_session, init_db
from database.models import Monument

def seed_monuments():
    """Add comprehensive monument data to the database"""
    
    init_db()
    
    # Check if monuments already exist
    existing_count = db_session.query(Monument).count()
    if existing_count > 0:
        print(f"Database already has {existing_count} monuments.")
        response = input("Do you want to clear and reseed? (yes/no): ")
        if response.lower() != 'yes':
            print("Seeding cancelled.")
            return
        
        # Clear existing data
        db_session.query(Monument).delete()
        db_session.commit()
        print("Cleared existing monuments.")
    
    monuments_data = [
        # DELHI
        {
            'name': 'Red Fort',
            'state': 'Delhi',
            'location': 'Netaji Subhash Marg, Chandni Chowk',
            'year_built': '1648',
            'official_description': 'A magnificent 17th-century fort complex built by Mughal Emperor Shah Jahan. This UNESCO World Heritage Site served as the main residence of Mughal emperors for nearly 200 years. Its red sandstone walls stretch for 2.5 km and rise to 18 meters. The fort houses palaces, mosques, and halls showcasing the zenith of Mughal architecture.'
        },
        {
            'name': 'Qutub Minar',
            'state': 'Delhi',
            'location': 'Mehrauli',
            'year_built': '1193',
            'official_description': 'The tallest brick minaret in the world, standing at 72.5 meters. This UNESCO World Heritage Site was built by Qutub-ud-din Aibak and is made of red sandstone and marble. The complex includes the Iron Pillar, which has stood without rusting for over 1,600 years, demonstrating ancient Indian metallurgical prowess.'
        },
        {
            'name': 'Humayun\'s Tomb',
            'state': 'Delhi',
            'location': 'Nizamuddin East',
            'year_built': '1570',
            'official_description': 'The tomb of Mughal Emperor Humayun, commissioned by his wife Hamida Banu Begum. This UNESCO World Heritage Site is the first garden-tomb on the Indian subcontinent and inspired the construction of the Taj Mahal. Built in red sandstone and white marble, it represents the pinnacle of Mughal architecture.'
        },
        {
            'name': 'India Gate',
            'state': 'Delhi',
            'location': 'Rajpath',
            'year_built': '1931',
            'official_description': 'A war memorial dedicated to 70,000 Indian soldiers who died in World War I. Designed by Sir Edwin Lutyens, this 42-meter high arch is made of red and yellow sandstone. The Amar Jawan Jyoti (eternal flame) burns at the base to honor unknown soldiers.'
        },
        {
            'name': 'Lotus Temple',
            'state': 'Delhi',
            'location': 'Bahapur',
            'year_built': '1986',
            'official_description': 'A Baháʼí House of Worship notable for its flowerlike shape, made of 27 free-standing marble-clad petals. It has won numerous architectural awards and attracts millions of visitors annually. The temple is open to all religions and serves as a place for meditation and peace.'
        },
        
        # UTTAR PRADESH
        {
            'name': 'Taj Mahal',
            'state': 'Uttar Pradesh',
            'location': 'Agra',
            'year_built': '1653',
            'official_description': 'One of the Seven Wonders of the World and a UNESCO World Heritage Site. Built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal, this ivory-white marble mausoleum took 22 years and 20,000 artisans to complete. It represents the finest example of Mughal architecture, combining elements from Islamic, Persian, and Indian styles.'
        },
        {
            'name': 'Agra Fort',
            'state': 'Uttar Pradesh',
            'location': 'Agra',
            'year_built': '1573',
            'official_description': 'A UNESCO World Heritage Site built by Emperor Akbar in red sandstone. This massive fort complex served as the main residence of Mughal emperors until 1638. The fort contains palaces, mosques, and audience halls showcasing Mughal grandeur and is located just 2.5 km from the Taj Mahal.'
        },
        {
            'name': 'Fatehpur Sikri',
            'state': 'Uttar Pradesh',
            'location': 'Fatehpur Sikri',
            'year_built': '1571',
            'official_description': 'Built by Emperor Akbar as his capital, this UNESCO World Heritage Site is a perfectly preserved Mughal city frozen in time. The red sandstone complex includes palaces, courts, mosques, and the famous Buland Darwaza (Gate of Victory), the highest gateway in the world.'
        },
        {
            'name': 'Varanasi Ghats',
            'state': 'Uttar Pradesh',
            'location': 'Varanasi',
            'year_built': 'Ancient',
            'official_description': 'One of the oldest continuously inhabited cities in the world. The 88 ghats along the Ganges River are sacred to Hindus and witness thousands of pilgrims daily. The evening Ganga Aarti at Dashashwamedh Ghat is a spectacular spiritual ceremony that has been performed for centuries.'
        },
        {
            'name': 'Sarnath',
            'state': 'Uttar Pradesh',
            'location': 'Varanasi',
            'year_built': '3rd Century BCE',
            'official_description': 'The place where Lord Buddha gave his first sermon after attaining enlightenment. The Dhamek Stupa, standing at 43.6 meters, marks the spot. Emperor Ashoka erected pillars here, and the site contains ruins of monasteries and temples from various periods of Buddhist history.'
        },
        
        # RAJASTHAN
        {
            'name': 'Hawa Mahal',
            'state': 'Rajasthan',
            'location': 'Jaipur',
            'year_built': '1799',
            'official_description': 'The Palace of Winds, built by Maharaja Sawai Pratap Singh. This five-story pink sandstone structure features 953 small windows (jharokhas) designed to allow royal ladies to observe street festivals while remaining unseen. Its unique honeycomb facade is an iconic symbol of Jaipur.'
        },
        {
            'name': 'Amber Fort',
            'state': 'Rajasthan',
            'location': 'Jaipur',
            'year_built': '1592',
            'official_description': 'A magnificent hilltop fort built by Raja Man Singh I. Constructed in red sandstone and marble, it overlooks Maota Lake. The fort complex includes palaces, gardens, and the famous Sheesh Mahal (Mirror Palace), where a single candle can illuminate the entire hall through thousands of mirrors.'
        },
        {
            'name': 'City Palace Jaipur',
            'state': 'Rajasthan',
            'location': 'Jaipur',
            'year_built': '1732',
            'official_description': 'A magnificent complex built by Maharaja Sawai Jai Singh II. It blends Rajput, Mughal, and European architectural styles. The palace houses museums containing royal costumes, weapons, and the world\'s largest silver vessels used to carry Ganges water to England.'
        },
        {
            'name': 'Mehrangarh Fort',
            'state': 'Rajasthan',
            'location': 'Jodhpur',
            'year_built': '1459',
            'official_description': 'One of India\'s largest forts, perched 410 feet above Jodhpur. Built by Rao Jodha, its walls are up to 36 meters high and 21 meters wide. The fort houses palaces with intricate carvings and expansive courtyards, offering panoramic views of the Blue City.'
        },
        {
            'name': 'Lake Palace',
            'state': 'Rajasthan',
            'location': 'Udaipur',
            'year_built': '1746',
            'official_description': 'A stunning white marble palace built on Jag Niwas island in Lake Pichola. Commissioned by Maharana Jagat Singh II, it appears to float on water. Now a luxury hotel, it has featured in James Bond films and represents the epitome of Rajput romantic architecture.'
        },
        {
            'name': 'Jaisalmer Fort',
            'state': 'Rajasthan',
            'location': 'Jaisalmer',
            'year_built': '1156',
            'official_description': 'The Golden Fort, one of the largest fully preserved fortified cities in the world and a UNESCO World Heritage Site. Built of yellow sandstone, it appears golden in sunlight. Unique among forts, it still houses a living population of about 3,000 people within its walls.'
        },
        {
            'name': 'Jantar Mantar',
            'state': 'Rajasthan',
            'location': 'Jaipur',
            'year_built': '1734',
            'official_description': 'A UNESCO World Heritage astronomical observatory built by Maharaja Sawai Jai Singh II. It houses 19 architectural astronomical instruments including the world\'s largest stone sundial. The instruments are accurate to seconds and demonstrate ancient Indian astronomical knowledge.'
        },
        
        # MAHARASHTRA
        {
            'name': 'Gateway of India',
            'state': 'Maharashtra',
            'location': 'Mumbai',
            'year_built': '1924',
            'official_description': 'An iconic monument built to commemorate the landing of King George V and Queen Mary in India. This 26-meter high Indo-Saracenic arch stands on the waterfront in South Mumbai. It was the site of the last British troops\' departure from India in 1948, symbolizing the end of British rule.'
        },
        {
            'name': 'Ajanta Caves',
            'state': 'Maharashtra',
            'location': 'Aurangabad',
            'year_built': '2nd Century BCE',
            'official_description': 'A UNESCO World Heritage Site consisting of 30 rock-cut Buddhist cave monuments. These caves contain masterpieces of Buddhist religious art with paintings and sculptures described as among the finest surviving examples of ancient Indian art, particularly in the expressive emotions depicted on faces.'
        },
        {
            'name': 'Ellora Caves',
            'state': 'Maharashtra',
            'location': 'Aurangabad',
            'year_built': '600-1000 CE',
            'official_description': 'A UNESCO World Heritage Site featuring 34 caves representing Buddhist, Hindu, and Jain monuments. The Kailasa temple (Cave 16) is the world\'s largest monolithic rock excavation, carved from a single rock. It demonstrates remarkable engineering and architectural skills of ancient India.'
        },
        {
            'name': 'Chhatrapati Shivaji Terminus',
            'state': 'Maharashtra',
            'location': 'Mumbai',
            'year_built': '1888',
            'official_description': 'A UNESCO World Heritage Site and one of the finest examples of Victorian Gothic Revival architecture in India. Designed by Frederick William Stevens, it combines Victorian Italianate Gothic Revival with traditional Indian palace architecture. It serves over 3 million commuters daily.'
        },
        {
            'name': 'Elephanta Caves',
            'state': 'Maharashtra',
            'location': 'Mumbai Harbor',
            'year_built': '5th-8th Century',
            'official_description': 'A UNESCO World Heritage Site on Elephanta Island. The caves contain rock-cut stone sculptures dedicated to Lord Shiva. The magnificent 6-meter Trimurti (three-faced Shiva) sculpture is considered a masterpiece of ancient Indian art and attracts thousands of visitors.'
        },
        
        # WEST BENGAL
        {
            'name': 'Victoria Memorial',
            'state': 'West Bengal',
            'location': 'Kolkata',
            'year_built': '1921',
            'official_description': 'A grand marble building dedicated to Queen Victoria. Built in Indo-Saracenic revival style, it combines British and Mughal elements. The memorial houses a museum with a vast collection of artifacts, paintings, and manuscripts from the British period and is surrounded by beautiful gardens.'
        },
        {
            'name': 'Howrah Bridge',
            'state': 'West Bengal',
            'location': 'Kolkata',
            'year_built': '1943',
            'official_description': 'An iconic cantilever bridge over the Hooghly River. Built without nuts and bolts, it is held together by rivets. The bridge spans 705 meters and handles approximately 100,000 vehicles and countless pedestrians daily, making it one of the busiest bridges in the world.'
        },
        {
            'name': 'Dakshineswar Kali Temple',
            'state': 'West Bengal',
            'location': 'Kolkata',
            'year_built': '1855',
            'official_description': 'A Hindu temple dedicated to Goddess Kali. Built by Rani Rashmoni, it is famous for being the place where spiritual leader Ramakrishna Paramhansa served as a priest. The temple complex features nine spires and twelve shrines, built in traditional Bengali architectural style.'
        },
        {
            'name': 'Cooch Behar Palace',
            'state': 'West Bengal',
            'location': 'Cooch Behar',
            'year_built': '1887',
            'official_description': 'Built during the reign of Maharaja Nripendra Narayan, this palace is modeled after Buckingham Palace. It showcases Italian Renaissance architecture and houses a museum displaying royal artifacts, weapons, and period furniture. The palace is surrounded by sprawling gardens.'
        },
        
        # TELANGANA
        {
            'name': 'Charminar',
            'state': 'Telangana',
            'location': 'Hyderabad',
            'year_built': '1591',
            'official_description': 'An iconic monument built by Sultan Muhammad Quli Qutb Shah. This 56-meter high structure with four minarets was constructed to commemorate the end of a deadly plague. Built in Indo-Islamic architecture, it features ornate stucco decorations and a mosque on the top floor.'
        },
        {
            'name': 'Golconda Fort',
            'state': 'Telangana',
            'location': 'Hyderabad',
            'year_built': '13th Century',
            'official_description': 'A magnificent fortress and former diamond market known for its acoustic system and architecture. The fort was the capital of the Qutb Shahi dynasty and famous for the Koh-i-Noor and Hope diamonds that were found in its mines. The sound and light show narrates its glorious history.'
        },
        {
            'name': 'Qutb Shahi Tombs',
            'state': 'Telangana',
            'location': 'Hyderabad',
            'year_built': '1543-1672',
            'official_description': 'A magnificent necropolis of the Qutb Shahi dynasty rulers. The tombs are built on a raised platform with domes and minarets in Persian, Pathan, and Hindu architectural styles. The complex includes mosques, pavilions, and beautifully landscaped gardens.'
        },
        {
            'name': 'Warangal Fort',
            'state': 'Telangana',
            'location': 'Warangal',
            'year_built': '13th Century',
            'official_description': 'Built by the Kakatiya dynasty, this fort showcases remarkable stone gateways and intricate sculptures. The famous Warangal Gate with its ornate stone work represents the architectural brilliance of the Kakatiya period. The fort complex includes temples and stone pillars.'
        },
        
        # KARNATAKA
        {
            'name': 'Mysore Palace',
            'state': 'Karnataka',
            'location': 'Mysore',
            'year_built': '1912',
            'official_description': 'The official residence of the Wadiyar dynasty, this three-story Indo-Saracenic palace is built with fine gray granite and pink marble. Illuminated by 97,000 light bulbs on Sundays and festivals, it is one of India\'s most visited monuments. The palace houses ornate halls, paintings, and royal artifacts.'
        },
        {
            'name': 'Hampi',
            'state': 'Karnataka',
            'location': 'Bellary District',
            'year_built': '14th-16th Century',
            'official_description': 'A UNESCO World Heritage Site and former capital of the Vijayanagara Empire. Spread over 4,100 hectares, it contains over 1,600 surviving remains including temples, palaces, and market structures. The ruins showcase brilliant Dravidian architecture and engineering marvels.'
        },
        {
            'name': 'Gol Gumbaz',
            'state': 'Karnataka',
            'location': 'Bijapur',
            'year_built': '1656',
            'official_description': 'The mausoleum of Sultan Mohammed Adil Shah features the world\'s second-largest dome. The whispering gallery under the dome is famous for its acoustic properties where even the slightest whisper echoes multiple times. The structure is a masterpiece of Deccan architecture.'
        },
        {
            'name': 'Vidhana Soudha',
            'state': 'Karnataka',
            'location': 'Bangalore',
            'year_built': '1956',
            'official_description': 'The seat of Karnataka\'s state legislature. Built in Neo-Dravidian style, it is one of the largest legislative buildings in India. The granite building features intricate carvings and is illuminated in the evenings, creating a spectacular sight in the heart of Bangalore.'
        },
        
        # TAMIL NADU
        {
            'name': 'Meenakshi Temple',
            'state': 'Tamil Nadu',
            'location': 'Madurai',
            'year_built': '6th Century',
            'official_description': 'A historic Hindu temple dedicated to Goddess Meenakshi and Lord Sundareswarar. The temple complex covers 14 acres and features 14 towering gopurams (gateway towers) with thousands of colorful sculptures. It is a masterpiece of Dravidian architecture and an important pilgrimage site.'
        },
        {
            'name': 'Brihadeeswarar Temple',
            'state': 'Tamil Nadu',
            'location': 'Thanjavur',
            'year_built': '1010',
            'official_description': 'A UNESCO World Heritage Site built by Raja Raja Chola I. The temple\'s 66-meter tower (vimana) is crowned by an 80-ton monolithic granite dome. It showcases the architectural brilliance of the Chola period and represents the zenith of Dravidian temple architecture.'
        },
        {
            'name': 'Shore Temple',
            'state': 'Tamil Nadu',
            'location': 'Mahabalipuram',
            'year_built': '700-728 CE',
            'official_description': 'A UNESCO World Heritage Site built by the Pallava dynasty. This structural temple complex stands on the shore of the Bay of Bengal. It is one of the oldest stone temples in South India and features intricate carvings of Shiva and Vishnu.'
        },
        {
            'name': 'Mahabalipuram Monuments',
            'state': 'Tamil Nadu',
            'location': 'Mahabalipuram',
            'year_built': '7th-8th Century',
            'official_description': 'A UNESCO World Heritage Site featuring rock-cut temples and monolithic sculptures. The complex includes the famous Pancha Rathas (five chariots), Arjuna\'s Penance relief sculpture, and cave temples. These monuments showcase the evolution of Dravidian architecture.'
        },
        
        # GOA
        {
            'name': 'Basilica of Bom Jesus',
            'state': 'Goa',
            'location': 'Old Goa',
            'year_built': '1605',
            'official_description': 'A UNESCO World Heritage Site holding the mortal remains of St. Francis Xavier. Built in Baroque style, it is one of the finest examples of Portuguese architecture in India. The church\'s facade of Goan laterite showcases intricate carvings and Jesuit symbolism.'
        },
        {
            'name': 'Se Cathedral',
            'state': 'Goa',
            'location': 'Old Goa',
            'year_built': '1619',
            'official_description': 'The largest church in Asia dedicated to St. Catherine. Built in Portuguese-Manueline style, it houses the Golden Bell, one of the finest bells in Goa. The church features a Tuscan exterior and Corinthian interior with ornate altars and paintings.'
        },
        {
            'name': 'Aguada Fort',
            'state': 'Goa',
            'location': 'Sinquerim',
            'year_built': '1612',
            'official_description': 'A 17th-century Portuguese fort standing at the confluence of the Mandovi River and Arabian Sea. Built to defend against Dutch and Maratha invasions, it features a lighthouse, bastions, and a large freshwater storage facility. The fort offers panoramic views of the coastline.'
        },
        
        # KERALA
        {
            'name': 'Padmanabhaswamy Temple',
            'state': 'Kerala',
            'location': 'Thiruvananthapuram',
            'year_built': '8th Century',
            'official_description': 'A famous Hindu temple dedicated to Lord Vishnu, known for its intricate Dravidian architecture. The temple gained international attention when vaults containing treasures worth billions were discovered. The 100-foot tall gopuram is a landmark of Kerala architecture.'
        },
        {
            'name': 'Mattancherry Palace',
            'state': 'Kerala',
            'location': 'Kochi',
            'year_built': '1555',
            'official_description': 'Also known as the Dutch Palace, it was gifted to the Raja of Kochi by the Portuguese. The palace features Kerala murals depicting Hindu epics, royal portraits, and exhibits of royal regalia. The architecture blends European and Kerala styles.'
        },
        {
            'name': 'Bekal Fort',
            'state': 'Kerala',
            'location': 'Kasaragod',
            'year_built': '1650',
            'official_description': 'The largest fort in Kerala, built by Shivappa Nayaka. The circular fort extends over 40 acres and features a sea-facing observation tower offering panoramic views of the Arabian Sea. The fort has been featured in numerous Bollywood films.'
        },
        
        # PUNJAB
        {
            'name': 'Golden Temple',
            'state': 'Punjab',
            'location': 'Amritsar',
            'year_built': '1604',
            'official_description': 'The holiest Gurdwara of Sikhism, known as Harmandir Sahib. The temple is covered in gold foil and sits in the center of a sacred pool (Amrit Sarovar). It is open to people of all faiths and serves free meals to over 100,000 people daily in its community kitchen (langar).'
        },
        {
            'name': 'Jallianwala Bagh',
            'state': 'Punjab',
            'location': 'Amritsar',
            'year_built': 'Memorial: 1951',
            'official_description': 'A historic public garden and memorial site marking the 1919 Jallianwala Bagh massacre where British troops fired on unarmed Indian civilians. The preserved bullet marks on walls and the Martyrs\' Well serve as poignant reminders of India\'s independence struggle.'
        },
        {
            'name': 'Wagah Border',
            'state': 'Punjab',
            'location': 'Attari',
            'year_built': '1947',
            'official_description': 'The ceremonial border crossing between India and Pakistan. The daily Beating Retreat ceremony performed by soldiers from both nations is a popular tourist attraction showcasing military pageantry and patriotic fervor. The ceremony represents both rivalry and respect.'
        },
        
        # HARYANA
        {
            'name': 'Kurukshetra',
            'state': 'Haryana',
            'location': 'Kurukshetra',
            'year_built': 'Ancient',
            'official_description': 'The sacred land where the epic Mahabharata war was fought and where Lord Krishna delivered the Bhagavad Gita. The area is dotted with numerous temples, sacred tanks, and sites of historical significance. It remains an important pilgrimage destination for Hindus.'
        },
        {
            'name': 'Pinjore Gardens',
            'state': 'Haryana',
            'location': 'Panchkula',
            'year_built': '17th Century',
            'official_description': 'A Mughal garden built by Nawab Fidai Khan. The seven-terraced garden features fountains, pavilions, and lush greenery. It showcases Persian garden design principles and provides insight into Mughal landscape architecture and their love for gardens.'
        },
        
        # GUJARAT
        {
            'name': 'Sabarmati Ashram',
            'state': 'Gujarat',
            'location': 'Ahmedabad',
            'year_built': '1917',
            'official_description': 'Mahatma Gandhi\'s residence for 12 years and the base for his non-violent freedom struggle. From here, Gandhi launched the historic Dandi March in 1930. The ashram houses a museum with Gandhi\'s photographs, letters, and personal belongings.'
        },
        {
            'name': 'Rani Ki Vav',
            'state': 'Gujarat',
            'location': 'Patan',
            'year_built': '11th Century',
            'official_description': 'A UNESCO World Heritage Site and intricately constructed stepwell. Built by Queen Udayamati, it is designed as an inverted temple with seven levels featuring over 500 principal sculptures and 1,000 minor ones. It represents the zenith of stepwell architecture in India.'
        },
        {
            'name': 'Somnath Temple',
            'state': 'Gujarat',
            'location': 'Veraval',
            'year_built': 'Rebuilt 1951',
            'official_description': 'One of the twelve Jyotirlinga shrines of Shiva. The temple has been destroyed and rebuilt several times throughout history. The current structure was built in Chalukya style and stands as a symbol of religious resilience. It faces the Arabian Sea with no land between it and Antarctica.'
        },
        {
            'name': 'Sun Temple Modhera',
            'state': 'Gujarat',
            'location': 'Mehsana',
            'year_built': '1026',
            'official_description': 'A magnificent temple dedicated to the Sun God built by King Bhima I of the Solanki dynasty. The temple complex features intricately carved pillars and panels depicting scenes from Hindu mythology. It is architecturally aligned so that the sun\'s rays illuminate the sanctum during equinoxes.'
        },
        
        # MADHYA PRADESH
        {
            'name': 'Khajuraho Temples',
            'state': 'Madhya Pradesh',
            'location': 'Khajuraho',
            'year_built': '950-1050 CE',
            'official_description': 'A UNESCO World Heritage Site featuring 22 surviving temples known for their nagara-style architecture and erotic sculptures. Built by Chandela dynasty rulers, these temples are celebrated for their intricate stone carvings depicting various aspects of life including music, dance, and spirituality.'
        },
        {
            'name': 'Sanchi Stupa',
            'state': 'Madhya Pradesh',
            'location': 'Sanchi',
            'year_built': '3rd Century BCE',
            'official_description': 'A UNESCO World Heritage Site and one of the oldest Buddhist monuments. Built by Emperor Ashoka, the Great Stupa contains relics of Buddha. The site features ornate stone gateways (toranas) with exquisite carvings depicting stories from Buddha\'s life and Jataka tales.'
        },
        {
            'name': 'Gwalior Fort',
            'state': 'Madhya Pradesh',
            'location': 'Gwalior',
            'year_built': '8th Century',
            'official_description': 'One of India\'s most invincible forts, described as "the pearl in the necklace of the forts of Hind." The fort complex includes palaces, temples, and the spectacular Man Mandir Palace with its blue ceramic tile decoration. It has witnessed numerous battles and dynasties.'
        },
        
        # ODISHA
        {
            'name': 'Konark Sun Temple',
            'state': 'Odisha',
            'location': 'Konark',
            'year_built': '1250',
            'official_description': 'A UNESCO World Heritage Site designed as a gigantic chariot of the Sun God with 24 wheels, pulled by seven horses. Built in Kalinga architecture style, it is adorned with intricate stone carvings and sculptures. The temple is also known as the Black Pagoda.'
        },
        {
            'name': 'Jagannath Temple',
            'state': 'Odisha',
            'location': 'Puri',
            'year_built': '12th Century',
            'official_description': 'One of the four Char Dham pilgrimage sites for Hindus. The temple is dedicated to Lord Jagannath and is famous for its annual Rath Yatra (chariot festival) where deities are pulled in massive chariots. The temple kitchen is the world\'s largest, serving thousands daily.'
        },
        {
            'name': 'Udayagiri and Khandagiri Caves',
            'state': 'Odisha',
            'location': 'Bhubaneswar',
            'year_built': '1st Century BCE',
            'official_description': 'Rock-cut caves built for Jain monks. The caves feature intricate carvings depicting religious and secular life of ancient India. The Hathigumpha (Elephant Cave) inscription provides valuable historical information about King Kharavela\'s reign.'
        },
        
        # ASSAM
        {
            'name': 'Kamakhya Temple',
            'state': 'Assam',
            'location': 'Guwahati',
            'year_built': '8th-17th Century',
            'official_description': 'One of the oldest Shakti Peethas dedicated to Goddess Kamakhya. Built in Nilachal style, the temple is an important pilgrimage site for Tantric worshippers. The annual Ambubachi Mela celebrates the goddess\'s menstruation and attracts thousands of devotees.'
        },
        {
            'name': 'Rang Ghar',
            'state': 'Assam',
            'location': 'Sivasagar',
            'year_built': '1746',
            'official_description': 'An amphitheater built by the Ahom kings, considered one of Asia\'s oldest surviving amphitheaters. Built in the shape of an inverted boat, it served as a royal pavilion for watching sports and cultural events. It showcases unique Ahom architecture.'
        },
        
        # SIKKIM
        {
            'name': 'Rumtek Monastery',
            'state': 'Sikkim',
            'location': 'Gangtok',
            'year_built': '1960s',
            'official_description': 'The largest monastery in Sikkim and seat of the Karmapa. Built in traditional Tibetan style, it houses precious religious artifacts, golden stupas, and rare Buddhist manuscripts. The monastery offers panoramic views of the surrounding Himalayan ranges.'
        },
        {
            'name': 'Pemayangtse Monastery',
            'state': 'Sikkim',
            'location': 'Pelling',
            'year_built': '1705',
            'official_description': 'One of Sikkim\'s oldest and most important monasteries belonging to the Nyingma order. The three-story monastery features magnificent wall paintings, sculptures, and a seven-tiered wooden structure depicting the celestial abode of Guru Padmasambhava.'
        },
        
        # HIMACHAL PRADESH
        {
            'name': 'Shimla Christ Church',
            'state': 'Himachal Pradesh',
            'location': 'Shimla',
            'year_built': '1857',
            'official_description': 'The second oldest church in North India, built in Neo-Gothic style. Located on The Ridge, it is a prominent landmark of Shimla. The church features stained glass windows representing faith, hope, charity, fortitude, patience, and humility.'
        },
        {
            'name': 'Bhimakali Temple',
            'state': 'Himachal Pradesh',
            'location': 'Sarahan',
            'year_built': '12th Century',
            'official_description': 'A temple complex dedicated to Goddess Bhimakali. Built in Hindu-Buddhist architectural style with distinctive pagoda-like towers, it features exquisite wood carvings and silver decorations. The temple offers breathtaking views of the Himalayan peaks.'
        },
        
        # UTTARAKHAND
        {
            'name': 'Badrinath Temple',
            'state': 'Uttarakhand',
            'location': 'Badrinath',
            'year_built': '8th-9th Century',
            'official_description': 'One of the four Char Dham pilgrimage sites dedicated to Lord Vishnu. Located at 3,300 meters in the Garhwal Himalayas, it is believed to have been established by Adi Shankaracharya. The temple opens for six months annually due to extreme winter conditions.'
        },
        {
            'name': 'Kedarnath Temple',
            'state': 'Uttarakhand',
            'location': 'Kedarnath',
            'year_built': '8th Century',
            'official_description': 'One of the twelve Jyotirlingas located at 3,583 meters in the Himalayas. The temple is dedicated to Lord Shiva and is built of massive stone slabs. Despite the devastating 2013 floods, the temple structure remained intact, considered miraculous by devotees.'
        },
        {
            'name': 'Rishikesh Lakshman Jhula',
            'state': 'Uttarakhand',
            'location': 'Rishikesh',
            'year_built': '1939',
            'official_description': 'An iconic suspension bridge over the Ganges River. Named after Lord Rama\'s brother Lakshman, it is believed he crossed the river at this spot using jute ropes. The 450-foot bridge connects two villages and offers stunning views of the river and surrounding hills.'
        },
        
        # JAMMU & KASHMIR
        {
            'name': 'Vaishno Devi Temple',
            'state': 'Jammu and Kashmir',
            'location': 'Katra',
            'year_built': 'Ancient',
            'official_description': 'One of the holiest Hindu temples dedicated to Goddess Vaishno Devi. Located in the Trikuta Mountains at 5,200 feet, pilgrims trek 12 km to reach the cave shrine. It is one of the most visited pilgrimage sites in India with millions of devotees annually.'
        },
        {
            'name': 'Shankaracharya Temple',
            'state': 'Jammu and Kashmir',
            'location': 'Srinagar',
            'year_built': '200 BCE',
            'official_description': 'Dedicated to Lord Shiva, this temple sits atop Shankaracharya Hill at 1,000 feet above the valley. It offers panoramic views of Srinagar, Dal Lake, and the Himalayas. The temple is believed to have been visited by Adi Shankaracharya in 750 CE.'
        },
        
        # LADAKH
        {
            'name': 'Thiksey Monastery',
            'state': 'Ladakh',
            'location': 'Leh',
            'year_built': '15th Century',
            'official_description': 'A Tibetan Buddhist monastery affiliated with the Gelug sect. The 12-story complex houses numerous stupas, statues, and a 49-foot tall Maitreya Buddha statue. The monastery offers spectacular views of the Indus Valley and surrounding mountains.'
        },
        {
            'name': 'Hemis Monastery',
            'state': 'Ladakh',
            'location': 'Leh',
            'year_built': '1630',
            'official_description': 'The largest and wealthiest monastery in Ladakh, dedicated to Padmasambhava. It houses a copper-gilt statue of Buddha, stupas of gold and silver, and sacred thangkas. The annual Hemis Festival celebrating Guru Padmasambhava\'s birth is a major attraction.'
        },
        
        # ANDHRA PRADESH
        {
            'name': 'Tirupati Balaji Temple',
            'state': 'Andhra Pradesh',
            'location': 'Tirupati',
            'year_built': '9th Century',
            'official_description': 'The richest and most visited Hindu temple in the world, dedicated to Lord Venkateswara. Located in the Tirumala hills, it receives offerings worth millions daily. The temple\'s Dravidian architecture features a gold-plated dome and intricate carvings.'
        },
        {
            'name': 'Charminar Hyderabad',
            'state': 'Andhra Pradesh',
            'location': 'Hyderabad',
            'year_built': '1591',
            'official_description': 'An iconic monument and mosque built by Muhammad Quli Qutb Shah. The structure with four grand arches and minarets showcases Indo-Islamic architecture. It stands at the heart of the old city and is surrounded by bustling bazaars.'
        },
        {
            'name': 'Amaravati Stupa',
            'state': 'Andhra Pradesh',
            'location': 'Amaravati',
            'year_built': '3rd Century BCE',
            'official_description': 'One of the oldest and largest Buddhist stupas in India, built during the reign of Emperor Ashoka. Though in ruins, the site reveals magnificent sculpture panels depicting Buddha\'s life. The Amaravati School of Art is renowned for its unique sculptural style.'
        },
        
        # BIHAR
        {
            'name': 'Mahabodhi Temple',
            'state': 'Bihar',
            'location': 'Bodh Gaya',
            'year_built': '5th-6th Century',
            'official_description': 'A UNESCO World Heritage Site marking the place where Buddha attained enlightenment under the Bodhi Tree. The 55-meter pyramidal tower is an excellent example of early brick structures in India. It remains the holiest site for Buddhists worldwide.'
        },
        {
            'name': 'Nalanda University Ruins',
            'state': 'Bihar',
            'location': 'Nalanda',
            'year_built': '5th Century',
            'official_description': 'A UNESCO World Heritage Site and ruins of one of the world\'s first residential universities. At its peak, Nalanda housed 10,000 students and 2,000 teachers. The site includes monasteries, temples, and lecture halls showcasing ancient Indian education systems.'
        },
        {
            'name': 'Vikramshila University',
            'state': 'Bihar',
            'location': 'Bhagalpur',
            'year_built': '8th Century',
            'official_description': 'One of the two most important centers of Buddhist learning in India during the Pala Empire. The ruins reveal a large stupa, monasteries, and a library. It was established by King Dharmapala and attracted scholars from across Asia.'
        },
        
        # JHARKHAND
        {
            'name': 'Baidyanath Temple',
            'state': 'Jharkhand',
            'location': 'Deoghar',
            'year_built': 'Ancient',
            'official_description': 'One of the twelve Jyotirlingas dedicated to Lord Shiva. The temple complex includes 22 temples and is a major pilgrimage site. During the holy month of Shravan, millions of devotees carry holy water from the Ganges to offer at the temple.'
        },
        {
            'name': 'Hundru Falls',
            'state': 'Jharkhand',
            'location': 'Ranchi',
            'year_built': 'Natural',
            'official_description': 'One of India\'s highest waterfalls where the Subarnarekha River plunges 320 feet. The falls create a spectacular sight especially during monsoons. The surrounding area offers scenic beauty and is a popular picnic spot.'
        },
        
        # CHHATTISGARH
        {
            'name': 'Chitrakote Falls',
            'state': 'Chhattisgarh',
            'location': 'Bastar',
            'year_built': 'Natural',
            'official_description': 'Known as the Niagara Falls of India, these horseshoe-shaped falls on the Indravati River span 300 meters. During monsoon, the falls create a thunderous roar and a spectacular sight. The surrounding area is rich in tribal culture and natural beauty.'
        },
        {
            'name': 'Sirpur Buddhist Sites',
            'state': 'Chhattisgarh',
            'location': 'Mahasamund',
            'year_built': '5th-8th Century',
            'official_description': 'An important Buddhist archaeological site with ruins of monasteries, viharas, and the Lakshman Temple. The site reveals intricate brick architecture and sculptures from the Somvanshi period. Excavations continue to uncover more Buddhist structures.'
        },
        
        # TRIPURA
        {
            'name': 'Ujjayanta Palace',
            'state': 'Tripura',
            'location': 'Agartala',
            'year_built': '1901',
            'official_description': 'A former royal palace built by Maharaja Radha Kishore Manikya. The palace showcases Indo-Saracenic architecture with Mughal domes and Hindu pillars. Now a state museum, it houses royal artifacts, manuscripts, and displays on Tripura\'s history and culture.'
        },
        {
            'name': 'Neermahal',
            'state': 'Tripura',
            'location': 'Melaghar',
            'year_built': '1930',
            'official_description': 'A water palace built in the middle of Rudrasagar Lake by Maharaja Bir Bikram. The palace blends Hindu and Muslim architectural styles and served as the royal summer residence. It hosts a water festival showcasing Tripura\'s cultural heritage.'
        },
        
        # MANIPUR
        {
            'name': 'Kangla Fort',
            'state': 'Manipur',
            'location': 'Imphal',
            'year_built': 'Ancient',
            'official_description': 'The ancient seat of Manipur\'s rulers for nearly 2,000 years. The fort complex includes temples, ceremonial buildings, and historical structures. It holds immense religious and historical significance for the Meitei people and houses two sacred temples.'
        },
        {
            'name': 'Shri Govindajee Temple',
            'state': 'Manipur',
            'location': 'Imphal',
            'year_built': '1846',
            'official_description': 'A Vaishnavaite temple built by Maharaja Nara Singh. The twin-domed temple features gold-covered domes and pinnacles. It is an important center of Manipuri Vaishnavism and showcases unique Manipuri architecture blending Hindu and local styles.'
        },
        
        # MEGHALAYA
        {
            'name': 'Living Root Bridges',
            'state': 'Meghalaya',
            'location': 'Cherrapunji',
            'year_built': 'Ancient (Living)',
            'official_description': 'Unique bridges made from living roots of rubber trees by the Khasi and Jaintia people. These bioengineered structures grow stronger over time and can last centuries. The double-decker root bridge in Nongriat village is especially famous and takes about 15-20 years to become functional.'
        },
        {
            'name': 'Nohkalikai Falls',
            'state': 'Meghalaya',
            'location': 'Cherrapunji',
            'year_built': 'Natural',
            'official_description': 'India\'s tallest plunge waterfall with a height of 1,115 feet. The falls create a spectacular sight especially during monsoons, plunging into a green pool. The name derives from a tragic local legend and the surrounding area offers breathtaking views.'
        },
        
        # MIZORAM
        {
            'name': 'Solomon\'s Temple',
            'state': 'Mizoram',
            'location': 'Aizawl',
            'year_built': '1996',
            'official_description': 'Built by the Kohhran Thianghlim (Pentecostal Church), this structure is modeled after Solomon\'s Temple in Jerusalem. Standing 163 feet tall, it is one of the largest churches in Mizoram. The building showcases modern religious architecture and serves as a significant Christian pilgrimage site.'
        },
        {
            'name': 'Phawngpui Peak',
            'state': 'Mizoram',
            'location': 'Champhai',
            'year_built': 'Natural',
            'official_description': 'The highest peak in Mizoram at 2,157 meters, also known as Blue Mountain. The peak holds spiritual significance for Mizos who believe it to be the dwelling place of gods. The area is rich in biodiversity and offers panoramic views of Myanmar.'
        },
        
        # NAGALAND
        {
            'name': 'Kohima War Cemetery',
            'state': 'Nagaland',
            'location': 'Kohima',
            'year_built': '1944',
            'official_description': 'A memorial dedicated to soldiers of the Allied Forces who died in World War II during the Battle of Kohima. The well-maintained cemetery features the famous Kohima Epitaph: "When you go home, tell them of us and say, for your tomorrow, we gave our today."'
        },
        {
            'name': 'Dzukou Valley',
            'state': 'Nagaland',
            'location': 'Kohima-Senapati border',
            'year_built': 'Natural',
            'official_description': 'A valley located at the border of Nagaland and Manipur, famous for its seasonal flowers and natural beauty. Known for the Dzukou lily that blooms in June-July, the valley offers pristine landscapes and is a popular trekking destination.'
        },
        
        # ARUNACHAL PRADESH
        {
            'name': 'Tawang Monastery',
            'state': 'Arunachal Pradesh',
            'location': 'Tawang',
            'year_built': '1680',
            'official_description': 'The largest monastery in India and second largest in the world after Lhasa\'s Potala Palace. Built by Merak Lama Lodre Gyatso, it belongs to the Gelugpa sect. The monastery houses a 28-foot golden Buddha statue and a valuable library of ancient manuscripts.'
        },
        {
            'name': 'Ita Fort',
            'state': 'Arunachal Pradesh',
            'location': 'Itanagar',
            'year_built': '14th-15th Century',
            'official_description': 'A historical fort built with lakhs of bricks irregularly shaped. The name "Ita" means brick in the local language. The fort showcases ancient engineering techniques and offers insights into the region\'s medieval history. Some sections of the fort are well-preserved.'
        },
        
        # ANDAMAN & NICOBAR ISLANDS
        {
            'name': 'Cellular Jail',
            'state': 'Andaman and Nicobar Islands',
            'location': 'Port Blair',
            'year_built': '1906',
            'official_description': 'A colonial prison also known as Kālā Pānī (Black Water). It was used to exile political prisoners during the British rule. The jail\'s seven wings radiate from a central tower, designed for solitary confinement. Now a national memorial, it stands as a symbol of India\'s freedom struggle.'
        },
        {
            'name': 'Ross Island',
            'state': 'Andaman and Nicobar Islands',
            'location': 'Port Blair',
            'year_built': '1857',
            'official_description': 'Once the administrative headquarters of the British in the Andamans, now a tourist destination. The island features ruins of colonial buildings overtaken by nature, including a church, bakery, and officers\' quarters. It offers glimpses into colonial lifestyle and history.'
        },
        
        # LAKSHADWEEP
        {
            'name': 'Ujra Mosque',
            'state': 'Lakshadweep',
            'location': 'Kavaratti',
            'year_built': 'Ancient',
            'official_description': 'One of the most beautiful mosques in Lakshadweep, known for its intricate wood carvings and architectural beauty. The mosque features a library with ancient Islamic texts and manuscripts. It showcases the Islamic cultural heritage of the islands.'
        },
        {
            'name': 'Kavaratti Marine Aquarium',
            'state': 'Lakshadweep',
            'location': 'Kavaratti',
            'year_built': '1986',
            'official_description': 'India\'s first low-temperature aquarium displaying rare marine life from the Lakshadweep waters. The aquarium houses colorful corals, tropical fish, and other marine specimens. It serves as an important center for marine biology education and conservation.'
        },
        
        # PUDUCHERRY
        {
            'name': 'Aurobindo Ashram',
            'state': 'Puducherry',
            'location': 'Puducherry',
            'year_built': '1926',
            'official_description': 'Founded by Sri Aurobindo and The Mother, this spiritual community attracts seekers from around the world. The ashram promotes integral yoga and human unity. The main building houses the samadhi (tomb) of Sri Aurobindo and The Mother, covered with flowers daily.'
        },
        {
            'name': 'Auroville',
            'state': 'Puducherry',
            'location': 'Auroville',
            'year_built': '1968',
            'official_description': 'An experimental township dedicated to human unity, founded by The Mother and designed by architect Roger Anger. The Matrimandir, a golden metallic sphere, serves as the soul of Auroville. The community promotes sustainable living and hosts residents from over 50 countries.'
        },
        
        # CHANDIGARH
        {
            'name': 'Rock Garden',
            'state': 'Chandigarh',
            'location': 'Chandigarh',
            'year_built': '1957',
            'official_description': 'A sculpture garden created by Nek Chand entirely from industrial and urban waste. Spread over 40 acres, it features thousands of sculptures of animals, birds, and humans made from recycled materials. It stands as a testament to sustainable art and creativity.'
        },
        {
            'name': 'Capitol Complex',
            'state': 'Chandigarh',
            'location': 'Chandigarh',
            'year_built': '1965',
            'official_description': 'A UNESCO World Heritage Site designed by Le Corbusier. The complex houses the Legislative Assembly, Secretariat, and High Court. It represents the architect\'s vision of modernist architecture and urban planning, featuring brutalist concrete structures and open plazas.'
        },
        
        # DADRA & NAGAR HAVELI AND DAMAN & DIU
        {
            'name': 'Diu Fort',
            'state': 'Dadra and Nagar Haveli and Daman and Diu',
            'location': 'Diu',
            'year_built': '1535',
            'official_description': 'A massive Portuguese fort built to defend against Mughal and Maratha attacks. The fort overlooks the Arabian Sea and features bastions, cannons, and a lighthouse. Its architecture reflects Portuguese military engineering with Gothic-style gateways and a chapel.'
        },
        {
            'name': 'St. Paul\'s Church',
            'state': 'Dadra and Nagar Haveli and Daman and Diu',
            'location': 'Diu',
            'year_built': '1610',
            'official_description': 'A beautiful Baroque-style church dedicated to Our Lady of Immaculate Conception. The church features ornate wooden altars, shell-embellished designs, and intricate carvings. It showcases Portuguese religious architecture and remains an active place of worship.'
        },
    ]
    
    # Add all monuments to database
    added_count = 0
    for data in monuments_data:
        monument = Monument(**data)
        db_session.add(monument)
        added_count += 1
    
    db_session.commit()
    
    print(f"\n✅ Successfully added {added_count} monuments to the database!")
    print(f"Total monuments now: {db_session.query(Monument).count()}")
    
    # Display state-wise count
    from sqlalchemy import func
    state_counts = db_session.query(
        Monument.state, 
        func.count(Monument.id)
    ).group_by(Monument.state).order_by(Monument.state).all()
    
    print("\n📊 Monuments by State/UT:")
    print("-" * 60)
    for state, count in state_counts:
        print(f"{state}: {count} monuments")

if __name__ == '__main__':
    seed_monuments()
