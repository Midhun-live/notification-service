from fastapi import HTTPException

templates = {
    "order_shipped": "Hello {{name}}, your order {{order_id}} has shipped",
    "welcome": "Welcome {{name}} to our platform"
}

class TemplateService:
    @staticmethod
    def render(template: str, variables: dict) -> str:
        if template not in templates:
            raise HTTPException(status_code=400, detail=f"Template '{template}' not found")
            
        message = templates[template]
        
        if not variables:
            variables = {}
            
        for key, value in variables.items():
            message = message.replace(f"{{{{{key}}}}}", str(value))
            
        return message
