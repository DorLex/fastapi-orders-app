from fastapi import APIRouter, Depends, BackgroundTasks

from src.accounts.services.auth import verify_token
from src.notifications.schemas import EmailSchema
from src.notifications.service import EmailNotificationService

router = APIRouter(
    prefix='/notifications',
    tags=['notifications'],
    dependencies=[Depends(verify_token)]
)


@router.post('/send-email/', response_model=dict)
async def send_email(email: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(EmailNotificationService().send_email, email)

    return {'message': f'Email отправлен по адресам: {email.emails}'}
