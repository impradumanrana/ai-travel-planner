def _normalize_place_name(place_name: str):
    return place_name.strip().lower().replace("-", " ")


DESTINATION_PROFILES = {
    "tirupati": {
        "destination_type": "temple city / pilgrimage destination",
        "outdoor_activities": [
            "early morning visit to Sri Venkateswara Temple if darshan is planned",
            "Sri Padmavathi Ammavari Temple",
            "ISKCON Tirupati",
            "Kapila Theertham if weather is clear",
            "local market visit for prasadam and souvenirs",
        ],
        "indoor_activities": [
            "temple darshan and covered queue planning",
            "regional vegetarian meal break",
            "rest at hotel during heavy rain or peak afternoon heat",
            "museum or temple complex visit where available",
        ],
        "food_suggestions": [
            "South Indian vegetarian meals",
            "idli, dosa, pongal, curd rice, lemon rice",
            "local Andhra meals at a hygienic restaurant",
        ],
        "avoid": [
            "monasteries",
            "snow activities",
            "high-altitude trekking",
            "trek pants as the main clothing suggestion",
        ],
        "dress_style": "modest, breathable temple-friendly clothing",
        "men_clothing": [
            "light cotton shirt or t-shirt",
            "comfortable trousers, cotton pants, or dhoti if preferred",
            "sandals or easy-to-remove footwear for temple visits",
        ],
        "women_clothing": [
            "cotton saree, salwar suit, kurti with leggings, or other modest breathable clothing",
            "light dupatta or shawl for temple comfort",
            "sandals or easy-to-remove footwear for temple visits",
        ],
        "packing_extras": [
            "small towel or handkerchief",
            "reusable water bottle",
            "temple-appropriate clothing",
            "light rain protection in monsoon months",
        ],
    },
    "manali": {
        "destination_type": "mountain / hill-station destination",
        "outdoor_activities": [
            "Hadimba Temple",
            "Solang Valley",
            "Old Manali walk",
            "Mall Road",
            "nearby viewpoints when roads and weather are safe",
        ],
        "indoor_activities": [
            "cafes in Old Manali",
            "local markets",
            "hotel rest during rain",
            "short scenic drives if roads are safe",
        ],
        "food_suggestions": [
            "local Himachali meal",
            "cafe lunch in Old Manali",
            "hot soup, momos, or thukpa",
        ],
        "avoid": [
            "beach activities",
            "temple-only itinerary",
        ],
        "dress_style": "layered clothing for changing mountain weather",
        "men_clothing": [
            "quick-dry t-shirt or shirt",
            "comfortable trousers or trek pants",
            "warm jacket or fleece layer",
        ],
        "women_clothing": [
            "warm layers with jeans, trousers, or comfortable travel pants",
            "sweater or fleece",
            "light ethnic wear only for easy city walks, not active mountain days",
        ],
        "packing_extras": [
            "warm jacket",
            "rain jacket or windcheater",
            "comfortable walking shoes",
        ],
    },
}


def get_destination_profile(place_name: str):
    """
    Return a small curated local profile when available.
    Unknown places get safe generic categories instead of fake named attractions.
    """
    normalized = _normalize_place_name(place_name)

    for key, profile in DESTINATION_PROFILES.items():
        if key in normalized:
            return profile

    return {
        "destination_type": "general travel destination",
        "outdoor_activities": [
            "popular local landmarks",
            "main market or old town walk",
            "safe viewpoints, parks, or waterfront areas if available",
        ],
        "indoor_activities": [
            "museum or cultural center if available",
            "covered market",
            "local restaurant or cafe break",
            "hotel rest during bad weather",
        ],
        "food_suggestions": [
            "well-rated local restaurant",
            "regional food based on the destination",
            "light meals during hot or rainy weather",
        ],
        "avoid": [
            "inventing specific attraction names not known from the profile",
            "assuming mountains, beaches, monasteries, snow, or trekking without evidence",
        ],
        "dress_style": "comfortable weather-appropriate travel clothing",
        "men_clothing": [
            "breathable shirt or t-shirt",
            "comfortable trousers or light pants",
            "comfortable walking shoes",
        ],
        "women_clothing": [
            "breathable western or ethnic wear suitable for the destination",
            "comfortable trousers, kurti, salwar suit, dress, or saree based on preference",
            "comfortable walking shoes or sandals",
        ],
        "packing_extras": [
            "basic medicines",
            "phone charger and power bank",
            "reusable water bottle",
        ],
    }
