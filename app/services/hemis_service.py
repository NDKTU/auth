import httpx

from app.exceptions.auth_exceptions import InvalidCredentialsException
from app.schemas.hemis import HemisProfileData

HEMIS_BASE = "https://student.ndki.uz/rest/v1"


class HemisService:
    async def login(self, login: str, password: str) -> HemisProfileData:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"{HEMIS_BASE}/auth/login",
                    json={"login": login, "password": password},
                )
                resp.raise_for_status()
                body = resp.json()
                if not body.get("success"):
                    raise InvalidCredentialsException()
                token = body["data"]["token"]

                resp = await client.get(
                    f"{HEMIS_BASE}/account/me",
                    headers={"Authorization": f"Bearer {token}"},
                )
                resp.raise_for_status()
                profile = resp.json()["data"]
        except httpx.HTTPStatusError:
            raise InvalidCredentialsException()
        except httpx.RequestError:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="HEMIS tizimi bilan bog'lanib bo'lmadi",
            )

        return HemisProfileData(
            hemis_id=profile["id"],
            student_id_number=profile["student_id_number"],
            passport_pin=profile.get("passport_pin"),
            first_name=profile.get("first_name"),
            second_name=profile.get("second_name"),
            third_name=profile.get("third_name"),
            full_name=profile.get("full_name"),
            university=profile.get("university"),
            email=profile.get("email"),
            birth_date=profile.get("birth_date"),
            image=profile.get("image"),
            raw_data=profile,
        )
