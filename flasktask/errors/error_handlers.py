from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

ERROR_403 = 403
ERROR_404 = 404
ERROR_500 = 500

error_pages = {
    ERROR_403: f'errors/{ERROR_403}.html',
    ERROR_404: f'errors/{ERROR_404}.html',
    ERROR_500: f'errors/{ERROR_500}.html',
}

err_msg = 'An error occurred'

@errors.app_errorhandler(ERROR_403)
def error_403(error):
    return render_template(error_pages.get(ERROR_403) or err_msg), ERROR_403

@errors.app_errorhandler(ERROR_404)
def error_404(error):
    return render_template(error_pages.get(ERROR_404) or err_msg), ERROR_404

@errors.app_errorhandler(ERROR_500)
def error_500(error):
    return render_template(error_pages.get(ERROR_500) or err_msg), ERROR_500
