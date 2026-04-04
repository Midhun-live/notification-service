from app.services.template_service import TemplateService
try:
    print(TemplateService.render("order_shipped", {"name": "Bob", "order_id": "XYZ"}))
except Exception as e:
    print("Error:", e)
