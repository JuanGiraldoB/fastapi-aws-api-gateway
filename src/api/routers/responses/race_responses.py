GET_RACES_200_RESPONSE = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "Bahrain": {
                        "race": "Bahrain",
                        "date": "02 Mar 2024",
                        "winner": "Max Verstappen",
                        "car": "Red Bull Racing Honda RBPT",
                        "laps": "57",
                        "duration": "1:31:44.742"
                    }
                }
            }
        }
    }
}

GET_FASTEST_LAPS_200_RESPONSE = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "Bahrain": {
                        "driver": "Max Verstappen",
                        "driver_prefix": "VER",
                        "car": "Red Bull Racing Honda RBPT",
                        "lap_time": "1:32.608"
                    },
                }
            }
        }
    }
}
