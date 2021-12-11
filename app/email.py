"""
Email functions
"""
from flask_mail import Message
from flask import render_template, current_app
from app import mail

def send_password_reset_email(user):
	"""
	Send password reset email to user
	"""
	token = user.get_reset_password_token()
	send_email(
		'Reset Your Password',
		sender=current_app.config['ADMIN'],
		recipients=[user.username],
		text_body=render_template('email/reset_password.txt',
															user=user, token=token),
		html_body=render_template('email/reset_password.html',
															user=user, token=token)
	)

def send_alert_email(user):
    send_email(
        'ALERT - Motion detected!',
        sender=current_app.config['ADMIN'],
        recipients=[user.username],
        text_body=render_template(
            'email/alert.txt',
            user=user,
        ),
        html_body=render_template(
            'email/alert.html',
            user=user,
        ),
    )


def send_email(subject, sender, recipients, text_body, html_body):
	"""
	Send email
	"""
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)
