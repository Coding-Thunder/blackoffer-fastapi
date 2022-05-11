def userEntity(item) -> dict:
    return {
        "name": item["name"],
        "email": item["email"],
        "password": item["password"]
    }
