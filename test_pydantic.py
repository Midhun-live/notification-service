from app.schemas.notifications import NotificationCreate
data = NotificationCreate(user_id="1", channels=["email"], template="t1")
data.message = "Hello test"
print(data.model_dump())
