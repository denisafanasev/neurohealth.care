from datetime import datetime

from models.module_manager import EducationModuleManager
from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.timetable_manager import TimetableManager

class CoursesAccessManager():
    """
    Manage access user to education programms, courses and modules
    """

    def is_user_has_active_subscription(self, _user_id):
        """
        Return is user has an active subscription

        Args:
            _user_id (int): user id
        
        Returns:
            Boolean: is there active subsription
            Date: Date of subscription expiration
        """

        user_manager = UserManager()
        user = user_manager.get_user_by_id(_user_id)

        if user.education_module_expiration_date >= datetime.now():
            return True, user.education_module_expiration_date
        
        return False, user.education_module_expiration_date


    def is_course_module_avalable_for_user(self, _course_id, _module_id, _user_id):
        """
        The function of checking the accessibility of the module for the user

        Args:
            _course_id (Integer): ID Course
            _module_id (Integer): ID module
            _user_id (Integer): ID User

        Returns:
            Boolean: Available module for the user or not
            Date: Start access date
        """

        access_start_date = None

        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        # if the user is superuser, then immediately return True and do not check anything else
        if user.role == 'superuser':
            return True, None

        # If this is an regular user, let's see what kind of course and module
        course = course_manager.get_course_by_id(_course_id)
        course_modules = module_manager.get_course_modules_list(_course_id)
        first_module = course_modules[0]

        # first module os all corses everything avalable for all users
        if first_module.id == _module_id:
            return True, None
    
        # additinal courses avalable only for users with subscription
        if course.type == 'additional':
            is_access, subscription_expiration_date = self.is_user_has_active_subscription(user.user_id)
            return is_access, None

        # modules of main courses avalable only in terms of education streams
        # we have to check is there active education stream for the user at tjis time
        if course.type == 'main':

            education_stream_manager = EducationStreamManager()

            education_streams = education_stream_manager.get_education_streams_list_by_id_user(user.user_id, user.role)
            active_education_stream = None

            for education_stream in education_streams:

                # check if education stream is active
                # if the user is in some education stream, choose the stream with the biggest end date
                if education_stream.status == "идет":
                    if active_education_stream is None:
                        active_education_stream = education_stream
                    else:
                        if active_education_stream.date_end <= education_stream.date_end:
                            active_education_stream = education_stream
                
            # now we have to check access to the module of the course
            if active_education_stream is not None:

                timetable_manager = TimetableManager()
                timetable = timetable_manager.get_timetable_by_id_module_and_id_education_stream(_module_id, active_education_stream.id)
                access_start_date = timetable.date_start
                if datetime.today() >= timetable.date_start:
                    return True, timetable.date_start
                else:
                    return False, timetable.date_start

        return False, access_start_date
