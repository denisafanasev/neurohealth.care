from services.education_program_subscription_service import EducationProgramSubscriptionService

class EducationProgramSubscriptionPageController():
    """
    Controller for the education program subscription page
    """

    def __init__(self):
        pass

    def get_page_data(self, _education_program_id):
        """
        Возвращает данные для страницы в отморматированном виде
        """

        service = EducationProgramSubscriptionService()

        education_program = service.get_education_program(_education_program_id)

        _data = {
            "subscription_payment_link": education_program.subscription_payment_link,
            "support_channel_link": education_program.support_channel_link
        }

        return _data
