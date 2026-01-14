def mock_lead_capture(name: str, email: str, platform: str):
    result = {
        "status": "success",
        "message": f"Lead captured successfully for {name}",
        "data": {
            "name": name,
            "email": email,
            "platform": platform
        }
    }

    print(result["message"])  # optional for CLI visibility
    return result
