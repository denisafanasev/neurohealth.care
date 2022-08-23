class EducationProgram():
    """
    Обучающая программа
    """    

    id = None
    name = None
    description = None
    subscription_payment_link = None
    education_stream_payment_link = None
    support_channel_link = None

    def __init__(self, _id, _name, _description, _subscription_payment_link, _education_stream_payment_link, _support_channel_link):
        self.id = _id
        self.name = _name
        self.description = _description
        self.subscription_payment_link = _subscription_payment_link
        self.education_stream_payment_link = _education_stream_payment_link
        self.support_channel_link = _support_channel_link